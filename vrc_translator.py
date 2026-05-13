import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
import time
import speech_recognition as sr
from pythonosc import udp_client, osc_server, dispatcher
import json
import os
import numpy as np
import webbrowser
import socket
import urllib.request
import zipfile
import tempfile
import subprocess
import sys
import shutil
from PIL import Image # <--- นำเข้าโมดูลโหลดรูปภาพ
from faster_whisper import WhisperModel
import keyboard
import sentry_sdk

from google import genai
from google.genai import types

def resource_path(relative_path):
    try:
        # PyInstaller สร้างโฟลเดอร์ Temp และเก็บ path ไว้ใน _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ตั้งค่า Theme เริ่มต้น
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# ================= CUSTOM WIDGET =================
class NavItem(ctk.CTkFrame):
    def __init__(self, master, text_var, command, hover_color=("gray85", "gray25"), **kwargs):
        super().__init__(master, fg_color="transparent", cursor="hand2", height=40, **kwargs)
        self.pack_propagate(False) 
        
        self.command = command
        self.is_active = False
        self.hover_color = hover_color
        
        self.indicator = ctk.CTkFrame(self, width=4, corner_radius=0, fg_color="transparent")
        self.indicator.pack(side="left", fill="y", pady=2)
        
        self.text_lbl = ctk.CTkLabel(self, text=text_var, font=ctk.CTkFont(size=14, weight="bold"), anchor="w")
        self.text_lbl.pack(side="left", fill="x", expand=True, padx=(15, 10))
        
        for w in (self, self.indicator, self.text_lbl):
            w.bind("<Button-1>", lambda e: self.command())
            w.bind("<Enter>", self.on_enter)
            w.bind("<Leave>", self.on_leave)

    def set_text(self, text):
        self.text_lbl.configure(text=text)

    def on_enter(self, e):
        if not self.is_active:
            self.configure(fg_color=self.hover_color)
    
    def on_leave(self, e):
        if not self.is_active:
            self.configure(fg_color="transparent")
            
    def set_active(self, active):
        self.is_active = active
        self.configure(fg_color=("gray80", "gray20") if active else "transparent")
        self.indicator.configure(fg_color="#2196F3" if active else "transparent")

# ================= MAIN APP =================
class SyncVRCApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1150x800")
        self.root.minsize(1000, 700)
        
        # เวอร์ชันของโปรแกรมล็อกที่ 1.0.0
        self.app_version = "1.0.0"
        self.root.title(f"SyncVRC - Real-time Voice Translator (v{self.app_version})")

        try: 
            self.root.iconbitmap(resource_path("icon.ico"))
        except Exception as e: 
            print(f"Failed to load icon: {e}")

        self.config_file = "config.json"
        
        self.is_running_out = False
        self.is_recording_out = False
        self.is_running_in = False
        self.hotkey_window = None 
        
        self.osc_client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
        
        self.recognizer_out = sr.Recognizer()
        self.recognizer_in = sr.Recognizer()
        self.whisper_lock = threading.Lock()
        
        self.mic_mapping = {}
        self.input_mic_names = []
        self.speaker_names = []
        self.get_active_devices() 

        self.current_ui_lang = "English"
        self.is_dark_mode = False 
        self.enable_telemetry_var = tk.BooleanVar(value=False)
        self.enable_mute_sync_var = tk.BooleanVar(value=False)
        self.is_vrc_muted = False 
        
        self.out_src_val = "English"
        self.out_tgt_val = "Japanese"
        self.in_src_val = "Japanese"
        self.in_tgt_val = "English"
        self.whisper_model_val = "medium"
        
        self.trans_engine_val = "Google Gemini"
        self.ai_device_val = "GPU (NVIDIA)"
        
        self.silence_timeout_val = 0.5
        self.max_record_time_val = 15
        self.beam_size_val = 2
        
        self.api_keys = {
            "Google Gemini": "",
            "DeepL API": "",
            "OpenAI": ""
        }
        
        self.hk_out = "F2"
        self.hk_in = "F3"
        self.hk_push = "None"
        
        self.latest_version_found = None
        self.latest_release_url = None
        self.latest_zip_url = None
        
        self.init_translations()
        self.setup_ui()     
        self.load_config()  
        self.init_sentry() 
        self.apply_hotkeys()
        self.change_ui_language(save=False) 
        self.apply_theme_colors()

        self.monitor_thread = threading.Thread(target=self.system_monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        self.osc_server_thread = threading.Thread(target=self.run_osc_server, daemon=True)
        self.osc_server_thread.start()
        
        threading.Thread(target=self.check_for_updates, daemon=True).start()

    def check_for_updates(self):
        repo_owner = "finalsiren1" 
        repo_name = "SyncVRC"
        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        
        try:
            req = urllib.request.Request(api_url, headers={'User-Agent': 'SyncVRC-App'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                latest_version = data.get("tag_name", "").replace("v", "")
                
                if latest_version and latest_version != self.app_version:
                    zip_url = None
                    for asset in data.get("assets", []):
                        if asset.get("name", "").endswith(".zip"):
                            zip_url = asset.get("browser_download_url")
                            break
                            
                    self.latest_version_found = latest_version
                    self.latest_release_url = data.get("html_url", f"https://github.com/{repo_owner}/{repo_name}/releases")
                    self.latest_zip_url = zip_url
                    
                    self.root.after(2000, self.prompt_update)
        except Exception:
            pass 

    def prompt_update(self):
        title = self.get_t("update_title")
        msg = self.get_t("update_msg").format(self.latest_version_found, self.app_version)
        if messagebox.askyesno(title, msg):
            self.start_update_process()
        else:
            self.show_update_button()

    def show_update_button(self):
        update_text = self.get_t("btn_update_avail").format(self.latest_version_found)
        self.btn_nav_update.configure(text=update_text)
        self.btn_nav_update.pack(fill="x", pady=5)

    def start_update_process(self):
        if self.latest_zip_url:
            self.show_downloading_ui(self.latest_zip_url)
        else:
            webbrowser.open(self.latest_release_url)

    def show_downloading_ui(self, zip_url):
        dl_window = ctk.CTkToplevel(self.root)
        dl_window.title(self.get_t("update_downloading_title"))
        dl_window.geometry("450x150")
        dl_window.transient(self.root)
        dl_window.grab_set()
        dl_window.protocol("WM_DELETE_WINDOW", lambda: None) 
        
        lbl_dl = ctk.CTkLabel(dl_window, text=self.get_t("update_downloading_msg").format(self.latest_version_found), font=ctk.CTkFont(size=14, weight="bold"))
        lbl_dl.pack(pady=(30, 15))
        
        progressbar = ctk.CTkProgressBar(dl_window, mode="indeterminate")
        progressbar.pack(fill="x", padx=40)
        progressbar.start()
        
        threading.Thread(target=self.download_and_install_update, args=(zip_url,), daemon=True).start()

    def download_and_install_update(self, zip_url):
        try:
            temp_dir = tempfile.gettempdir()
            zip_path = os.path.join(temp_dir, "syncvrc_update.zip")
            extract_path = os.path.join(temp_dir, "syncvrc_update_extracted")

            req = urllib.request.Request(zip_url, headers={'User-Agent': 'SyncVRC-App'})
            with urllib.request.urlopen(req) as response, open(zip_path, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)

            if os.path.exists(extract_path):
                shutil.rmtree(extract_path, ignore_errors=True)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

            source_dir = extract_path
            extracted_items = os.listdir(extract_path)
            if len(extracted_items) == 1 and os.path.isdir(os.path.join(extract_path, extracted_items[0])):
                source_dir = os.path.join(extract_path, extracted_items[0])

            is_compiled = getattr(sys, 'frozen', False)
            current_exe = sys.executable if is_compiled else os.path.abspath(__file__)
            current_dir = os.path.dirname(current_exe)
            
            start_cmd = f'start "" "{sys.executable}"' if is_compiled else f'start "" "{sys.executable}" "{current_exe}"'

            bat_path = os.path.join(temp_dir, "syncvrc_updater.bat")
            bat_content = f"""@echo off
title SyncVRC Auto Updater
echo ========================================
echo  SyncVRC Updater
echo  Please wait... Applying update.
echo ========================================
timeout /t 5 /nobreak > NUL
xcopy /E /Y /Q "{source_dir}\\*" "{current_dir}\\"
{start_cmd}
del /f /q "{zip_path}"
rmdir /S /Q "{extract_path}"
(goto) 2>nul & del "%~f0"
"""
            with open(bat_path, "w", encoding="utf-8") as f:
                f.write(bat_content)

            subprocess.Popen([bat_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
            os._exit(0)

        except Exception as e:
            self.root.after(0, lambda err=e: messagebox.showerror("Update Error", f"Failed to auto-update: {err}"))

    def run_osc_server(self):
        disp = dispatcher.Dispatcher()
        disp.map("/avatar/parameters/MuteSelf", self.on_vrc_mute_changed)
        while True:
            try:
                server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 9001), disp)
                server.serve_forever()
            except Exception:
                time.sleep(5) 

    def on_vrc_mute_changed(self, address, *args):
        if not self.enable_mute_sync_var.get() or not args: return
        is_muted = bool(args[0])
        if self.is_vrc_muted != is_muted:
            self.is_vrc_muted = is_muted
            if self.is_running_out:
                if self.is_vrc_muted:
                    self.root.after(0, lambda: self.log_out(self.get_t("log_mute_paused"), "info"))
                else:
                    self.root.after(0, lambda: self.log_out(self.get_t("log_mute_resumed"), "info"))

    def init_sentry(self):
        def before_send(event, hint):
            if self.enable_telemetry_var.get(): return event
            return None
        try:
            sentry_sdk.init(
                dsn="https://f57bdeaf919e6e8ee35548aac2b5df84@o4511378101456896.ingest.us.sentry.io/4511378110959616",
                send_default_pii=False, 
                traces_sample_rate=1.0,
                before_send=before_send
            )
        except Exception: pass

    def get_active_devices(self):
        try: mics = sr.Microphone.list_microphone_names()
        except: mics = []
            
        inputs, loopbacks = [], []
        seen = set()
        self.mic_mapping.clear()
        
        for i, name in enumerate(mics):
            if name not in seen:
                seen.add(name)
                self.mic_mapping[name] = i
                is_virtual = any(v in name.lower() for v in ["stereo mix", "wave link", "voicemeeter", "cable", "loopback", "virtual", "output"])
                if is_virtual: loopbacks.append(name)
                else: inputs.append(name)
                
        self.input_mic_names = inputs if inputs else ["No Microphone Found"]
        self.speaker_names = loopbacks if loopbacks else ["No Loopback Found"]
        return self.input_mic_names, self.speaker_names

    def system_monitor_loop(self):
        while True:
            detected = self.check_osc_enabled()
            try:
                if detected:
                    self.lbl_osc_indicator.configure(text=self.get_t("osc_detected"), text_color="#28a745" if not self.is_dark_mode else "#2ea043")
                else:
                    self.lbl_osc_indicator.configure(text=self.get_t("osc_not_detected"), text_color="#dc3545" if not self.is_dark_mode else "#ff6b6b")
            except: break

            if not self.is_running_out and not self.is_running_in:
                old_in, old_out = list(self.input_mic_names), list(self.speaker_names)
                new_in, new_out = self.get_active_devices()
                if old_in != new_in or old_out != new_out:
                    try: self.root.after(0, self.update_audio_dropdowns)
                    except: break

            time.sleep(3)

    def check_osc_enabled(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.bind(('0.0.0.0', 9000))
            sock.close()
            return False 
        except OSError: return True

    def update_audio_dropdowns(self):
        current_out, current_in = self.mic_combo_out.get(), self.mic_combo_in.get()
        self.mic_combo_out.configure(values=self.input_mic_names)
        self.mic_combo_in.configure(values=self.speaker_names)
        
        if current_out in self.input_mic_names: self.mic_combo_out.set(current_out)
        else: self.mic_combo_out.set(self.input_mic_names[0])
            
        if current_in in self.speaker_names: self.mic_combo_in.set(current_in)
        else: self.mic_combo_in.set(self.speaker_names[0])

    def init_translations(self):
        self.lang_map = {"English": "en", "日本語": "ja", "中文": "zh", "한국어": "ko"}
        self.translations = {
            "en": {
                "nav_trans": "Translation",
                "nav_audio": "Audio Setup",
                "nav_settings": "Settings",
                "ui_lang": "UI Language:",
                "api_key": "API Key:",
                "btn_save": "Save",
                "btn_edit": "Edit",
                "osc_status": "OSC Status: ",
                "osc_detected": "🟢 Detected",
                "osc_not_detected": "🔴 Not Detected",
                "left_frame": "Outgoing System (Speak -> VRChat)",
                "right_frame": "Incoming System (Listen -> Translate)",
                "mic_out": "Select Microphone (Your voice):",
                "src_lang_out": "From:",
                "tgt_lang_out": "Translate to:",
                "mode_auto": "Auto (Continuous)",
                "mode_push": "Push to Record",
                "btn_start_out": "Start Outgoing",
                "btn_stop_out": "Stop Outgoing",
                "btn_hold": "Hold to Speak",
                "btn_loading_model": "⏳ Loading Model...",
                "manual_label": "Manual Translate (Type and Send):",
                "btn_send": "Send",
                "log_out": "Outgoing Log:",
                "speaker_in": "Select Speaker Loopback (Virtual Audio):",
                "src_lang_in": "Listen Language:",
                "tgt_lang_in": "Translate to:",
                "btn_start_in": "Start Incoming",
                "btn_stop_in": "Stop Incoming",
                "log_in": "Incoming Log (Not sent to VRChat):",
                "warn_manual": "Please start Outgoing system before sending manual text.",
                "theme_title": "Appearance:",
                "theme_dark": "Dark Mode",
                "telemetry_lbl": "Share anonymous crash reports to help improve SyncVRC (No voice/text data collected)",
                "mute_sync_lbl": "Enable VRC Mute Sync (Pause translation when VRChat mic is muted)",
                "license": "Free for Non-Commercial Use | MIT License",
                "credit": "credit by Meiji ღ",
                "support_msg": "Buy me a snack by supporting me here:",
                "log_load_model": "Loading Whisper Model ({})... Please wait.",
                "log_model_loaded": "Whisper Model loaded successfully!",
                "log_start_mic": "Started Outgoing Mic: {}",
                "log_auto_listen": "Listening (Auto)...",
                "log_recording": "Recording...",
                "log_out_stop": "Outgoing Stopped.",
                "log_start_loop": "Started Incoming Loopback: {}",
                "log_speaker_listen": "Listening to Speaker...",
                "log_in_stop": "Incoming Stopped.",
                "log_mute_paused": "VRC Mute Sync: Microphone Muted (Paused)",
                "log_mute_resumed": "VRC Mute Sync: Microphone Unmuted (Resumed)",
                "sec_general": "General Settings",
                "sec_api": "AI & Translation Engine",
                "sec_hotkey": "Shortcut Keys",
                "engine_lbl": "Translation Engine:",
                "device_lbl": "AI Processing Device:",
                "device_info": "GPU requires NVIDIA & CUDA. CPU is slower but works on AMD/Intel PCs.",
                                "model_lbl": "Whisper Model:",
                "btn_clear_cache": "Clear Cache",
                "nav_docs": "Documentation",
                "confirm_download_title": "Download Required",
                "confirm_download_msg": "This model ({}) is not downloaded yet.\nDownload size: approx. {}\nDo you want to proceed?",
                "confirm_clear_title": "Clear Cache",
                "confirm_clear_msg": "Are you sure you want to delete all unused models?",
                "downloading_model_title": "Downloading Model",
                "downloading_model_msg": "Downloading {} model: {}%",
                "cache_cleared_msg": "Unused models have been removed.",
                "model_info_tiny": "Size: ~75 MB | RAM: ~1 GB | Accuracy: Low — Fast, suitable for simple/short phrases",
                "model_info_base": "Size: ~145 MB | RAM: ~1 GB | Accuracy: Fair — Good balance for casual use",
                "model_info_small": "Size: ~484 MB | RAM: ~2 GB | Accuracy: Good — Recommended for most users",
                "model_info_medium": "Size: ~1.5 GB | RAM: ~5 GB | Accuracy: High — Best for clear audio (Default)",
                "model_info_large": "Size: ~3.1 GB | RAM: ~10 GB | Accuracy: Very High — Best quality, requires strong GPU",

                "hk_out_lbl": "Start Outgoing:",
                "hk_in_lbl": "Start Incoming:",
                "hk_push_lbl": "Hold to Speak (Push Mode):",
                "warn_same_lang": "Source and target languages cannot be the same.",
                "warn_same_lang_lock": "Same language selected. Start button is locked until you change the language.",
                "warn_osc_forgot": "VRChat OSC not detected on default port (9000).\nIf you use a different port, you can ignore this.\nOtherwise, don't forget to enable it in the radial menu!\n\n(Starting anyway...)",
                "err_cuda_not_found": "CUDA/GPU Error: No compatible NVIDIA GPU found.\n👉 If using AMD/Intel, go to Settings -> Change 'AI Device' to CPU.\n👉 If using NVIDIA, install CUDA 12.x: https://developer.nvidia.com/cuda-12-9-1-download-archive",
                "err_api_limit": "API Limit Exceeded: Too many requests. Please check your quota or wait a moment.",
                "err_api_invalid": "API Error: Invalid API Key. Please check your key in Settings.",
                "err_api_empty": "❌ Please enter your API Key in the Settings tab before starting.",
                "alert_cuda": "CUDA/GPU Error\n\nNo compatible NVIDIA GPU was found on your system.\n\n• If you use AMD or Intel, please go to Settings and change 'AI Device' to CPU.\n• If you use NVIDIA, please download and install CUDA Toolkit 12.x from:\nhttps://developer.nvidia.com/cuda-12-9-1-download-archive\n\nThe system has been stopped.",
                "alert_api_limit": "API Rate Limit Reached\n\nYou have exceeded the API request limit. This usually happens with free-tier keys.\n\nPlease wait a moment before trying again, or consider upgrading to a paid API plan for uninterrupted use.\n\nThe system has been stopped.",
                "alert_api_invalid": "Invalid API Key\n\nYour API key was rejected by the server. Please go to Settings and check that your key is correct.\n\nThe system has been stopped.",
                "alert_whisper_error": "Speech Recognition Error\n\nFailed to load the Whisper model: {}\n\nThe system has been stopped.",
                "alert_api_generic": "Translation Error\n\nAn unexpected error occurred: {}\n\nThe system has been stopped.",
                "adv_audio_lbl": "Advanced Audio Settings",
                "silence_timeout_lbl": "Silence Timeout (Wait to finish):",
                "max_record_time_lbl": "Max Recording Time per phrase:",
                "beam_size_lbl": "AI Accuracy vs Speed (Beam Size):",
                "update_title": "Update Available",
                "update_msg": "A new version (v{}) is available! You are currently using v{}.\n\nWould you like to automatically download and install it now?",
                "btn_update_avail": "Update v{}",
                "update_downloading_title": "Downloading Update",
                "update_downloading_msg": "Downloading v{}...\nPlease wait, the app will restart automatically."
            },
            "ja": {
                "nav_trans": "翻訳メイン",
                "nav_audio": "オーディオ設定",
                "nav_settings": "一般設定",
                "ui_lang": "UI 言語:",
                "api_key": "API キー:",
                "btn_save": "保存",
                "btn_edit": "編集",
                "osc_status": "OSC ステータス: ",
                "osc_detected": "🟢 検出されました",
                "osc_not_detected": "🔴 未検出",
                "left_frame": "送信システム (音声 -> VRChat)",
                "right_frame": "受信システム (他人の音声を翻訳)",
                "mic_out": "マイクを選択 (あなたの声):",
                "src_lang_out": "翻訳元:",
                "tgt_lang_out": "翻訳先:",
                "mode_auto": "自動 (連続)",
                "mode_push": "押して録音",
                "btn_start_out": "送信開始",
                "btn_stop_out": "送信停止",
                "btn_hold": "押している間話す",
                "btn_loading_model": "⏳ モデルを読み込み中...",
                "manual_label": "手動翻訳 (入力して送信):",
                "btn_send": "送信",
                "log_out": "送信ログ:",
                "speaker_in": "スピーカーを選択 (仮想オーディオ):",
                "src_lang_in": "受信言語:",
                "tgt_lang_in": "翻訳先:",
                "btn_start_in": "受信開始",
                "btn_stop_in": "受信停止",
                "log_in": "受信ログ (VRChatには送信されません):",
                "warn_manual": "手動テキストを送信する前に、送信(Outgoing)システムを開始してください。",
                "theme_title": "外観:",
                "theme_dark": "ダークモード",
                "telemetry_lbl": "匿名のクラッシュレポートを送信してSyncVRCの改善に協力する (音声/テキストデータは収集されません)",
                "mute_sync_lbl": "VRC Mute Syncを有効にする (VRChatでミュート時に翻訳を一時停止)",
                "license": "非営利目的でのみ無料で使用可能 | MITライセンス",
                "credit": "クレジット: Meiji ღ",
                "support_msg": "おやつ代の支援はこちらからお願いします：",
                "log_load_model": "Whisperモデル({})を読み込んでいます... お待ちください。",
                "log_model_loaded": "Whisperモデルの読み込み完了！",
                "log_start_mic": "送信マイクを開始: {}",
                "log_auto_listen": "待機中 (自動)...",
                "log_recording": "録音中...",
                "log_out_stop": "送信を停止しました。",
                "log_start_loop": "受信ループバックを開始: {}",
                "log_speaker_listen": "スピーカーを待機中...",
                "log_in_stop": "受信を停止しました。",
                "log_mute_paused": "VRC Mute Sync: マイクがミュートされました (一時停止)",
                "log_mute_resumed": "VRC Mute Sync: マイクのミュートが解除されました (再開)",
                "sec_general": "一般設定",
                "sec_api": "AI & 翻訳エンジン構成",
                "sec_hotkey": "ショートカットキー",
                "engine_lbl": "翻訳エンジン:",
                "device_lbl": "AI 処理デバイス:",
                "device_info": "GPUにはNVIDIAとCUDAが必要です。CPUはAMD/Intelで動作しますが遅くなります。",
                                "model_lbl": "Whisper モデル:",
                "btn_clear_cache": "キャッシュをクリア",
                "nav_docs": "ドキュメンテーション",
                "confirm_download_title": "ダウンロードが必要です",
                "confirm_download_msg": "このモデル ({}) はまだダウンロードされていません。\nダウンロードサイズ: 約 {}\n続行しますか？",
                "confirm_clear_title": "キャッシュをクリア",
                "confirm_clear_msg": "使用されていないすべてのモデルを削除してもよろしいですか？",
                "downloading_model_title": "モデルをダウンロード中",
                "downloading_model_msg": "{} モデルをダウンロード中: {}%",
                "cache_cleared_msg": "未使用のモデルが削除されました。",
                "model_info_tiny": "サイズ: ~75 MB | RAM: ~1 GB | 精度: 低 — 高速、短いフレーズに適しています",
                "model_info_base": "サイズ: ~145 MB | RAM: ~1 GB | 精度: 普通 — カジュアルな使用に最適",
                "model_info_small": "サイズ: ~484 MB | RAM: ~2 GB | 精度: 良好 — ほとんどのユーザーにおすすめ",
                "model_info_medium": "サイズ: ~1.5 GB | RAM: ~5 GB | 精度: 高い — クリアな音声に最適 (デフォルト)",
                "model_info_large": "サイズ: ~3.1 GB | RAM: ~10 GB | 精度: 非常に高い — 最高品質、強力なGPUが必要",

                "hk_out_lbl": "送信開始:",
                "hk_in_lbl": "受信開始:",
                "hk_push_lbl": "押している間話す:",
                "warn_same_lang": "翻訳元と翻訳先の言語を同じにすることはできません。",
                "warn_same_lang_lock": "同じ言語が選択されています。言語を変更するまで開始ボタンはロックされます。",
                "warn_osc_forgot": "デフォルトポート(9000)でVRChat OSCが検出されませんでした。\n別のポートを使用している場合は無視してください。\n（そのまま開始します...）",
                "err_cuda_not_found": "CUDA/GPU エラー: 互換性のあるNVIDIA GPUが見つかりません。\n👉 AMD/Intelを使用している場合は、設定で「AIデバイス」をCPUに変更してください。\n👉 NVIDIAを使用している場合は、CUDA 12.xをインストールしてください: https://developer.nvidia.com/cuda-12-9-1-download-archive",
                "err_api_limit": "API制限超過: リクエストが多すぎます。しばらくお待ちください。",
                "err_api_invalid": "APIエラー: 無効なAPIキーです。設定を確認してください。",
                "err_api_empty": "❌ 開始する前に、設定タブでAPIキーを入力してください。",
                "alert_cuda": "CUDA/GPU エラー\n\nお使いのシステムに互換性のあるNVIDIA GPUが見つかりませんでした。\n\n• AMDまたはIntelをご利用の場合は、設定の「AIデバイス」をCPUに変更してください。\n• NVIDIAをご利用の場合は、CUDA Toolkit 12.x をダウンロードしてインストールしてください：\nhttps://developer.nvidia.com/cuda-12-9-1-download-archive\n\nシステムは停止されました。",
                "alert_api_limit": "APIレート制限\n\nAPIリクエストの制限を超えました。無料枠のキーではよく発生します。\n\n少し待ってから再度お試しいただくか、有料APIプランへのアップグレードをご検討ください。\n\nシステムは停止されました。",
                "alert_api_invalid": "無効なAPIキー\n\nAPIキーがサーバーに拒否されました。設定でキーが正しいか確認してください。\n\nシステムは停止されました。",
                "alert_whisper_error": "音声認識エラー\n\nWhisperモデルの読み込みに失敗しました: {}\n\nシステムは停止されました。",
                "alert_api_generic": "翻訳エラー\n\n予期しないエラーが発生しました: {}\n\nシステムは停止されました。",
                "adv_audio_lbl": "⚙️ 高度なオーディオ設定",
                "silence_timeout_lbl": "無音タイムアウト (発話終了の待機):",
                "max_record_time_lbl": "1回の最大録音時間:",
                "beam_size_lbl": "AIの精度と速度 (Beam Size):",
                "update_title": "アップデート利用可能",
                "update_msg": "新しいバージョン (v{}) が利用可能です！現在のバージョンは v{} です。\n\n今すぐ自動的にダウンロードしてインストールしますか？",
                "btn_update_avail": "v{} にアップデート",
                "update_downloading_title": "アップデートをダウンロード中",
                "update_downloading_msg": "v{} をダウンロードしています...\nアプリが自動的に再起動するまでお待ちください。"
            },
            "zh": {
                "nav_trans": "翻译主页",
                "nav_audio": "音频设置",
                "nav_settings": "系统设置",
                "ui_lang": "界面语言:",
                "api_key": "API 密钥:",
                "btn_save": "保存",
                "btn_edit": "编辑",
                "osc_status": "OSC 状态: ",
                "osc_detected": "🟢 已检测到",
                "osc_not_detected": "🔴 未检测到",
                "left_frame": "输出系统 (语音 -> VRChat)",
                "right_frame": "输入系统 (翻译他人的声音)",
                "mic_out": "选择麦克风 (你的声音):",
                "src_lang_out": "源语言:",
                "tgt_lang_out": "翻译为:",
                "mode_auto": "自动 (连续)",
                "mode_push": "按住录音",
                "btn_start_out": "开始输出",
                "btn_stop_out": "停止输出",
                "btn_hold": "按住说话",
                "btn_loading_model": "⏳ 正在加载模型...",
                "manual_label": "手动翻译 (输入并发送):",
                "btn_send": "发送",
                "log_out": "输出日志:",
                "speaker_in": "选择扬声器 (虚拟音频):",
                "src_lang_in": "聆听语言:",
                "tgt_lang_in": "翻译为:",
                "btn_start_in": "开始输入",
                "btn_stop_in": "停止输入",
                "log_in": "输入日志 (不会发送到 VRChat):",
                "warn_manual": "在发送手动文本之前，请先启动输出 (Outgoing) 系统。",
                "theme_title": "外观:",
                "theme_dark": "深色模式",
                "telemetry_lbl": "发送匿名崩溃报告以帮助改进 SyncVRC (不收集语音/文本数据)",
                "mute_sync_lbl": "启用 VRC Mute Sync (在 VRChat 中静音时暂停翻译)",
                "license": "仅供非商业用途免费使用 | MIT 许可证",
                "credit": "鸣谢: Meiji ღ",
                "support_msg": "请我吃点心，在这里支持我：",
                "log_load_model": "正在加载 Whisper 模型 ({})... 请稍候。",
                "log_model_loaded": "Whisper 模型加载完成！",
                "log_start_mic": "已启动输出麦克风: {}",
                "log_auto_listen": "正在聆听 (自动)...",
                "log_recording": "正在录音...",
                "log_out_stop": "输出已停止。",
                "log_start_loop": "已启动输入环回: {}",
                "log_speaker_listen": "正在聆听扬声器...",
                "log_in_stop": "输入已停止。",
                "log_mute_paused": "VRC Mute Sync: 麦克风已静音 (已暂停)",
                "log_mute_resumed": "VRC Mute Sync: 麦克风已取消静音 (已恢复)",
                "sec_general": "常规设置",
                "sec_api": "AI & 翻译引擎配置",
                "sec_hotkey": "快捷键",
                "engine_lbl": "翻译引擎:",
                "device_lbl": "AI 处理设备:",
                "device_info": "GPU 需要 NVIDIA 和 CUDA。CPU 较慢，但适用于 AMD/Intel 电脑。",
                                "model_lbl": "Whisper 模型:",
                "btn_clear_cache": "清除缓存",
                "nav_docs": "文档",
                "confirm_download_title": "需要下载",
                "confirm_download_msg": "此模型 ({}) 尚未下载。\n下载大小: 约 {}\n要继续吗？",
                "confirm_clear_title": "清除缓存",
                "confirm_clear_msg": "您确定要删除所有未使用的模型吗？",
                "downloading_model_title": "正在下载模型",
                "downloading_model_msg": "正在下载 {} 模型: {}%",
                "cache_cleared_msg": "未使用的模型已删除。",
                "model_info_tiny": "大小: ~75 MB | 内存: ~1 GB | 准确度: 低 — 速度快，适合简单/短语",
                "model_info_base": "大小: ~145 MB | 内存: ~1 GB | 准确度: 一般 — 适合日常使用",
                "model_info_small": "大小: ~484 MB | 内存: ~2 GB | 准确度: 良好 — 推荐大多数用户使用",
                "model_info_medium": "大小: ~1.5 GB | 内存: ~5 GB | 准确度: 高 — 适合清晰音频 (默认)",
                "model_info_large": "大小: ~3.1 GB | 内存: ~10 GB | 准确度: 非常高 — 最佳质量，需要强大GPU",

                "hk_out_lbl": "开始输出:",
                "hk_in_lbl": "开始输入:",
                "hk_push_lbl": "按住说话:",
                "warn_same_lang": "源语言和目标语言不能相同。",
                "warn_same_lang_lock": "已选择相同语言。在更改语言之前，开始按钮将被锁定。",
                "warn_osc_forgot": "未在默认端口 (9000) 上检测到 VRChat OSC。\n如果您使用其他端口，请忽略此消息。\n(仍将继续启动...)",
                "err_cuda_not_found": "CUDA/GPU 错误: 未找到兼容的 NVIDIA GPU。\n👉 如果使用 AMD/Intel，请在设置中将“AI 处理设备”更改为 CPU。\n👉 如果使用 NVIDIA，请安装 CUDA 12.x: https://developer.nvidia.com/cuda-12-9-1-download-archive",
                "err_api_limit": "API 限制: 请求过多，请稍后再试。",
                "err_api_invalid": "API 错误: 密钥无效，请检查设置。",
                "err_api_empty": "❌ 开始之前，请在设置选项卡中输入您的 API 密钥。",
                "alert_cuda": "CUDA/GPU 错误\n\n未在您的系统中找到兼容的 NVIDIA GPU。\n\n• 如果使用 AMD 或 Intel，请前往设置将'AI 处理设备'更改为 CPU。\n• 如果使用 NVIDIA，请下载并安装 CUDA Toolkit 12.x：\nhttps://developer.nvidia.com/cuda-12-9-1-download-archive\n\n系统已停止。",
                "alert_api_limit": "API 请求频率限制\n\n已超过 API 请求限制。使用免费密钥时经常会发生这种情况。\n\n请稍等片刻后重试，或者考虑升级到付费 API 方案以获得不间断的使用体验。\n\n系统已停止。",
                "alert_api_invalid": "API 密钥无效\n\n您的 API 密钥已被服务器拒绝。请前往设置检查您的密钥是否正确。\n\n系统已停止。",
                "alert_whisper_error": "语音识别错误\n\nWhisper 模型加载失败: {}\n\n系统已停止。",
                "alert_api_generic": "翻译错误\n\n发生意外错误: {}\n\n系统已停止。",
                "adv_audio_lbl": "⚙️ 高级音频设置",
                "silence_timeout_lbl": "静音超时 (等待说话结束):",
                "max_record_time_lbl": "单次最大录音时间:",
                "beam_size_lbl": "AI 准确度与速度 (Beam Size):",
                "update_title": "有可用更新",
                "update_msg": "新版本 (v{}) 已发布！您当前使用的是 v{}。\n\n您想现在自动下载并安装吗？",
                "btn_update_avail": "更新至 v{}",
                "update_downloading_title": "正在下载更新",
                "update_downloading_msg": "正在下载 v{}...\n请稍候，应用将自动重启。"
            },
            "ko": {
                "nav_trans": "번역 메인",
                "nav_audio": "오디오 설정",
                "nav_settings": "설정",
                "ui_lang": "UI 언어:",
                "api_key": "API 키:",
                "btn_save": "저장",
                "btn_edit": "편집",
                "osc_status": "OSC 상태: ",
                "osc_detected": "🟢 감지됨",
                "osc_not_detected": "🔴 감지되지 않음",
                "left_frame": "송신 시스템 (음성 -> VRChat)",
                "right_frame": "수신 시스템 (음성 번역)",
                "mic_out": "마이크 선택 (내 목소리):",
                "src_lang_out": "출발어:",
                "tgt_lang_out": "도착어:",
                "mode_auto": "자동 (연속)",
                "mode_push": "눌러서 녹음",
                "btn_start_out": "송신 시작",
                "btn_stop_out": "송신 중지",
                "btn_hold": "누른 채로 말하기",
                "btn_loading_model": "⏳ 모델 로딩 중...",
                "manual_label": "수동 번역 (입력 및 전송):",
                "btn_send": "전송",
                "log_out": "송신 로그:",
                "speaker_in": "스피커 선택 (가상 오디오):",
                "src_lang_in": "수신 언어:",
                "tgt_lang_in": "도착어:",
                "btn_start_in": "수신 시작",
                "btn_stop_in": "수신 중지",
                "log_in": "수신 로그 (VRChat으로 전송되지 않음):",
                "warn_manual": "수동 텍스트를 전송하기 전에 송신(Outgoing) 시스템을 시작하십시오.",
                "theme_title": "테마 설정:",
                "theme_dark": "다크 모드",
                "telemetry_lbl": "익명 크래시 보고서를 공유하여 SyncVRC 개선에 참여 (음성/텍스트 데이터 수집 안 함)",
                "mute_sync_lbl": "VRC Mute Sync 활성화 (VRChat에서 음소거 시 번역 일시 중지)",
                "license": "비상업적 용도로만 무료 사용 가능 | MIT 라이선스",
                "credit": "크레딧: Meiji ღ",
                "support_msg": "여기서 저를 후원하여 간식을 사주세요:",
                "log_load_model": "Whisper 모델 ({}) 로드 중... 잠시만 기다려주세요.",
                "log_model_loaded": "Whisper 모델 로드 완료!",
                "log_start_mic": "송신 마이크 시작됨: {}",
                "log_auto_listen": "듣는 중 (자동)...",
                "log_recording": "녹음 중...",
                "log_out_stop": "송신이 중지되었습니다.",
                "log_start_loop": "수신 루프백 시작됨: {}",
                "log_speaker_listen": "스피커 듣는 중...",
                "log_in_stop": "수신이 중지되었습니다.",
                "log_mute_paused": "VRC Mute Sync: 마이크가 음소거되었습니다 (일시 중지됨)",
                "log_mute_resumed": "VRC Mute Sync: 마이크 음소거가 해제되었습니다 (재개됨)",
                "sec_general": "일반 설정",
                "sec_api": "AI 및 번역 엔진 구성",
                "sec_hotkey": "단축키 설정",
                "engine_lbl": "번역 엔진:",
                "device_lbl": "AI 처리 장치:",
                "device_info": "GPU는 NVIDIA 및 CUDA가 필요합니다. CPU는 AMD/Intel에서 작동하지만 느립니다.",
                                "model_lbl": "Whisper 모델:",
                "btn_clear_cache": "캐시 지우기",
                "nav_docs": "문서",
                "confirm_download_title": "다운로드 필요",
                "confirm_download_msg": "이 모델({})은 아직 다운로드되지 않았습니다.\n다운로드 크기: 약 {}\n계속하시겠습니까?",
                "confirm_clear_title": "캐시 지우기",
                "confirm_clear_msg": "사용하지 않는 모든 모델을 삭제하시겠습니까?",
                "downloading_model_title": "모델 다운로드 중",
                "downloading_model_msg": "{} 모델 다운로드 중: {}%",
                "cache_cleared_msg": "사용하지 않는 모델이 제거되었습니다.",
                "model_info_tiny": "크기: ~75 MB | RAM: ~1 GB | 정확도: 낮음 — 빠름, 짧은 문장에 적합",
                "model_info_base": "크기: ~145 MB | RAM: ~1 GB | 정확도: 보통 — 일상적인 사용에 적합",
                "model_info_small": "크기: ~484 MB | RAM: ~2 GB | 정확도: 양호 — 대부분의 사용자에게 권장",
                "model_info_medium": "크기: ~1.5 GB | RAM: ~5 GB | 정확도: 높음 — 깨끗한 오디오에 최적 (기본값)",
                "model_info_large": "크기: ~3.1 GB | RAM: ~10 GB | 정확도: 매우 높음 — 최상의 품질, 강력한 GPU 필요",

                "hk_out_lbl": "송신 시작:",
                "hk_in_lbl": "수신 시작:",
                "hk_push_lbl": "누른 채로 말하기:",
                "warn_same_lang": "출발어와 도착어를 같게 설정할 수 없습니다.",
                "warn_same_lang_lock": "같은 언어가 선택되었습니다. 언어를 변경할 때까지 시작 버튼이 잠깁니다.",
                "warn_osc_forgot": "기본 포트(9000)에서 VRChat OSC가 감지되지 않았습니다.\n다른 포트를 사용하는 경우 무시하셔도 됩니다.\n(그래도 시작합니다...)",
                "err_cuda_not_found": "CUDA/GPU 오류: 호환되는 NVIDIA GPU를 찾을 수 없습니다.\n👉 AMD/Intel을 사용하는 경우 설정에서 'AI 디바이스'를 CPU로 변경하십시오.\n👉 NVIDIA를 사용하는 경우 CUDA 고설치하십시오: https://developer.nvidia.com/cuda-12-9-1-download-archive",
                "err_api_limit": "API 한도 초과: 요청이 너무 많습니다. 잠시 기다려 주십시오.",
                "err_api_invalid": "API 오류: 잘못된 API 키입니다. 설정에서 키를 확인하십시오.",
                "err_api_empty": "❌ 시작하기 전에 설정 탭에서 API 키를 입력하십시오.",
                "alert_cuda": "CUDA/GPU 오류\n\n시스템에서 호환되는 NVIDIA GPU를 찾을 수 없습니다.\n\n• AMD 또는 Intel을 사용하는 경우 설정에서 'AI 디바이스'를 CPU로 변경하세요.\n• NVIDIA를 사용하는 경우 CUDA Toolkit 12.x를 다운로드하여 설치하세요:\nhttps://developer.nvidia.com/cuda-12-9-1-download-archive\n\n시스템이 중지되었습니다.",
                "alert_api_limit": "API 요청 한도 초과\n\nAPI 요청 한도를 초과했습니다. 무료 등급 키에서 자주 발생합니다.\n\n잠시 기다린 후 다시 시도하거나, 유료 API 요금제로 업그레이드를 고려해 주세요.\n\n시스템이 중지되었습니다.",
                "alert_api_invalid": "잘못된 API 키\n\nAPI 키가 서버에서 거부되었습니다. 설정에서 키가 올바른지 확인하세요.\n\n시스템이 중지되었습니다.",
                "alert_whisper_error": "음성 인식 오류\n\nWhisper 모델 로드에 실패했습니다: {}\n\n시스템이 중지되었습니다.",
                "alert_api_generic": "번역 오류\n\n예상치 못한 오류가 발생했습니다: {}\n\n시스템이 중지되었습니다.",
                "adv_audio_lbl": "⚙️ 고급 오디오 설정",
                "silence_timeout_lbl": "무음 시간 초과 (말하기 종료 대기):",
                "max_record_time_lbl": "1회 최대 녹음 시간:",
                "beam_size_lbl": "AI 정확도 및 속도 (Beam Size):",
                "update_title": "업데이트 가능",
                "update_msg": "새 버전(v{})을 사용할 수 있습니다! 현재 버전은 v{}입니다.\n\n지금 자동으로 다운로드하여 설치하시겠습니까?",
                "btn_update_avail": "v{} 업데이트",
                "update_downloading_title": "업데이트 다운로드 중",
                "update_downloading_msg": "v{} 다운로드 중...\n잠시만 기다려주세요. 앱이 자동으로 다시 시작됩니다."
            }
        }

    def get_t(self, key):
        code = self.lang_map.get(self.current_ui_lang, "en")
        return self.translations.get(code, self.translations["en"]).get(key, "")

    def setup_ctrl_a(self, widget, is_entry=True):
        def _select_all_entry(event):
            event.widget.select_range(0, 'end')
            event.widget.icursor('end')
            return "break"

        def _select_all_textbox(event):
            event.widget.tag_add("sel", "1.0", "end")
            return "break"

        def _copy_entry(event):
            try:
                event.widget.event_generate("<<Copy>>")
            except: pass
            return "break"

        def _paste_entry(event):
            try:
                event.widget.event_generate("<<Paste>>")
            except: pass
            return "break"
        
        def _on_key_entry(event):
            # Check for Ctrl held (state bit 0x4) and match keycode for A(65), C(67), V(86)
            if event.state & 0x4:
                if event.keycode == 65:  # A
                    return _select_all_entry(event)
                elif event.keycode == 67:  # C
                    return _copy_entry(event)
                elif event.keycode == 86:  # V
                    return _paste_entry(event)

        def _on_key_textbox(event):
            if event.state & 0x4:
                if event.keycode == 65:  # A
                    return _select_all_textbox(event)
                elif event.keycode == 67:  # C
                    return _copy_entry(event)
                elif event.keycode == 86:  # V
                    return _paste_entry(event)
            
        inner_widget = widget._entry if is_entry else widget._textbox
        if is_entry:
            inner_widget.bind("<Control-a>", _select_all_entry)
            inner_widget.bind("<Control-A>", _select_all_entry)
            inner_widget.bind("<KeyPress>", _on_key_entry)
        else:
            inner_widget.bind("<Control-a>", _select_all_textbox)
            inner_widget.bind("<Control-A>", _select_all_textbox)
            inner_widget.bind("<KeyPress>", _on_key_textbox)

    def update_settings_state(self):
        any_running = self.is_running_out or self.is_running_in
        state = "disabled" if any_running else "normal"
        text_color = "gray" if any_running else ("gray10", "gray90")
        
        self.trans_engine_combo.configure(state=state)
        self.ai_device_combo.configure(state=state)
        
        self.lbl_sec_api.configure(text_color=text_color)
        self.lbl_engine.configure(text_color=text_color)
        self.lbl_api_key.configure(text_color=text_color)
        self.lbl_device.configure(text_color=text_color)
        self.lbl_device_info.configure(text_color=text_color)
        if hasattr(self, 'lbl_model'):
            self.lbl_model.configure(text_color=text_color)
            self.whisper_model_combo.configure(state=state)
            self.btn_clear_cache.configure(state=state)
        
        if any_running:
            self.api_key_entry.configure(state="disabled", fg_color=("gray85", "gray25"))
            self.btn_api_action.configure(state="disabled")
        else:
            self.btn_api_action.configure(state="normal")
            current_key = self.api_keys.get(self.trans_engine_val, "").strip()
            if current_key and self.btn_api_action.cget("text") == self.get_t("btn_edit"):
                self.api_key_entry.configure(state="disabled", show="*", fg_color=("gray85", "gray25"))
            else:
                default_entry_color = ctk.ThemeManager.theme["CTkEntry"]["fg_color"]
                self.api_key_entry.configure(state="normal", show="", fg_color=default_entry_color)

    def setup_ui(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # ================= SIDEBAR =================
        self.sidebar_frame = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        # --- สร้าง Frame จัดกลุ่ม Logo + Text ---
        self.header_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.header_frame.pack(padx=20, pady=(30, 20), anchor="w", fill="x")

        # โหลดรูป Icon (บังคับใช้ไฟล์ชื่อ icon.png)
        try:
            app_icon = ctk.CTkImage(light_image=Image.open("icon.png"), size=(42, 42))
            self.lbl_icon = ctk.CTkLabel(self.header_frame, text="", image=app_icon)
            self.lbl_icon.pack(side="left", padx=(0, 10))
        except Exception:
            pass 

        # กลุ่ม Text (ชื่อแอป + เวอร์ชัน)
        self.header_text_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.header_text_frame.pack(side="left", fill="both")

        self.lbl_app_title = ctk.CTkLabel(self.header_text_frame, text="SyncVRC", font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_app_title.pack(anchor="w", pady=(0, 0))

        self.lbl_app_version = ctk.CTkLabel(self.header_text_frame, text=f"v{self.app_version}", font=ctk.CTkFont(size=12, weight="bold"), text_color="gray")
        self.lbl_app_version.pack(anchor="w", pady=(0, 0))

        # ----------------------------------------

        self.btn_nav_trans = NavItem(self.sidebar_frame, text_var=self.get_t("nav_trans"), command=lambda: self.select_frame("trans"))
        self.btn_nav_trans.pack(fill="x", pady=2)

        self.btn_nav_audio = NavItem(self.sidebar_frame, text_var=self.get_t("nav_audio"), command=lambda: self.select_frame("audio"))
        self.btn_nav_audio.pack(fill="x", pady=2)

        self.btn_nav_settings = NavItem(self.sidebar_frame, text_var=self.get_t("nav_settings"), command=lambda: self.select_frame("settings"))
        self.btn_nav_settings.pack(fill="x", pady=2)

        self.btn_nav_docs = NavItem(self.sidebar_frame, text_var=self.get_t("nav_docs") + " ↗", command=lambda: webbrowser.open("https://finalsiren1.github.io/SyncVRC/"), hover_color=("#e2e8f0", "#334155"))
        self.btn_nav_docs.pack(fill="x", pady=(20, 2))

        # จุดสำหรับวางปุ่ม Update เมื่อปฏิเสธ Pop-up
        self.update_btn_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.update_btn_frame.pack(fill="x", pady=10, padx=15)
        self.btn_nav_update = ctk.CTkButton(self.update_btn_frame, text="", fg_color="#ff9800", text_color="black", hover_color="#e68a00", font=ctk.CTkFont(weight="bold"), command=self.start_update_process)

        spacer = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        spacer.pack(fill="both", expand=True)

        self.lbl_osc_status_text = ctk.CTkLabel(self.sidebar_frame, font=ctk.CTkFont(weight="bold", size=12))
        self.lbl_osc_status_text.pack(padx=20, pady=(0, 0), anchor="w")
        
        self.lbl_osc_indicator = ctk.CTkLabel(self.sidebar_frame, font=ctk.CTkFont(weight="bold", size=12))
        self.lbl_osc_indicator.pack(padx=20, pady=(0, 20), anchor="w")

        # ================= MAIN CONTENT =================
        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.frame_trans = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frame_audio = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frame_settings = ctk.CTkFrame(self.main_container, fg_color="transparent")

        for frame in (self.frame_trans, self.frame_audio, self.frame_settings):
            frame.grid(row=0, column=0, sticky="nsew")

        self.build_trans_frame()
        self.build_audio_frame()
        self.build_settings_frame()
        self.build_footer()

        self.select_frame("trans")

    def select_frame(self, name):
        self.btn_nav_trans.set_active(name == "trans")
        self.btn_nav_audio.set_active(name == "audio")
        self.btn_nav_settings.set_active(name == "settings")

        if name == "trans": self.frame_trans.tkraise()
        elif name == "audio": self.frame_audio.tkraise()
        elif name == "settings": self.frame_settings.tkraise()

    def build_trans_frame(self):
        langs = ["English", "Japanese", "Chinese", "Korean", "Spanish", "Russian", "French", "German", "Portuguese", "Thai"]
        self.frame_trans.columnconfigure(0, weight=1)
        self.frame_trans.columnconfigure(1, weight=1)
        self.frame_trans.rowconfigure(0, weight=1)

        # --- Left: Outgoing ---
        left_panel = ctk.CTkFrame(self.frame_trans)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.lbl_left_title = ctk.CTkLabel(left_panel, font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_left_title.pack(anchor="w", pady=(15,10), padx=20)

        grid_frame_out = ctk.CTkFrame(left_panel, fg_color="transparent")
        grid_frame_out.pack(fill="x", padx=20, pady=5)
        grid_frame_out.columnconfigure(1, weight=1)
        grid_frame_out.columnconfigure(3, weight=1)

        self.lbl_src_out = ctk.CTkLabel(grid_frame_out)
        self.lbl_src_out.grid(row=0, column=0, sticky="w", pady=5)
        self.src_lang_out = ctk.CTkOptionMenu(grid_frame_out, values=langs, width=120, command=self.on_out_lang_change)
        self.src_lang_out.set(self.out_src_val)
        self.src_lang_out.grid(row=0, column=1, sticky="w", padx=(10, 20), pady=5)

        self.lbl_tgt_out = ctk.CTkLabel(grid_frame_out)
        self.lbl_tgt_out.grid(row=0, column=2, sticky="w", pady=5)
        self.tgt_lang_out = ctk.CTkOptionMenu(grid_frame_out, values=langs, width=120, command=self.on_out_lang_change)
        self.tgt_lang_out.set(self.out_tgt_val)
        self.tgt_lang_out.grid(row=0, column=3, sticky="w", padx=(10, 0), pady=5)

        self.mode_var_out = tk.StringVar(value="auto")
        mode_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        mode_frame.pack(fill="x", padx=20, pady=(10, 15))
        self.radio_auto = ctk.CTkRadioButton(mode_frame, variable=self.mode_var_out, value="auto", command=self.on_mode_change_out)
        self.radio_auto.pack(side="left")
        self.radio_push = ctk.CTkRadioButton(mode_frame, variable=self.mode_var_out, value="push", command=self.on_mode_change_out)
        self.radio_push.pack(side="left", padx=20)

        btn_frame_out = ctk.CTkFrame(left_panel, fg_color="transparent")
        btn_frame_out.pack(padx=20, pady=(0, 15), anchor="w")
        self.start_btn_out = ctk.CTkButton(btn_frame_out, width=160, height=40, font=ctk.CTkFont(weight="bold"), fg_color="#28a745", hover_color="#218838", command=self.toggle_out_thread)
        self.start_btn_out.pack(side="left")
        
        self.push_btn_out = ctk.CTkButton(btn_frame_out, width=160, height=40, font=ctk.CTkFont(weight="bold"), fg_color="#007bff", hover_color="#0069d9", state="disabled")
        self.push_btn_out.pack(side="left", padx=(10, 0))
        self.push_btn_out.bind("<ButtonPress-1>", self.start_push_record)
        self.push_btn_out.bind("<ButtonRelease-1>", self.stop_push_record)

        self.lbl_manual = ctk.CTkLabel(left_panel)
        self.lbl_manual.pack(anchor="w", padx=20)
        text_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        text_frame.pack(fill="x", padx=20, pady=(0, 15))
        self.manual_entry = ctk.CTkEntry(text_frame)
        self.manual_entry.pack(side="left", expand=True, fill="x")
        self.manual_entry.bind("<Return>", lambda event: self.send_manual_text())
        self.setup_ctrl_a(self.manual_entry, is_entry=True)
        
        self.btn_send = ctk.CTkButton(text_frame, width=60, command=self.send_manual_text)
        self.btn_send.pack(side="left", padx=(5,0))

        self.lbl_log_out = ctk.CTkLabel(left_panel)
        self.lbl_log_out.pack(anchor="w", padx=20)
        self.log_area_out = ctk.CTkTextbox(left_panel, state="disabled", font=ctk.CTkFont(family="Consolas", size=12))
        self.log_area_out.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.setup_ctrl_a(self.log_area_out, is_entry=False)

        # --- Right: Incoming ---
        right_panel = ctk.CTkFrame(self.frame_trans)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        self.lbl_right_title = ctk.CTkLabel(right_panel, font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_right_title.pack(anchor="w", pady=(15,10), padx=20)

        grid_frame_in = ctk.CTkFrame(right_panel, fg_color="transparent")
        grid_frame_in.pack(fill="x", padx=20, pady=5)
        grid_frame_in.columnconfigure(1, weight=1)
        grid_frame_in.columnconfigure(3, weight=1)

        self.lbl_src_in = ctk.CTkLabel(grid_frame_in)
        self.lbl_src_in.grid(row=0, column=0, sticky="w", pady=5)
        self.src_lang_in = ctk.CTkOptionMenu(grid_frame_in, values=langs, width=120, command=self.on_in_lang_change)
        self.src_lang_in.set(self.in_src_val)
        self.src_lang_in.grid(row=0, column=1, sticky="w", padx=(10, 20), pady=5)

        self.lbl_tgt_in = ctk.CTkLabel(grid_frame_in)
        self.lbl_tgt_in.grid(row=0, column=2, sticky="w", pady=5)
        self.tgt_lang_in = ctk.CTkOptionMenu(grid_frame_in, values=langs, width=120, command=self.on_in_lang_change)
        self.tgt_lang_in.set(self.in_tgt_val)
        self.tgt_lang_in.grid(row=0, column=3, sticky="w", padx=(10, 0), pady=5)

        btn_frame_in = ctk.CTkFrame(right_panel, fg_color="transparent")
        btn_frame_in.pack(padx=20, pady=(10, 15), anchor="w")
        self.start_btn_in = ctk.CTkButton(btn_frame_in, width=160, height=40, font=ctk.CTkFont(weight="bold"), fg_color="#28a745", hover_color="#218838", command=self.toggle_in_thread)
        self.start_btn_in.pack(side="left")

        self.lbl_log_in = ctk.CTkLabel(right_panel)
        self.lbl_log_in.pack(anchor="w", padx=20)
        self.log_area_in = ctk.CTkTextbox(right_panel, state="disabled", font=ctk.CTkFont(family="Consolas", size=12))
        self.log_area_in.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.setup_ctrl_a(self.log_area_in, is_entry=False)

    def build_audio_frame(self):
        panel = ctk.CTkFrame(self.frame_audio)
        panel.pack(fill="both", expand=True)

        lbl_title = ctk.CTkLabel(panel, text="Audio Device Setup", font=ctk.CTkFont(size=18, weight="bold"))
        lbl_title.grid(row=0, column=0, sticky="w", pady=(20, 10), padx=30)

        self.lbl_mic_out = ctk.CTkLabel(panel, font=ctk.CTkFont(weight="bold"))
        self.lbl_mic_out.grid(row=1, column=0, sticky="w", padx=30, pady=(5, 5))
        self.mic_combo_out = ctk.CTkOptionMenu(panel, values=self.input_mic_names, width=500, command=lambda e: self.save_all_settings())
        if self.input_mic_names: self.mic_combo_out.set(self.input_mic_names[0])
        self.mic_combo_out.grid(row=2, column=0, sticky="w", padx=30, pady=(0, 15))

        self.lbl_speaker_in = ctk.CTkLabel(panel, font=ctk.CTkFont(weight="bold"))
        self.lbl_speaker_in.grid(row=3, column=0, sticky="w", padx=30, pady=(5, 5))
        self.mic_combo_in = ctk.CTkOptionMenu(panel, values=self.speaker_names, width=500, command=lambda e: self.save_all_settings())
        if self.speaker_names: self.mic_combo_in.set(self.speaker_names[0])
        self.mic_combo_in.grid(row=4, column=0, sticky="w", padx=30, pady=(0, 15))
        
        self.chk_mute_sync = ctk.CTkCheckBox(panel, text=self.get_t("mute_sync_lbl"), variable=self.enable_mute_sync_var, command=self.save_all_settings)
        self.chk_mute_sync.grid(row=5, column=0, sticky="w", padx=30, pady=(0, 10))

        ctk.CTkFrame(panel, height=2, fg_color=("gray85", "gray30")).grid(row=6, column=0, sticky="ew", padx=30, pady=15)

        # --- Advanced Audio Settings ---
        self.lbl_adv_audio = ctk.CTkLabel(panel, font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_adv_audio.grid(row=7, column=0, sticky="w", padx=30, pady=(5, 10))

        # 1. Silence Timeout
        frame_silence = ctk.CTkFrame(panel, fg_color="transparent")
        frame_silence.grid(row=8, column=0, sticky="ew", padx=30, pady=5)
        self.lbl_silence = ctk.CTkLabel(frame_silence, width=220, anchor="w")
        self.lbl_silence.pack(side="left")
        self.slider_silence = ctk.CTkSlider(frame_silence, from_=0.3, to=2.0, number_of_steps=17, command=self.update_silence_lbl)
        self.slider_silence.pack(side="left", padx=10)
        self.lbl_silence_val = ctk.CTkLabel(frame_silence, width=40, text=f"{self.silence_timeout_val:.1f}s")
        self.lbl_silence_val.pack(side="left")

        # 2. Max Record Time
        frame_max_rec = ctk.CTkFrame(panel, fg_color="transparent")
        frame_max_rec.grid(row=9, column=0, sticky="ew", padx=30, pady=5)
        self.lbl_max_rec = ctk.CTkLabel(frame_max_rec, width=220, anchor="w")
        self.lbl_max_rec.pack(side="left")
        self.slider_max_rec = ctk.CTkSlider(frame_max_rec, from_=5, to=30, number_of_steps=25, command=self.update_max_rec_lbl)
        self.slider_max_rec.pack(side="left", padx=10)
        self.lbl_max_rec_val = ctk.CTkLabel(frame_max_rec, width=40, text=f"{int(self.max_record_time_val)}s")
        self.lbl_max_rec_val.pack(side="left")

        # 3. Beam Size
        frame_beam = ctk.CTkFrame(panel, fg_color="transparent")
        frame_beam.grid(row=10, column=0, sticky="ew", padx=30, pady=5)
        self.lbl_beam = ctk.CTkLabel(frame_beam, width=220, anchor="w")
        self.lbl_beam.pack(side="left")
        self.slider_beam = ctk.CTkSlider(frame_beam, from_=1, to=5, number_of_steps=4, command=self.update_beam_lbl)
        self.slider_beam.pack(side="left", padx=10)
        self.lbl_beam_val = ctk.CTkLabel(frame_beam, width=40, text=f"{int(self.beam_size_val)}")
        self.lbl_beam_val.pack(side="left")

    def update_silence_lbl(self, val):
        self.silence_timeout_val = float(val)
        self.lbl_silence_val.configure(text=f"{self.silence_timeout_val:.1f}s")
        self.save_all_settings()

    def update_max_rec_lbl(self, val):
        self.max_record_time_val = int(val)
        self.lbl_max_rec_val.configure(text=f"{self.max_record_time_val}s")
        self.save_all_settings()

    def update_beam_lbl(self, val):
        self.beam_size_val = int(val)
        self.lbl_beam_val.configure(text=f"{self.beam_size_val}")
        self.save_all_settings()

    def build_settings_frame(self):
        panel = ctk.CTkFrame(self.frame_settings)
        panel.pack(fill="both", expand=True)

        # --- Section 1: General ---
        self.lbl_sec_general = ctk.CTkLabel(panel, font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_sec_general.grid(row=0, column=0, columnspan=3, sticky="w", padx=30, pady=(20, 10))

        self.lbl_ui_lang = ctk.CTkLabel(panel, width=160, anchor="w")
        self.lbl_ui_lang.grid(row=1, column=0, sticky="w", padx=30, pady=5)
        self.ui_lang_combo = ctk.CTkOptionMenu(panel, values=list(self.lang_map.keys()), width=200, command=self.change_ui_language)
        self.ui_lang_combo.set(self.current_ui_lang)
        self.ui_lang_combo.grid(row=1, column=1, sticky="w", pady=5)

        self.lbl_theme_title = ctk.CTkLabel(panel, width=160, anchor="w")
        self.lbl_theme_title.grid(row=2, column=0, sticky="w", padx=30, pady=5)
        self.switch_theme = ctk.CTkSwitch(panel, command=self.toggle_theme, onvalue=True, offvalue=False)
        self.switch_theme.grid(row=2, column=1, sticky="w", pady=5)
        if self.is_dark_mode: self.switch_theme.select()
        
        self.chk_telemetry = ctk.CTkCheckBox(panel, text=self.get_t("telemetry_lbl"), variable=self.enable_telemetry_var, command=self.save_all_settings)
        self.chk_telemetry.grid(row=3, column=1, columnspan=2, sticky="w", pady=(5, 5))

        ctk.CTkFrame(panel, height=2, fg_color=("gray85", "gray30")).grid(row=4, column=0, columnspan=3, sticky="ew", padx=30, pady=20)

        # --- Section 2: API & Engine ---
        self.lbl_sec_api = ctk.CTkLabel(panel, font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_sec_api.grid(row=5, column=0, columnspan=3, sticky="w", padx=30, pady=(0, 10))

        self.lbl_engine = ctk.CTkLabel(panel, width=160, anchor="w")
        self.lbl_engine.grid(row=6, column=0, sticky="w", padx=30, pady=5)
        engines = ["Google Gemini", "DeepL API", "OpenAI"]
        self.trans_engine_combo = ctk.CTkOptionMenu(panel, values=engines, width=200, command=self.on_engine_change)
        self.trans_engine_combo.set(self.trans_engine_val)
        self.trans_engine_combo.grid(row=6, column=1, sticky="w", pady=5)

        self.lbl_api_key = ctk.CTkLabel(panel, width=160, anchor="w")
        self.lbl_api_key.grid(row=7, column=0, sticky="w", padx=30, pady=5)
        self.api_key_var = tk.StringVar()
        self.api_key_entry = ctk.CTkEntry(panel, width=350, textvariable=self.api_key_var) 
        self.api_key_entry.grid(row=7, column=1, sticky="w", pady=5)
        self.api_key_entry.bind("<FocusOut>", lambda e: self.save_all_settings())
        self.setup_ctrl_a(self.api_key_entry, is_entry=True)
        self.btn_api_action = ctk.CTkButton(panel, width=80, command=self.toggle_api_edit)
        self.btn_api_action.grid(row=7, column=2, sticky="w", padx=(10, 0), pady=5)

        self.lbl_device = ctk.CTkLabel(panel, width=160, anchor="w")
        self.lbl_device.grid(row=8, column=0, sticky="w", padx=30, pady=(15, 5))
        devices = ["GPU (NVIDIA)", "CPU (Fallback)"]
        self.ai_device_combo = ctk.CTkOptionMenu(panel, values=devices, width=200, command=lambda e: self.save_all_settings())
        self.ai_device_combo.set(self.ai_device_val)
        self.ai_device_combo.grid(row=8, column=1, sticky="w", pady=(15, 5))
        
        self.lbl_device_info = ctk.CTkLabel(panel, text_color="gray", font=ctk.CTkFont(size=11))
        self.lbl_device_info.grid(row=9, column=1, columnspan=2, sticky="w", pady=(0, 5))

        self.lbl_model = ctk.CTkLabel(panel, width=160, anchor="w")
        self.lbl_model.grid(row=10, column=0, sticky="w", padx=30, pady=5)
        
        self.whisper_model_combo = ctk.CTkOptionMenu(panel, width=200, command=self.on_model_change)
        self.whisper_model_combo.grid(row=10, column=1, sticky="w", pady=5)
        self.update_model_dropdown()
        
        self.btn_clear_cache = ctk.CTkButton(panel, width=120, command=self.clear_model_cache, fg_color="#dc3545", hover_color="#c82333")
        self.btn_clear_cache.grid(row=10, column=2, sticky="w", padx=(10, 0), pady=5)

        self.lbl_model_info = ctk.CTkLabel(panel, text="", text_color="gray", font=ctk.CTkFont(size=11), wraplength=500, justify="left")
        self.lbl_model_info.grid(row=11, column=1, columnspan=2, sticky="w", pady=(0, 5))
        self.update_model_info_label()

        ctk.CTkFrame(panel, height=2, fg_color=("gray85", "gray30")).grid(row=12, column=0, columnspan=3, sticky="ew", padx=30, pady=20)

        # --- Section 3: Hotkeys ---
        self.lbl_sec_hotkey = ctk.CTkLabel(panel, font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_sec_hotkey.grid(row=13, column=0, columnspan=3, sticky="w", padx=30, pady=(0, 10))

        keys = ["None", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "Insert", "Delete", "Home", "End", "PageUp", "PageDown", "Pause"]
        
        self.lbl_hk_out_set = ctk.CTkLabel(panel, width=160, anchor="w")
        self.lbl_hk_out_set.grid(row=14, column=0, sticky="w", padx=30, pady=5)
        self.cmb_hk_out = ctk.CTkOptionMenu(panel, values=keys, width=200, command=self.on_hotkey_change)
        self.cmb_hk_out.set(self.hk_out)
        self.cmb_hk_out.grid(row=14, column=1, sticky="w", pady=5)

        self.lbl_hk_in_set = ctk.CTkLabel(panel, width=160, anchor="w")
        self.lbl_hk_in_set.grid(row=15, column=0, sticky="w", padx=30, pady=5)
        self.cmb_hk_in = ctk.CTkOptionMenu(panel, values=keys, width=200, command=self.on_hotkey_change)
        self.cmb_hk_in.set(self.hk_in)
        self.cmb_hk_in.grid(row=15, column=1, sticky="w", pady=5)

        self.lbl_hk_push_set = ctk.CTkLabel(panel, width=160, anchor="w")
        self.lbl_hk_push_set.grid(row=16, column=0, sticky="w", padx=30, pady=5)
        self.cmb_hk_push = ctk.CTkOptionMenu(panel, values=keys, width=200, command=self.on_hotkey_change)
        self.cmb_hk_push.set(self.hk_push)
        self.cmb_hk_push.grid(row=16, column=1, sticky="w", pady=5)

    def build_footer(self):
        footer_frame = ctk.CTkFrame(self.root, fg_color="transparent", height=40)
        footer_frame.grid(row=1, column=1, sticky="ew", padx=20, pady=(0,10))
        
        self.lbl_support = ctk.CTkLabel(footer_frame, text_color="gray")
        self.lbl_support.pack(side="left", padx=(0, 5))
        
        self.btn_kofi = ctk.CTkButton(footer_frame, text="Ko-fi", width=70, height=24, fg_color="#F16061", hover_color="#D14041", command=lambda: webbrowser.open("https://ko-fi.com/meijivrc"))
        self.btn_kofi.pack(side="left", padx=2)
        
        self.btn_patreon = ctk.CTkButton(footer_frame, text="Patreon", width=70, height=24, fg_color="#F96854", hover_color="#D94834", command=lambda: webbrowser.open("https://www.patreon.com/meijino"))
        self.btn_patreon.pack(side="left", padx=2)

        self.lbl_license = ctk.CTkLabel(footer_frame, text_color="gray", font=ctk.CTkFont(size=11))
        self.lbl_license.pack(side="right")

        self.lbl_credit = ctk.CTkLabel(footer_frame, text_color="gray", font=ctk.CTkFont(size=11, slant="italic"))
        self.lbl_credit.pack(side="right", padx=(10, 15))

    def on_out_lang_change(self, value):
        src = self.src_lang_out.get()
        tgt = self.tgt_lang_out.get()
        if src == tgt and self.is_running_out:
            messagebox.showwarning("SyncVRC", self.get_t("warn_same_lang"))
            self.src_lang_out.set(self.out_src_val)
            self.tgt_lang_out.set(self.out_tgt_val)
        else:
            self.out_src_val = src
            self.out_tgt_val = tgt
            if src == tgt:
                messagebox.showwarning("SyncVRC", self.get_t("warn_same_lang"))
            self.save_all_settings()

    def on_in_lang_change(self, value):
        src = self.src_lang_in.get()
        tgt = self.tgt_lang_in.get()
        if src == tgt and self.is_running_in:
            messagebox.showwarning("SyncVRC", self.get_t("warn_same_lang"))
            self.src_lang_in.set(self.in_src_val)
            self.tgt_lang_in.set(self.in_tgt_val)
        else:
            self.in_src_val = src
            self.in_tgt_val = tgt
            if src == tgt:
                messagebox.showwarning("SyncVRC", self.get_t("warn_same_lang"))
            self.save_all_settings()

    def on_engine_change(self, value):
        if str(self.api_key_entry.cget("state")) == "normal":
            self.api_keys[self.trans_engine_val] = self.api_key_var.get().strip()
        
        self.trans_engine_val = value
        
        new_key = self.api_keys.get(value, "")
        self.api_key_var.set(new_key)
        
        if new_key:
            self.api_key_entry.configure(state="disabled", show="*", fg_color=("gray85", "gray25"))
            self.btn_api_action.configure(text=self.get_t("btn_edit"))
        else:
            default_entry_color = ctk.ThemeManager.theme["CTkEntry"]["fg_color"]
            self.api_key_entry.configure(state="normal", show="", fg_color=default_entry_color)
            self.btn_api_action.configure(text=self.get_t("btn_save"))
            
        self.save_all_settings()

    def on_hotkey_change(self, value):
        self.hk_out = self.cmb_hk_out.get()
        self.hk_in = self.cmb_hk_in.get()
        self.hk_push = self.cmb_hk_push.get()
        self.update_button_texts()
        self.save_all_settings()
        self.apply_hotkeys()

    def toggle_api_edit(self):
        current_state = self.api_key_entry.cget("state")
        if current_state == 'normal':
            val = self.api_key_var.get().strip()
            if val:
                self.api_keys[self.trans_engine_val] = val
                self.api_key_entry.configure(show="*", state="disabled", fg_color=("gray85", "gray25"))
                self.btn_api_action.configure(text=self.get_t("btn_edit"))
                self.save_all_settings()
        else:
            default_entry_color = ctk.ThemeManager.theme["CTkEntry"]["fg_color"]
            self.api_key_entry.configure(state="normal", show="", fg_color=default_entry_color)
            self.btn_api_action.configure(text=self.get_t("btn_save"))

    def update_button_texts(self):
        out_state = self.get_t("btn_stop_out") if self.is_running_out else self.get_t("btn_start_out")
        hk_out_str = f" [{self.hk_out}]" if self.hk_out and self.hk_out != "None" else ""
        self.start_btn_out.configure(text=out_state + hk_out_str)

        hk_push_str = f" [{self.hk_push}]" if self.hk_push and self.hk_push != "None" else ""
        self.push_btn_out.configure(text=self.get_t("btn_hold") + hk_push_str)

        in_state = self.get_t("btn_stop_in") if self.is_running_in else self.get_t("btn_start_in")
        hk_in_str = f" [{self.hk_in}]" if self.hk_in and self.hk_in != "None" else ""
        self.start_btn_in.configure(text=in_state + hk_in_str)

    def load_config(self):
        self.api_keys = {"Google Gemini": "", "DeepL API": "", "OpenAI": ""}
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    if "api_keys" in data:
                        self.api_keys = data["api_keys"]
                    elif "api_key" in data: 
                        self.api_keys["Google Gemini"] = data["api_key"]

                    self.trans_engine_val = data.get("trans_engine", "Google Gemini")
                    if hasattr(self, 'trans_engine_combo'):
                        self.trans_engine_combo.set(self.trans_engine_val)

                    self.ai_device_val = data.get("ai_device", "GPU (NVIDIA)")
                    if hasattr(self, 'ai_device_combo'):
                        self.ai_device_combo.set(self.ai_device_val)

                    self.enable_telemetry_var.set(data.get("enable_telemetry", False))
                    self.enable_mute_sync_var.set(data.get("enable_mute_sync", False))
                    
                    self.silence_timeout_val = float(data.get("silence_timeout", 0.5))
                    self.max_record_time_val = int(data.get("max_record_time", 15))
                    self.beam_size_val = int(data.get("beam_size", 2))
                    
                    if hasattr(self, 'slider_silence'): self.slider_silence.set(self.silence_timeout_val)
                    if hasattr(self, 'slider_max_rec'): self.slider_max_rec.set(self.max_record_time_val)
                    if hasattr(self, 'slider_beam'): self.slider_beam.set(self.beam_size_val)

                    current_key = self.api_keys.get(self.trans_engine_val, "")
                    self.api_key_var.set(current_key)
                    
                    self.current_ui_lang = data.get("ui_lang", "English")
                    
                    self.is_dark_mode = data.get("theme_dark", False)
                    self.whisper_model_val = data.get("whisper_model", "medium")
                    ctk.set_appearance_mode("Dark" if self.is_dark_mode else "Light")
                    if hasattr(self, 'switch_theme'):
                        if self.is_dark_mode: self.switch_theme.select()
                        else: self.switch_theme.deselect()
                    
                    self.out_src_val = data.get("out_src", "English")
                    self.out_tgt_val = data.get("out_tgt", "Japanese")
                    if hasattr(self, 'src_lang_out'):
                        self.src_lang_out.set(self.out_src_val)
                        self.tgt_lang_out.set(self.out_tgt_val)
                        
                    self.in_src_val = data.get("in_src", "Japanese")
                    self.in_tgt_val = data.get("in_tgt", "English")
                    if hasattr(self, 'src_lang_in'):
                        self.src_lang_in.set(self.in_src_val)
                        self.tgt_lang_in.set(self.in_tgt_val)
                    

                        
                    self.hk_out = data.get("hk_out", "F2")
                    self.hk_in = data.get("hk_in", "F3")
                    self.hk_push = data.get("hk_push", "None")
                    if hasattr(self, 'cmb_hk_out'):
                        self.cmb_hk_out.set(self.hk_out)
                        self.cmb_hk_in.set(self.hk_in)
                        self.cmb_hk_push.set(self.hk_push)
                        
                    if current_key:
                        self.api_key_entry.configure(state="disabled", show="*", fg_color=("gray85", "gray25"))
                        self.btn_api_action.configure(text=self.get_t("btn_edit"))
                    else:
                        default_entry_color = ctk.ThemeManager.theme["CTkEntry"]["fg_color"]
                        self.api_key_entry.configure(state="normal", show="", fg_color=default_entry_color)
                        self.btn_api_action.configure(text=self.get_t("btn_save"))
            except Exception: pass
        else:
            self.btn_api_action.configure(text=self.get_t("btn_save"))

    def save_all_settings(self):
        if hasattr(self, 'trans_engine_val') and str(self.api_key_entry.cget("state")) == "normal":
            self.api_keys[self.trans_engine_val] = self.api_key_var.get().strip()
            
        self.recognizer_out.pause_threshold = self.silence_timeout_val
        self.recognizer_in.pause_threshold = self.silence_timeout_val
            
        data = {
            "api_keys": self.api_keys,
            "trans_engine": self.trans_engine_combo.get() if hasattr(self, 'trans_engine_combo') else "Google Gemini",
            "ai_device": self.ai_device_combo.get() if hasattr(self, 'ai_device_combo') else "GPU (NVIDIA)",
            "ui_lang": self.ui_lang_combo.get() if hasattr(self, 'ui_lang_combo') else "English",
            "theme_dark": self.is_dark_mode,
            "whisper_model": getattr(self, 'whisper_model_val', "medium"),
            "enable_telemetry": self.enable_telemetry_var.get(),
            "enable_mute_sync": self.enable_mute_sync_var.get(),
            "silence_timeout": self.silence_timeout_val,
            "max_record_time": self.max_record_time_val,
            "beam_size": self.beam_size_val,
            "out_src": self.src_lang_out.get() if hasattr(self, 'src_lang_out') else "English",
            "out_tgt": self.tgt_lang_out.get() if hasattr(self, 'tgt_lang_out') else "Japanese",
            "in_src": self.src_lang_in.get() if hasattr(self, 'src_lang_in') else "Japanese",
            "in_tgt": self.tgt_lang_in.get() if hasattr(self, 'tgt_lang_in') else "English",
            "hk_out": self.hk_out,
            "hk_in": self.hk_in,
            "hk_push": self.hk_push
        }
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f)
        except: pass

    def apply_hotkeys(self):
        keyboard.unhook_all()
        if self.hk_out != "None":
            keyboard.add_hotkey(self.hk_out, lambda: self.root.after(0, self.toggle_out_thread))
        if self.hk_in != "None":
            keyboard.add_hotkey(self.hk_in, lambda: self.root.after(0, self.toggle_in_thread))
        if self.hk_push != "None":
            keyboard.on_press_key(self.hk_push, lambda e: self.root.after(0, self.start_push_record, e))
            keyboard.on_release_key(self.hk_push, lambda e: self.root.after(0, self.stop_push_record, e))

    def apply_theme_colors(self):
        if self.is_dark_mode:
            self.lbl_app_title.configure(text_color="#88C0D0")
            self.lbl_osc_status_text.configure(text_color="#81A1C1")
            self.sidebar_frame.configure(fg_color="#2b2b2b")
        else:
            self.lbl_app_title.configure(text_color="#1f538d")
            self.lbl_osc_status_text.configure(text_color="#2196F3")
            self.sidebar_frame.configure(fg_color="#e0e0e0")

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        ctk.set_appearance_mode("Dark" if self.is_dark_mode else "Light")
        self.apply_theme_colors()
        self.switch_theme.configure(text=self.get_t("theme_dark"))
        self.save_all_settings()

    def change_ui_language(self, value=None, save=True):
        self.current_ui_lang = self.ui_lang_combo.get()
        if save: self.save_all_settings()
        
        self.btn_nav_trans.set_text(self.get_t("nav_trans"))
        self.btn_nav_audio.set_text(self.get_t("nav_audio"))
        self.btn_nav_settings.set_text(self.get_t("nav_settings"))

        self.lbl_ui_lang.configure(text=self.get_t("ui_lang"))
        self.lbl_api_key.configure(text=self.get_t("api_key"))
        self.lbl_engine.configure(text=self.get_t("engine_lbl"))
        self.lbl_device.configure(text=self.get_t("device_lbl"))
        self.lbl_device_info.configure(text=self.get_t("device_info"))
        if hasattr(self, 'lbl_model'):
            self.lbl_model.configure(text=self.get_t("model_lbl"))
            self.btn_clear_cache.configure(text=self.get_t("btn_clear_cache"))
            self.update_model_info_label()
            if hasattr(self, 'btn_nav_docs'):
                self.btn_nav_docs.set_text(self.get_t("nav_docs") + " ↗")
        
        self.lbl_support.configure(text=self.get_t("support_msg"))
        self.lbl_osc_status_text.configure(text=self.get_t("osc_status"))
        
        if self.api_key_entry.cget("state") == 'disabled':
            self.btn_api_action.configure(text=self.get_t("btn_edit"))
        else:
            self.btn_api_action.configure(text=self.get_t("btn_save"))
        
        self.switch_theme.configure(text=self.get_t("theme_dark"))
        self.chk_telemetry.configure(text=self.get_t("telemetry_lbl"))
        self.chk_mute_sync.configure(text=self.get_t("mute_sync_lbl"))
        self.lbl_adv_audio.configure(text=self.get_t("adv_audio_lbl"))
        self.lbl_silence.configure(text=self.get_t("silence_timeout_lbl"))
        self.lbl_max_rec.configure(text=self.get_t("max_record_time_lbl"))
        self.lbl_beam.configure(text=self.get_t("beam_size_lbl"))

        self.lbl_left_title.configure(text=self.get_t("left_frame"))
        self.lbl_right_title.configure(text=self.get_t("right_frame"))
        self.lbl_mic_out.configure(text=self.get_t("mic_out"))
        self.lbl_speaker_in.configure(text=self.get_t("speaker_in"))
        
        self.lbl_src_out.configure(text=self.get_t("src_lang_out"))
        self.lbl_tgt_out.configure(text=self.get_t("tgt_lang_out"))
        self.radio_auto.configure(text=self.get_t("mode_auto"))
        self.radio_push.configure(text=self.get_t("mode_push"))
        self.lbl_manual.configure(text=self.get_t("manual_label"))
        self.btn_send.configure(text=self.get_t("btn_send"))
        self.lbl_log_out.configure(text=self.get_t("log_out"))

        self.lbl_src_in.configure(text=self.get_t("src_lang_in"))
        self.lbl_tgt_in.configure(text=self.get_t("tgt_lang_in"))
        self.lbl_log_in.configure(text=self.get_t("log_in"))
        self.lbl_license.configure(text=self.get_t("license"))
        self.lbl_credit.configure(text=self.get_t("credit"))

        self.lbl_theme_title.configure(text=self.get_t("theme_title"))
        self.lbl_sec_general.configure(text=self.get_t("sec_general"))
        self.lbl_sec_api.configure(text=self.get_t("sec_api"))
        self.lbl_sec_hotkey.configure(text=self.get_t("sec_hotkey"))
        self.lbl_hk_out_set.configure(text=self.get_t("hk_out_lbl"))
        self.lbl_hk_in_set.configure(text=self.get_t("hk_in_lbl"))
        self.lbl_hk_push_set.configure(text=self.get_t("hk_push_lbl"))

        if hasattr(self, 'latest_version_found') and self.latest_version_found:
            self.btn_nav_update.configure(text=self.get_t("btn_update_avail").format(self.latest_version_found))

        self.update_button_texts()

    def log_out(self, message, msg_type="info"):
        self.log_area_out.configure(state="normal")
        time_str = time.strftime('%H:%M:%S')
        
        if msg_type == "heard":     prefix = "[MIC]"
        elif msg_type == "trans":   prefix = "[API]"
        elif msg_type == "err":     prefix = "[ERR]"
        else:                       prefix = "[SYS]"
            
        formatted = f"[{time_str}] {prefix} {message}\n"
        self.log_area_out.insert("end", formatted)
        self.log_area_out.see("end")
        self.log_area_out.configure(state="disabled")

    def log_in(self, message, msg_type="info"):
        self.log_area_in.configure(state="normal")
        time_str = time.strftime('%H:%M:%S')
        
        if msg_type == "heard":     prefix = "[MIC]"
        elif msg_type == "trans":   prefix = "[API]"
        elif msg_type == "err":     prefix = "[ERR]"
        else:                       prefix = "[SYS]"
            
        formatted = f"[{time_str}] {prefix} {message}\n"
        self.log_area_in.insert("end", formatted)
        self.log_area_in.see("end")
        self.log_area_in.configure(state="disabled")

    def init_core_systems(self):
        api_key = self.api_keys.get(self.trans_engine_val, "").strip()
        if not api_key:
            self.root.after(0, lambda: self.log_out(self.get_t("err_api_invalid"), "err"))
            self.root.after(0, lambda: self.select_frame("settings"))
            return False
        self.save_all_settings()

        if self.trans_engine_val == "Google Gemini":
            if not hasattr(self, 'gemini_client'):
                try:
                    self.gemini_client = genai.Client(api_key=api_key)
                    sys_instruct = "You are a pure translation API. Translate the text accurately and completely. Output ONLY the translated text. No filler."
                    safety_settings = [
                        types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
                        types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=types.HarmBlockThreshold.BLOCK_NONE),
                        types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
                        types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
                    ]
                    self.gen_config = types.GenerateContentConfig(temperature=0.2, system_instruction=sys_instruct, safety_settings=safety_settings)
                except Exception as e:
                    self.root.after(0, lambda err=e: self.log_out(f"API Initialization Error: {err}", "err"))
                    if self.enable_telemetry_var.get():
                        try: sentry_sdk.capture_exception(e)
                        except: pass
                    return False

        if not hasattr(self, 'whisper_model'):
            self.root.after(0, lambda: self.start_btn_out.configure(state="disabled", text=self.get_t("btn_loading_model")))
            self.root.after(0, lambda: self.start_btn_in.configure(state="disabled", text=self.get_t("btn_loading_model")))
            
            dev_type = "cuda" if self.ai_device_val == "GPU (NVIDIA)" else "cpu"
            c_type = "float16" if dev_type == "cuda" else "int8"
            
            self.root.after(0, lambda: self.log_out(self.get_t("log_load_model").format(dev_type.upper()), "info"))
            try:
                if getattr(self, "whisper_model_val", "medium") == "medium":
                    model_path = "medium"
                else:
                    model_dir = os.path.join(resource_path("models"), f"faster-whisper-{self.whisper_model_val}")
                    model_path = model_dir if os.path.exists(model_dir) else self.whisper_model_val
                
                self.whisper_model = WhisperModel(model_path, device=dev_type, compute_type=c_type)
                self.root.after(0, lambda: self.log_out(self.get_t("log_model_loaded"), "info"))
            except Exception as e:
                err_str = str(e).lower()
                if any(k in err_str for k in ["cuda", "cudnn", "cublas", "gpu", "library"]):
                    self.root.after(0, lambda: self.log_out(self.get_t("err_cuda_not_found"), "err"))
                    self.root.after(0, lambda: messagebox.showerror("SyncVRC", self.get_t("alert_cuda")))
                    self.root.after(0, lambda: self.select_frame("settings"))
                else:
                    self.root.after(0, lambda err=e: self.log_out(f"Whisper Error: {err}", "err"))
                    self.root.after(0, lambda err=e: messagebox.showerror("SyncVRC", self.get_t("alert_whisper_error").format(str(err))))
                    
                if self.enable_telemetry_var.get():
                    try: sentry_sdk.capture_exception(e)
                    except: pass
                
                self.root.after(0, self.update_button_texts)
                self.root.after(0, lambda: self.start_btn_out.configure(state="normal"))
                self.root.after(0, lambda: self.start_btn_in.configure(state="normal"))
                return False
                
            self.root.after(0, lambda: self.start_btn_out.configure(state="normal"))
            self.root.after(0, lambda: self.start_btn_in.configure(state="normal"))
            
        self._error_shown = False
        return True

    def force_stop_all(self):
        """Force stop both outgoing and incoming systems and reset UI."""
        self.is_running_out = False
        self.is_running_in = False
        self.root.after(0, self.update_button_texts)
        self.root.after(0, lambda: self.start_btn_out.configure(fg_color="#28a745", hover_color="#218838", state="normal"))
        self.root.after(0, lambda: self.start_btn_in.configure(fg_color="#28a745", hover_color="#218838", state="normal"))
        self.root.after(0, lambda: self.mic_combo_out.configure(state="normal"))
        self.root.after(0, lambda: self.mic_combo_in.configure(state="normal"))
        self.root.after(0, lambda: self.push_btn_out.configure(state="disabled"))
        self.root.after(0, self.update_settings_state)

    def handle_fatal_error(self, alert_key, log_msg, source_type, err=None, go_settings=False):
        """Handle a fatal error: stop systems, log it, show popup alert (only once)."""
        if getattr(self, '_error_shown', False):
            return
        self._error_shown = True
        
        log_func = self.log_out if source_type == "out" else self.log_in
        self.root.after(0, lambda: log_func(log_msg, "err"))
        
        self.force_stop_all()
        
        alert_msg = self.get_t(alert_key)
        if err and "{}" in alert_msg:
            alert_msg = alert_msg.format(str(err))
        
        def _show_alert():
            messagebox.showerror("SyncVRC", alert_msg)
            if go_settings:
                self.select_frame("settings")
            self._error_shown = False
        
        self.root.after(100, _show_alert)

    def on_mode_change_out(self):
        if not self.is_running_out:
            self.push_btn_out.configure(state="disabled")
            return
        if self.mode_var_out.get() == "auto":
            self.push_btn_out.configure(state="disabled")
            threading.Thread(target=self.auto_listen_out, daemon=True).start()
        else:
            self.push_btn_out.configure(state="normal")

    def toggle_out_thread(self): 
        if not self.is_running_out:
            if self.src_lang_out.get() == self.tgt_lang_out.get():
                messagebox.showwarning("SyncVRC", self.get_t("warn_same_lang"))
                return

            if str(self.api_key_entry.cget("state")) == "normal":
                self.api_keys[self.trans_engine_val] = self.api_key_var.get().strip()
                self.api_key_entry.configure(show="*", state="disabled", fg_color=("gray85", "gray25"))
                self.btn_api_action.configure(text=self.get_t("btn_edit"))
                self.save_all_settings()

            api_key = self.api_keys.get(self.trans_engine_val, "").strip()
            if not api_key:
                messagebox.showwarning("SyncVRC", self.get_t("err_api_empty"))
                self.select_frame("settings")
                return

            if not self.check_osc_enabled():
                messagebox.showwarning("SyncVRC", self.get_t("warn_osc_forgot"))
                
        threading.Thread(target=self.toggle_out, daemon=True).start()

    def toggle_out(self):
        if not self.is_running_out:
            if not hasattr(self, 'whisper_model'):
                self.root.after(0, lambda: self.start_btn_out.configure(state="disabled", text=self.get_t("btn_loading_model")))
            
            if not self.init_core_systems(): return
            
            self.is_running_out = True
            self.root.after(0, self.update_button_texts) 
            self.root.after(0, lambda: self.start_btn_out.configure(fg_color="#dc3545", hover_color="#c82333"))
            self.root.after(0, lambda: self.mic_combo_out.configure(state="disabled"))
            self.root.after(0, lambda: self.log_out(self.get_t("log_start_mic").format(self.mic_combo_out.get()), "info"))
            self.root.after(0, self.update_settings_state)
            self.on_mode_change_out()
        else:
            self.is_running_out = False
            self.root.after(0, self.update_button_texts) 
            self.root.after(0, lambda: self.start_btn_out.configure(fg_color="#28a745", hover_color="#218838"))
            self.root.after(0, lambda: self.mic_combo_out.configure(state="normal"))
            self.root.after(0, lambda: self.push_btn_out.configure(state="disabled"))
            self.root.after(0, self.update_settings_state)
            self.root.after(0, lambda: self.log_out(self.get_t("log_out_stop"), "info"))

    def auto_listen_out(self):
        mic_name = self.mic_combo_out.get()
        mic_idx = self.mic_mapping.get(mic_name, None)
        if mic_idx is None: return
        with sr.Microphone(device_index=mic_idx) as source:
            self.recognizer_out.adjust_for_ambient_noise(source, duration=0.5)
            self.root.after(0, lambda: self.log_out(self.get_t("log_auto_listen"), "info"))
            while self.is_running_out and self.mode_var_out.get() == "auto":
                if self.enable_mute_sync_var.get() and self.is_vrc_muted:
                    time.sleep(0.5)
                    continue
                    
                try:
                    audio = self.recognizer_out.listen(source, timeout=1, phrase_time_limit=self.max_record_time_val)
                    if self.enable_mute_sync_var.get() and self.is_vrc_muted:
                        continue
                    threading.Thread(target=self.process_audio, args=(audio, "out"), daemon=True).start()
                except sr.WaitTimeoutError: continue
                except Exception as e:
                    if self.enable_telemetry_var.get():
                        try: sentry_sdk.capture_exception(e)
                        except: pass

    def start_push_record(self, event=None):
        if not self.is_running_out or self.mode_var_out.get() != "push": return
        if self.is_recording_out: return 
        self.is_recording_out = True
        self.log_out(self.get_t("log_recording"), "info")
        threading.Thread(target=self.push_listen_out, daemon=True).start()

    def stop_push_record(self, event=None):
        if not self.is_running_out or self.mode_var_out.get() != "push": return
        self.is_recording_out = False

    def push_listen_out(self):
        mic_name = self.mic_combo_out.get()
        mic_idx = self.mic_mapping.get(mic_name, None)
        if mic_idx is None: return
        with sr.Microphone(device_index=mic_idx) as source:
            try:
                audio = self.recognizer_out.listen(source, timeout=None, phrase_time_limit=self.max_record_time_val)
                if self.enable_mute_sync_var.get() and self.is_vrc_muted:
                    return
                self.process_audio(audio, "out")
            except Exception as e:
                if self.enable_telemetry_var.get():
                    try: sentry_sdk.capture_exception(e)
                    except: pass

    def send_manual_text(self):
        if not self.is_running_out:
            messagebox.showwarning("SyncVRC", self.get_t("warn_manual"))
            return
        text = self.manual_entry.get().strip()
        if text:
            self.manual_entry.delete(0, 'end')
            self.log_out(f"{text}", "heard")
            threading.Thread(target=self.process_manual_translation, args=(text,), daemon=True).start()

    def process_manual_translation(self, text):
        tgt = self.tgt_lang_out.get()
        self.osc_client.send_message("/chatbox/typing", True)
        
        try:
            if self.trans_engine_val == "Google Gemini":
                prompt = f"Translate exactly to {tgt}: {text}"
                response = self.gemini_client.models.generate_content(
                    model='gemini-2.5-flash', contents=prompt, config=self.gen_config
                )
                translation = response.text.strip()
            else:
                translation = f"[{self.trans_engine_val} integration coming soon] {text}"
                
            self.root.after(0, lambda: self.log_out(f"{translation}", "trans"))
            self.send_to_vrchat(f"{text}\n{translation}")
        except Exception as e:
            err_str = str(e).lower()
            self.osc_client.send_message("/chatbox/typing", False)
            
            if any(k in err_str for k in ["429", "quota", "exhausted", "limit"]):
                self.handle_fatal_error("alert_api_limit", self.get_t("err_api_limit"), "out", go_settings=True)
            elif "api key not valid" in err_str or "api_key" in err_str:
                self.handle_fatal_error("alert_api_invalid", self.get_t("err_api_invalid"), "out", go_settings=True)
            else:
                self.handle_fatal_error("alert_api_generic", f"❌ Error: {e}", "out", err=e)

            if self.enable_telemetry_var.get() and "limit" not in err_str and "api key" not in err_str:
                try: sentry_sdk.capture_exception(e)
                except: pass

    def toggle_in_thread(self): 
        if not self.is_running_in:
            if self.src_lang_in.get() == self.tgt_lang_in.get():
                messagebox.showwarning("SyncVRC", self.get_t("warn_same_lang"))
                return

            if str(self.api_key_entry.cget("state")) == "normal":
                self.api_keys[self.trans_engine_val] = self.api_key_var.get().strip()
                self.api_key_entry.configure(show="*", state="disabled", fg_color=("gray85", "gray25"))
                self.btn_api_action.configure(text=self.get_t("btn_edit"))
                self.save_all_settings()

            api_key = self.api_keys.get(self.trans_engine_val, "").strip()
            if not api_key:
                messagebox.showwarning("SyncVRC", self.get_t("err_api_empty"))
                self.select_frame("settings")
                return

            if not self.check_osc_enabled():
                messagebox.showwarning("SyncVRC", self.get_t("warn_osc_forgot"))
                
        threading.Thread(target=self.toggle_in, daemon=True).start()

    def toggle_in(self):
        if not self.is_running_in:
            if not hasattr(self, 'whisper_model'):
                self.root.after(0, lambda: self.start_btn_in.configure(state="disabled", text=self.get_t("btn_loading_model")))
            
            if not self.init_core_systems(): return
            
            self.is_running_in = True
            self.root.after(0, self.update_button_texts) 
            self.root.after(0, lambda: self.start_btn_in.configure(fg_color="#dc3545", hover_color="#c82333"))
            self.root.after(0, lambda: self.mic_combo_in.configure(state="disabled"))
            self.root.after(0, lambda: self.log_in(self.get_t("log_start_loop").format(self.mic_combo_in.get()), "info"))
            self.update_settings_state()
            threading.Thread(target=self.auto_listen_in, daemon=True).start()
        else:
            self.is_running_in = False
            self.root.after(0, self.update_button_texts) 
            self.root.after(0, lambda: self.start_btn_in.configure(fg_color="#28a745", hover_color="#218838"))
            self.root.after(0, lambda: self.mic_combo_in.configure(state="normal"))
            self.update_settings_state()
            self.root.after(0, lambda: self.log_in(self.get_t("log_in_stop"), "info"))

    def auto_listen_in(self):
        mic_name = self.mic_combo_in.get()
        mic_idx = self.mic_mapping.get(mic_name, None)
        if mic_idx is None: return
        with sr.Microphone(device_index=mic_idx) as source:
            self.recognizer_out.adjust_for_ambient_noise(source, duration=0.5)
            self.root.after(0, lambda: self.log_in(self.get_t("log_speaker_listen"), "info"))
            while self.is_running_in:
                try:
                    audio = self.recognizer_in.listen(source, timeout=1, phrase_time_limit=self.max_record_time_val)
                    threading.Thread(target=self.process_audio, args=(audio, "in"), daemon=True).start()
                except sr.WaitTimeoutError: continue
                except Exception as e:
                    if self.enable_telemetry_var.get():
                        try: sentry_sdk.capture_exception(e)
                        except: pass

    def process_audio(self, audio, source_type):
        if source_type == "out" and not self.is_running_out: return
        if source_type == "in" and not self.is_running_in: return

        try:
            audio_data = audio.get_raw_data(convert_rate=16000, convert_width=2)
            audio_np = np.frombuffer(audio_data, np.int16).astype(np.float32) / 32768.0

            if source_type == "out":
                lang_code = self.get_whisper_lang_code(self.src_lang_out.get())
                stt_prompt = "The speaker's name is Meiji, a VRChat creator."
                tgt = self.tgt_lang_out.get()
                log_func = self.log_out
            else:
                lang_code = self.get_whisper_lang_code(self.src_lang_in.get())
                stt_prompt = "" 
                tgt = self.tgt_lang_in.get()
                log_func = self.log_in

            with self.whisper_lock:
                if source_type == "out" and not self.is_running_out: return
                if source_type == "in" and not self.is_running_in: return

                # Check if VAD model file exists (may be missing in packaged builds)
                vad_available = True
                try:
                    import faster_whisper
                    vad_path = os.path.join(os.path.dirname(faster_whisper.__file__), "assets", "silero_vad_v6.onnx")
                    if not os.path.exists(vad_path):
                        vad_available = False
                except Exception:
                    vad_available = False

                transcribe_kwargs = dict(
                    beam_size=self.beam_size_val, 
                    language=lang_code, 
                    initial_prompt=stt_prompt,
                    condition_on_previous_text=False
                )
                if vad_available:
                    transcribe_kwargs["vad_filter"] = True
                    transcribe_kwargs["vad_parameters"] = dict(min_silence_duration_ms=int(self.silence_timeout_val * 1000))

                segments, _ = self.whisper_model.transcribe(audio_np, **transcribe_kwargs)
                
                valid_texts = []
                for segment in segments:
                    text = segment.text.strip()
                    if any(bad_word in text for bad_word in ["字幕", "視聴", "Subtitles", "視聴ありがとうございました"]): continue
                    valid_texts.append(text)
                text = "".join(valid_texts).strip()

            if text:
                self.root.after(0, lambda: log_func(text, "heard"))
                if source_type == "out": self.osc_client.send_message("/chatbox/typing", True)

                if self.trans_engine_val == "Google Gemini":
                    prompt = f"Translate exactly to {tgt}: {text}"
                    response = self.gemini_client.models.generate_content(
                        model='gemini-2.5-flash', contents=prompt, config=self.gen_config
                    )
                    translation = response.text.strip()
                else:
                    translation = f"[{self.trans_engine_val} integration coming soon] {text}"

                self.root.after(0, lambda: log_func(translation, "trans"))

                if source_type == "out":
                    self.send_to_vrchat(f"{text}\n{translation}")

        except Exception as e:
            err_str = str(e).lower()
            if source_type == "out":
                self.osc_client.send_message("/chatbox/typing", False)
            
            if any(k in err_str for k in ["429", "quota", "exhausted", "limit"]):
                self.handle_fatal_error("alert_api_limit", self.get_t("err_api_limit"), source_type, go_settings=True)
            elif "api key not valid" in err_str or "api_key" in err_str:
                self.handle_fatal_error("alert_api_invalid", self.get_t("err_api_invalid"), source_type, go_settings=True)
            else:
                self.handle_fatal_error("alert_api_generic", f"❌ Error: {e}", source_type, err=e)

            if self.enable_telemetry_var.get() and "limit" not in err_str and "api key" not in err_str:
                try: sentry_sdk.capture_exception(e)
                except: pass

    def send_to_vrchat(self, text):
        max_length = 144
        if len(text) <= max_length:
            self.osc_client.send_message("/chatbox/input", [text, True, False])
        else:
            chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
            for chunk in chunks:
                if not self.is_running_out: break
                self.osc_client.send_message("/chatbox/input", [chunk, True, False])
                time.sleep(1.8)

    def get_whisper_lang_code(self, lang_name):
        codes = {"English": "en", "Japanese": "ja", "Korean": "ko", "Chinese": "zh", "Spanish": "es", "Russian": "ru", "French": "fr", "German": "de", "Portuguese": "pt", "Thai": "th"}
        return codes.get(lang_name, "en")


    MODEL_SIZES = {
        "tiny": "~75 MB",
        "base": "~145 MB",
        "small": "~484 MB",
        "medium": "~1.5 GB",
        "large-v3": "~3.1 GB"
    }

    def update_model_dropdown(self):
        models = ["tiny", "base", "small", "medium", "large-v3"]
        display_values = []
        for m in models:
            if m == "medium":
                display_values.append(m + " (Downloaded)")
            else:
                model_dir = os.path.join(resource_path("models"), f"faster-whisper-{m}")
                if os.path.exists(model_dir) and os.path.exists(os.path.join(model_dir, "model.bin")):
                    display_values.append(m + " (Downloaded)")
                else:
                    display_values.append(m)
        
        self.whisper_model_combo.configure(values=display_values)
        
        # Set current value correctly
        curr = getattr(self, "whisper_model_val", "medium")
        for dv in display_values:
            if dv.startswith(curr):
                self.whisper_model_combo.set(dv)
                break

    def update_model_info_label(self):
        """Update the model info label based on the currently selected whisper model."""
        curr = getattr(self, "whisper_model_val", "medium")
        info_key_map = {
            "tiny": "model_info_tiny",
            "base": "model_info_base",
            "small": "model_info_small",
            "medium": "model_info_medium",
            "large-v3": "model_info_large"
        }
        key = info_key_map.get(curr, "model_info_medium")
        if hasattr(self, 'lbl_model_info'):
            self.lbl_model_info.configure(text=self.get_t(key))

    def download_whisper_model(self, model_name, on_complete, on_cancel):
        repo_id = f"Systran/faster-whisper-{model_name}"
        save_dir = os.path.join(resource_path("models"), f"faster-whisper-{model_name}")
        
        dl_window = ctk.CTkToplevel(self.root)
        dl_window.title(self.get_t("downloading_model_title"))
        dl_window.geometry("500x180")
        dl_window.transient(self.root)
        dl_window.grab_set()
        dl_window.protocol("WM_DELETE_WINDOW", lambda: self.cancel_download(dl_window, on_cancel))
        
        lbl_msg = ctk.CTkLabel(dl_window, text=self.get_t("downloading_model_msg").format(model_name, "0"), font=ctk.CTkFont(size=14, weight="bold"))
        lbl_msg.pack(pady=(20, 10))
        
        progressbar = ctk.CTkProgressBar(dl_window, mode="determinate")
        progressbar.pack(fill="x", padx=40)
        progressbar.set(0)
        
        lbl_detail = ctk.CTkLabel(dl_window, text="Preparing...", font=ctk.CTkFont(size=11), text_color="gray")
        lbl_detail.pack(pady=(5, 10))
        
        self.download_cancelled = False
        
        def run_download():
            import urllib.request, json, shutil
            try:
                os.makedirs(save_dir, exist_ok=True)
                url = f"https://huggingface.co/api/models/{repo_id}/tree/main"
                req = urllib.request.Request(url, headers={'User-Agent': 'SyncVRC-App'})
                with urllib.request.urlopen(req) as response:
                    data = json.loads(response.read().decode('utf-8'))
                
                files_to_download = []
                for f in data:
                    if f['type'] == 'file' and f['path'] in ['config.json', 'model.bin', 'tokenizer.json', 'vocabulary.txt', 'vocabulary.json']:
                        files_to_download.append(f)
                
                total_size = sum(f.get('size', 0) for f in files_to_download)
                downloaded_size = 0
                
                for file_info in files_to_download:
                    if self.download_cancelled:
                        break
                    
                    file_name = file_info['path']
                    file_url = f"https://huggingface.co/{repo_id}/resolve/main/{file_name}"
                    file_path = os.path.join(save_dir, file_name)
                    
                    self.root.after(0, lambda name=file_name: lbl_detail.configure(text=f"Downloading {name}..."))
                    
                    req_file = urllib.request.Request(file_url, headers={'User-Agent': 'SyncVRC-App'})
                    with urllib.request.urlopen(req_file) as response, open(file_path, 'wb') as out_file:
                        chunk_size = 1024 * 64
                        while True:
                            if self.download_cancelled:
                                break
                            chunk = response.read(chunk_size)
                            if not chunk:
                                break
                            out_file.write(chunk)
                            downloaded_size += len(chunk)
                            if total_size > 0:
                                percent = (downloaded_size / total_size)
                                percent_int = int(percent * 100)
                                self.root.after(0, lambda p=percent, pint=percent_int: (
                                    progressbar.set(p),
                                    lbl_msg.configure(text=self.get_t("downloading_model_msg").format(model_name, str(pint)))
                                ))
                
                if self.download_cancelled:
                    shutil.rmtree(save_dir, ignore_errors=True)
                else:
                    self.root.after(0, dl_window.destroy)
                    self.root.after(0, on_complete)
                    self.root.after(0, self.update_model_dropdown)
                    
            except Exception as e:
                self.root.after(0, lambda err=e: messagebox.showerror("Download Error", f"Failed to download model:\n{str(err)}"))
                import shutil
                shutil.rmtree(save_dir, ignore_errors=True)
                self.root.after(0, dl_window.destroy)
                self.root.after(0, on_cancel)
                
        import threading
        threading.Thread(target=run_download, daemon=True).start()

    def cancel_download(self, window, on_cancel):
        self.download_cancelled = True
        window.destroy()
        on_cancel()

    def on_model_change(self, value):
        from tkinter import messagebox
        import os
        
        # Strip the " (Downloaded)" if it exists
        clean_val = value.replace(" (Downloaded)", "")
        
        if self.is_running_out or self.is_running_in:
            messagebox.showwarning("SyncVRC", "Please stop Outgoing and Incoming before changing the model.")
            self.update_model_dropdown()
            return

        if clean_val == "medium":
            self.apply_model_change("medium")
            self.update_model_dropdown()
            self.update_model_info_label()
            return

        model_dir = os.path.join(resource_path("models"), f"faster-whisper-{clean_val}")
        if not os.path.exists(model_dir) or not os.path.exists(os.path.join(model_dir, "model.bin")):
            size_str = self.MODEL_SIZES.get(clean_val, "unknown")
            msg = self.get_t("confirm_download_msg").format(clean_val, size_str)
            if messagebox.askyesno(self.get_t("confirm_download_title"), msg):
                self.download_whisper_model(clean_val, 
                    on_complete=lambda: self.apply_model_change(clean_val),
                    on_cancel=lambda: self.update_model_dropdown()
                )
            else:
                self.update_model_dropdown()
        else:
            self.apply_model_change(clean_val)
            self.update_model_dropdown()
        self.update_model_info_label()

    def apply_model_change(self, value):
        self.whisper_model_val = value
        if hasattr(self, 'whisper_model'):
            del self.whisper_model
        self.save_all_settings()
        self.update_model_info_label()

    def clear_model_cache(self):
        from tkinter import messagebox
        import os, shutil
        
        if not messagebox.askyesno(self.get_t("confirm_clear_title"), self.get_t("confirm_clear_msg")):
            return
            
        models_dir = resource_path("models")
        if not os.path.exists(models_dir):
            messagebox.showinfo("SyncVRC", "No unused models to clear.")
            return
            
        cleared = False
        for item in os.listdir(models_dir):
            if item.startswith("faster-whisper-") and item != f"faster-whisper-{self.whisper_model_val}":
                shutil.rmtree(os.path.join(models_dir, item), ignore_errors=True)
                cleared = True
                
        if cleared:
            messagebox.showinfo("SyncVRC", self.get_t("cache_cleared_msg"))
            self.update_model_dropdown()
        else:
            messagebox.showinfo("SyncVRC", "No unused models to clear.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = SyncVRCApp(root)
    root.mainloop()