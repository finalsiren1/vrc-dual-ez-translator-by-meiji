import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import speech_recognition as sr
from pythonosc import udp_client
import json
import os
import numpy as np
from faster_whisper import WhisperModel

from google import genai
from google.genai import types

class VRChatTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x740") # ขยายความสูงนิดหน่อยเพื่อรับกับ Credit
        self.root.resizable(False, False)

        # State Variables
        self.is_running_out = False
        self.is_recording_out = False
        self.is_running_in = False
        
        self.osc_client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
        self.recognizer_out = sr.Recognizer()
        self.recognizer_in = sr.Recognizer()
        self.config_file = "config.json"
        self.mic_names = sr.Microphone.list_microphone_names()
        self.whisper_lock = threading.Lock()
        
        self.init_translations()
        self.setup_ui()
        self.load_config()
        self.change_ui_language() # Apply default language (English)

    def init_translations(self):
        self.current_ui_lang = "en"
        self.translations = {
            "en": {
                "title": "VRC DUAL EZ Translator",
                "ui_lang": "UI Language:",
                "api_key": "Gemini API Key:",
                "left_frame": "Outgoing System (Speak -> VRChat Chatbox)",
                "right_frame": "Incoming System (Translate others' voices)",
                "mic_out": "Select Microphone (Your voice):",
                "src_lang_out": "From:",
                "tgt_lang_out": "Translate to:",
                "mode_auto": "Auto (Continuous)",
                "mode_push": "Push to Record",
                "btn_start_out": "Start Outgoing",
                "btn_stop_out": "Stop Outgoing",
                "btn_hold": "Hold to Speak",
                "manual_label": "Manual Translate (Type and Send):",
                "btn_send": "Send",
                "log_out": "Outgoing Log:",
                "speaker_in": "Select Speaker Loopback (Wave Link / Stereo Mix):",
                "src_lang_in": "Listen Language:",
                "tgt_lang_in": "Translate to:",
                "btn_start_in": "Start Incoming",
                "btn_stop_in": "Stop Incoming",
                "log_in": "Incoming Log (Not sent to VRChat):",
                "warn_manual": "Please start Outgoing system before sending manual text."
            },
            "ja": {
                "title": "VRC DUAL EZ Translator",
                "ui_lang": "UI 言語:",
                "api_key": "Gemini API キー:",
                "left_frame": "送信システム (音声 -> VRChat チャットボックス)",
                "right_frame": "受信システム (他人の音声を翻訳)",
                "mic_out": "マイクを選択 (あなたの声):",
                "src_lang_out": "翻訳元:",
                "tgt_lang_out": "翻訳先:",
                "mode_auto": "自動 (連続)",
                "mode_push": "押して録音",
                "btn_start_out": "送信開始",
                "btn_stop_out": "送信停止",
                "btn_hold": "押している間話す",
                "manual_label": "手動翻訳 (入力して送信):",
                "btn_send": "送信",
                "log_out": "送信ログ:",
                "speaker_in": "スピーカーのループバックを選択 (Wave Link / Stereo Mix):",
                "src_lang_in": "受信言語:",
                "tgt_lang_in": "翻訳先:",
                "btn_start_in": "受信開始",
                "btn_stop_in": "受信停止",
                "log_in": "受信ログ (VRChatには送信されません):",
                "warn_manual": "手動テキストを送信する前に、送信(Outgoing)システムを開始してください。"
            }
        }

    def setup_ui(self):
        # Top Bar (UI Lang + API Key)
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill="x", pady=(10,0))
        
        self.lbl_ui_lang = tk.Label(top_frame)
        self.lbl_ui_lang.pack(side="left", padx=(20, 5))
        
        self.ui_lang_combo = ttk.Combobox(top_frame, values=["English", "日本語"], state="readonly", width=12)
        self.ui_lang_combo.set("English")
        self.ui_lang_combo.pack(side="left", padx=(0, 20))
        self.ui_lang_combo.bind("<<ComboboxSelected>>", self.change_ui_language)

        self.lbl_api_key = tk.Label(top_frame)
        self.lbl_api_key.pack(side="left", padx=(0, 5))
        self.api_key_entry = ttk.Entry(top_frame, width=50, show="*")
        self.api_key_entry.pack(side="left")

        # Credit Footer (บรรทัดลายเซ็นของคุณ)
        credit_label = tk.Label(self.root, text="credit by Meiji ღ", fg="#888888", font=("Arial", 9, "italic"))
        credit_label.pack(side="bottom", pady=5)

        # Main Panes
        main_pane = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_pane.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        self.left_frame = tk.LabelFrame(main_pane, padx=10, pady=10)
        self.right_frame = tk.LabelFrame(main_pane, padx=10, pady=10)

        main_pane.add(self.left_frame, width=530)
        main_pane.add(self.right_frame, width=530)

        self.build_left_panel()
        self.build_right_panel()

    def build_left_panel(self):
        self.lbl_mic_out = tk.Label(self.left_frame)
        self.lbl_mic_out.pack(anchor="w", pady=(5,0))
        self.mic_combo_out = ttk.Combobox(self.left_frame, values=self.mic_names, state="readonly")
        if self.mic_names: self.mic_combo_out.current(0)
        self.mic_combo_out.pack(fill="x", pady=5)

        lang_frame = tk.Frame(self.left_frame)
        lang_frame.pack(fill="x", pady=5)
        self.lbl_src_out = tk.Label(lang_frame)
        self.lbl_src_out.pack(side="left")
        self.src_lang_out = ttk.Combobox(lang_frame, values=["Thai", "English", "Japanese", "Korean", "Chinese"], state="readonly", width=12)
        self.src_lang_out.set("Thai")
        self.src_lang_out.pack(side="left", padx=5)
        
        self.lbl_tgt_out = tk.Label(lang_frame)
        self.lbl_tgt_out.pack(side="left", padx=(10,0))
        self.tgt_lang_out = ttk.Combobox(lang_frame, values=["English", "Japanese", "Korean", "Chinese", "Thai"], state="readonly", width=12)
        self.tgt_lang_out.set("English")
        self.tgt_lang_out.pack(side="left", padx=5)

        self.mode_var_out = tk.StringVar(value="auto")
        mode_frame = tk.Frame(self.left_frame)
        mode_frame.pack(fill="x", pady=5)
        self.radio_auto = ttk.Radiobutton(mode_frame, variable=self.mode_var_out, value="auto", command=self.on_mode_change_out)
        self.radio_auto.pack(side="left")
        self.radio_push = ttk.Radiobutton(mode_frame, variable=self.mode_var_out, value="push", command=self.on_mode_change_out)
        self.radio_push.pack(side="left", padx=10)

        btn_frame = tk.Frame(self.left_frame)
        btn_frame.pack(pady=10)
        self.start_btn_out = tk.Button(btn_frame, bg="#4CAF50", fg="white", width=15, command=self.toggle_out_thread)
        self.start_btn_out.pack(side="left", padx=5)
        self.push_btn_out = tk.Button(btn_frame, bg="#2196F3", fg="white", width=15)
        self.push_btn_out.pack(side="left", padx=5)
        self.push_btn_out.bind("<ButtonPress-1>", self.start_push_record)
        self.push_btn_out.bind("<ButtonRelease-1>", self.stop_push_record)
        self.push_btn_out["state"] = "disabled"

        self.lbl_manual = tk.Label(self.left_frame)
        self.lbl_manual.pack(anchor="w")
        text_frame = tk.Frame(self.left_frame)
        text_frame.pack(fill="x", pady=(0, 10))
        self.manual_entry = ttk.Entry(text_frame)
        self.manual_entry.pack(side="left", expand=True, fill="x")
        self.manual_entry.bind("<Return>", lambda event: self.send_manual_text())
        self.btn_send = ttk.Button(text_frame, command=self.send_manual_text)
        self.btn_send.pack(side="left", padx=(5,0))

        self.lbl_log_out = tk.Label(self.left_frame)
        self.lbl_log_out.pack(anchor="w")
        self.log_area_out = scrolledtext.ScrolledText(self.left_frame, height=14, state='disabled', bg="#f4f4f4")
        self.log_area_out.pack(fill="both", expand=True, pady=5)

    def build_right_panel(self):
        self.lbl_speaker_in = tk.Label(self.right_frame)
        self.lbl_speaker_in.pack(anchor="w", pady=(5,0))
        self.mic_combo_in = ttk.Combobox(self.right_frame, values=self.mic_names, state="readonly")
        if self.mic_names: self.mic_combo_in.current(0)
        self.mic_combo_in.pack(fill="x", pady=5)

        lang_frame = tk.Frame(self.right_frame)
        lang_frame.pack(fill="x", pady=5)
        self.lbl_src_in = tk.Label(lang_frame)
        self.lbl_src_in.pack(side="left")
        self.src_lang_in = ttk.Combobox(lang_frame, values=["Japanese", "English", "Korean", "Chinese"], state="readonly", width=12)
        self.src_lang_in.set("Japanese")
        self.src_lang_in.pack(side="left", padx=5)
        
        self.lbl_tgt_in = tk.Label(lang_frame)
        self.lbl_tgt_in.pack(side="left", padx=(10,0))
        self.tgt_lang_in = ttk.Combobox(lang_frame, values=["Thai", "English", "Japanese", "Chinese", "Korean"], state="readonly", width=12)
        self.tgt_lang_in.set("Thai")
        self.tgt_lang_in.pack(side="left", padx=5)

        btn_frame = tk.Frame(self.right_frame)
        btn_frame.pack(pady=10)
        self.start_btn_in = tk.Button(btn_frame, bg="#4CAF50", fg="white", width=15, command=self.toggle_in_thread)
        self.start_btn_in.pack(side="left", padx=5)

        self.lbl_log_in = tk.Label(self.right_frame)
        self.lbl_log_in.pack(anchor="w")
        self.log_area_in = scrolledtext.ScrolledText(self.right_frame, height=21, state='disabled', bg="#eef9f0")
        self.log_area_in.pack(fill="both", expand=True, pady=5)

    def change_ui_language(self, event=None):
        lang_map = {"English": "en", "日本語": "ja"}
        sel = self.ui_lang_combo.get()
        self.current_ui_lang = lang_map.get(sel, "en")
        t = self.translations[self.current_ui_lang]

        self.root.title(t["title"])
        self.lbl_ui_lang.config(text=t["ui_lang"])
        self.lbl_api_key.config(text=t["api_key"])
        
        self.left_frame.config(text=t["left_frame"])
        self.right_frame.config(text=t["right_frame"])
        
        self.lbl_mic_out.config(text=t["mic_out"])
        self.lbl_src_out.config(text=t["src_lang_out"])
        self.lbl_tgt_out.config(text=t["tgt_lang_out"])
        self.radio_auto.config(text=t["mode_auto"])
        self.radio_push.config(text=t["mode_push"])
        
        if self.is_running_out:
            self.start_btn_out.config(text=t["btn_stop_out"])
        else:
            self.start_btn_out.config(text=t["btn_start_out"])
            
        self.push_btn_out.config(text=t["btn_hold"])
        self.lbl_manual.config(text=t["manual_label"])
        self.btn_send.config(text=t["btn_send"])
        self.lbl_log_out.config(text=t["log_out"])

        self.lbl_speaker_in.config(text=t["speaker_in"])
        self.lbl_src_in.config(text=t["src_lang_in"])
        self.lbl_tgt_in.config(text=t["tgt_lang_in"])
        
        if self.is_running_in:
            self.start_btn_in.config(text=t["btn_stop_in"])
        else:
            self.start_btn_in.config(text=t["btn_start_in"])
            
        self.lbl_log_in.config(text=t["log_in"])

    def log_out(self, message):
        self.log_area_out.config(state='normal')
        self.log_area_out.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_area_out.see(tk.END)
        self.log_area_out.config(state='disabled')

    def log_in(self, message):
        self.log_area_in.config(state='normal')
        self.log_area_in.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_area_in.see(tk.END)
        self.log_area_in.config(state='disabled')

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get("api_key"): self.api_key_entry.insert(0, data["api_key"])
            except Exception: pass

    def save_config(self, api_key):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump({"api_key": api_key}, f)

    def init_core_systems(self):
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showerror("Error", "Please enter Gemini API Key.")
            return False
        self.save_config(api_key)

        if not hasattr(self, 'gemini_client'):
            try:
                self.gemini_client = genai.Client(api_key=api_key)
                sys_instruct = """You are a pure translation API. Translate the text accurately and completely. Output ONLY the translated text. No filler."""
                safety_settings = [
                    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
                    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=types.HarmBlockThreshold.BLOCK_NONE),
                    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
                    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
                ]
                self.gen_config = types.GenerateContentConfig(temperature=0.2, system_instruction=sys_instruct, safety_settings=safety_settings)
            except Exception as e:
                messagebox.showerror("Error", f"Gemini Init Error: {e}")
                return False

        if not hasattr(self, 'whisper_model'):
            self.start_btn_out.config(state="disabled")
            self.start_btn_in.config(state="disabled")
            self.log_out("Loading Whisper Model... Please wait.")
            try:
                self.whisper_model = WhisperModel("medium", device="cuda", compute_type="float16")
                self.log_out("Whisper Model loaded!")
            except Exception as e:
                messagebox.showerror("Error", f"Whisper Init Error: {e}")
                self.start_btn_out.config(state="normal")
                self.start_btn_in.config(state="normal")
                return False
            self.start_btn_out.config(state="normal")
            self.start_btn_in.config(state="normal")
            
        return True

    # ================= OUTGOING SYSTEM =================
    def on_mode_change_out(self):
        if not self.is_running_out:
            self.push_btn_out["state"] = "disabled"
            return
        if self.mode_var_out.get() == "auto":
            self.push_btn_out["state"] = "disabled"
            threading.Thread(target=self.auto_listen_out, daemon=True).start()
        else:
            self.push_btn_out["state"] = "normal"

    def toggle_out_thread(self): threading.Thread(target=self.toggle_out, daemon=True).start()

    def toggle_out(self):
        t = self.translations[self.current_ui_lang]
        if not self.is_running_out:
            if not self.init_core_systems(): return
            self.is_running_out = True
            self.start_btn_out.config(text=t["btn_stop_out"], bg="#f44336")
            self.mic_combo_out.config(state="disabled")
            self.log_out(f"Started Outgoing Mic: {self.mic_combo_out.get()}")
            self.on_mode_change_out()
        else:
            self.is_running_out = False
            self.start_btn_out.config(text=t["btn_start_out"], bg="#4CAF50")
            self.mic_combo_out.config(state="readonly")
            self.push_btn_out["state"] = "disabled"
            self.log_out("Outgoing Stopped.")

    def auto_listen_out(self):
        mic_idx = self.mic_names.index(self.mic_combo_out.get())
        with sr.Microphone(device_index=mic_idx) as source:
            self.recognizer_out.adjust_for_ambient_noise(source, duration=0.5)
            self.log_out("Listening (Auto)...")
            while self.is_running_out and self.mode_var_out.get() == "auto":
                try:
                    audio = self.recognizer_out.listen(source, timeout=1, phrase_time_limit=10)
                    threading.Thread(target=self.process_audio, args=(audio, "out"), daemon=True).start()
                except sr.WaitTimeoutError: continue
                except Exception: pass

    def start_push_record(self, event):
        if not self.is_running_out or self.mode_var_out.get() != "push": return
        self.is_recording_out = True
        self.log_out("Recording...")
        threading.Thread(target=self.push_listen_out, daemon=True).start()

    def stop_push_record(self, event):
        if not self.is_running_out or self.mode_var_out.get() != "push": return
        self.is_recording_out = False
        self.log_out("Processing...")

    def push_listen_out(self):
        mic_idx = self.mic_names.index(self.mic_combo_out.get())
        with sr.Microphone(device_index=mic_idx) as source:
            try:
                audio = self.recognizer_out.listen(source, timeout=None, phrase_time_limit=15)
                self.process_audio(audio, "out")
            except Exception: pass

    # ================= MANUAL TEXT INPUT =================
    def send_manual_text(self):
        if not self.is_running_out:
            t = self.translations[self.current_ui_lang]
            messagebox.showwarning("Warning", t["warn_manual"])
            return
        text = self.manual_entry.get().strip()
        if text:
            self.manual_entry.delete(0, tk.END)
            self.log_out(f"Manual Input: {text}")
            threading.Thread(target=self.process_manual_translation, args=(text,), daemon=True).start()

    def process_manual_translation(self, text):
        tgt = self.tgt_lang_out.get()
        self.osc_client.send_message("/chatbox/typing", True)
        prompt = f"Translate exactly to {tgt}: {text}"

        try:
            response = self.gemini_client.models.generate_content(
                model='gemini-2.5-flash', contents=prompt, config=self.gen_config
            )
            translation = response.text.strip()
            result_text = f"{text}\n{translation}"
            
            self.log_out(f"Translated:\n{result_text}")
            self.send_to_vrchat(result_text)
        except Exception as e:
            if self.is_running_out: self.log_out(f"Error: {e}")
            self.osc_client.send_message("/chatbox/typing", False)

    # ================= INCOMING SYSTEM =================
    def toggle_in_thread(self): threading.Thread(target=self.toggle_in, daemon=True).start()

    def toggle_in(self):
        t = self.translations[self.current_ui_lang]
        if not self.is_running_in:
            if not self.init_core_systems(): return
            self.is_running_in = True
            self.start_btn_in.config(text=t["btn_stop_in"], bg="#f44336")
            self.mic_combo_in.config(state="disabled")
            self.log_in(f"Started Incoming Loopback: {self.mic_combo_in.get()}")
            threading.Thread(target=self.auto_listen_in, daemon=True).start()
        else:
            self.is_running_in = False
            self.start_btn_in.config(text=t["btn_start_in"], bg="#4CAF50")
            self.mic_combo_in.config(state="readonly")
            self.log_in("Incoming Stopped.")

    def auto_listen_in(self):
        mic_idx = self.mic_names.index(self.mic_combo_in.get())
        with sr.Microphone(device_index=mic_idx) as source:
            self.recognizer_in.adjust_for_ambient_noise(source, duration=0.5)
            self.log_in("Listening to Speaker...")
            while self.is_running_in:
                try:
                    audio = self.recognizer_in.listen(source, timeout=1, phrase_time_limit=15)
                    threading.Thread(target=self.process_audio, args=(audio, "in"), daemon=True).start()
                except sr.WaitTimeoutError: continue
                except Exception: pass

    # ================= SHARED PROCESSING =================
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

                segments, _ = self.whisper_model.transcribe(
                    audio_np, 
                    beam_size=5, 
                    language=lang_code, 
                    initial_prompt=stt_prompt,
                    vad_filter=True,
                    vad_parameters=dict(min_silence_duration_ms=500),
                    condition_on_previous_text=False 
                )
                
                valid_texts = []
                for segment in segments:
                    text = segment.text.strip()
                    if any(bad_word in text for bad_word in ["字幕", "視聴", "Subtitles", "視聴ありがとうございました"]):
                        continue
                    valid_texts.append(text)
                
                text = "".join(valid_texts).strip()

            if text:
                log_func(f"Heard: {text}")
                
                if source_type == "out": self.osc_client.send_message("/chatbox/typing", True)

                prompt = f"Translate exactly to {tgt}: {text}"
                response = self.gemini_client.models.generate_content(
                    model='gemini-2.5-flash', contents=prompt, config=self.gen_config
                )
                translation = response.text.strip()
                result_text = f"{text}\n{translation}"
                log_func(f"Translated:\n{result_text}")

                if source_type == "out":
                    self.send_to_vrchat(result_text)

        except Exception as e:
            if source_type == "out":
                if self.is_running_out: self.log_out(f"Error: {e}")
                self.osc_client.send_message("/chatbox/typing", False)
            else:
                if self.is_running_in: self.log_in(f"Error: {e}")

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
        codes = {"Thai": "th", "English": "en", "Japanese": "ja", "Korean": "ko", "Chinese": "zh"}
        return codes.get(lang_name, "en")

if __name__ == "__main__":
    root = tk.Tk()
    app = VRChatTranslatorApp(root)
    root.mainloop()