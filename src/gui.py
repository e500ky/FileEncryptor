import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
from typing import Callable, Optional
from .encryption import TextEncryptor
from .file_handler import FileHandler

class FileEncryptorGUI():
    def __init__(self):
        self.window = TkinterDnD.Tk()
        self.window.title("TXT Dosya Şifreleyici")
        self.window.geometry("850x720")
        self.window.iconbitmap("src/logo.ico")
        self.window.resizable(False, False)

        ctk.set_appearance_mode("dark")
        
        self.window.configure(bg="#1a1a1a")
        
        self.encryptor = TextEncryptor()
        self.file_handler = FileHandler()
        self.status_timer = None
        
        self._setup_ui()
        self._setup_drag_drop()

    def _clear_status(self):
        self.status_label.configure(text="")
        self.status_timer = None

    def _update_status(self, message: str, duration: int = 3000):
        self.status_label.configure(text=message)
        
        if self.status_timer:
            self.window.after_cancel(self.status_timer)
        
        self.status_timer = self.window.after(duration, self._clear_status)

    def _setup_ui(self):
        self.main_frame = ctk.CTkFrame(
            self.window,
            fg_color="transparent",
            corner_radius=0
        )
        self.main_frame.pack(fill="both", expand=True)
        
        self.content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#2b2b2b",
            corner_radius=15
        )
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.title_label = ctk.CTkLabel(
            self.content_frame,
            text="TXT Dosya Şifreleyici",
            font=("Helvetica", 28, "bold"),
            text_color="#ffffff"
        )
        self.title_label.pack(pady=(30, 20))
        
        self.drop_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="#1f2937",
            corner_radius=10,
            height=100
        )
        self.drop_frame.pack(fill="x", padx=40, pady=20)
        
        self.drop_label = ctk.CTkLabel(
            self.drop_frame,
            text="Dosyayı buraya sürükleyin veya aşağıdaki butonu kullanın",
            font=("Helvetica", 13),
            text_color="#9ca3af"
        )
        self.drop_label.pack(pady=20)
        
        self.select_button = ctk.CTkButton(
            self.content_frame,
            text="Dosya Seç",
            command=self._select_file,
            font=("Helvetica", 14),
            height=40,
            corner_radius=10,
            fg_color="#3b82f6",
            hover_color="#2563eb"
        )
        self.select_button.pack(pady=10)
        
        self.file_info_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.file_info_frame.pack(pady=10)
        
        self.remove_button = ctk.CTkButton(
            self.file_info_frame,
            text="✕",
            command=self._remove_file,
            font=("Helvetica", 12),
            width=25,
            height=25,
            corner_radius=5,
            fg_color="#ef4444",
            hover_color="#b91c1c",
            state="disabled"
        )
        self.remove_button.pack(side="left", padx=10)
        self.remove_button.pack_forget()
       
        self.file_label = ctk.CTkLabel(
            self.file_info_frame,
            text="Henüz dosya seçilmedi",
            font=("Helvetica", 13),
            text_color="#9ca3af"
        )
        self.file_label.pack(side="left", padx=(1, 0))
        
        self.key_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.key_frame.pack(fill="x", padx=40, pady=20)
        
        self.key_container = ctk.CTkFrame(
            self.key_frame,
            fg_color="transparent"
        )
        self.key_container.pack(expand=True)
        
        self.key_label = ctk.CTkLabel(
            self.key_container,
            text="Şifreleme Anahtarı:",
            font=("Helvetica", 14),
            text_color="#ffffff"
        )
        self.key_label.pack(side="left", padx=5)
        
        self.key_entry = ctk.CTkEntry(
            self.key_container,
            show="*",
            width=250,
            height=40,
            font=("Helvetica", 13),
            corner_radius=10,
            fg_color="#1f2937",
            border_color="#3b82f6",
            text_color="#ffffff"
        )
        self.key_entry.pack(side="left", padx=5)
        
        self.button_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.button_frame.pack(pady=20)
        
        self.encrypt_button = ctk.CTkButton(
            self.button_frame,
            text="Şifrele",
            command=self._encrypt_file,
            state="disabled",
            font=("Helvetica", 14, "bold"),
            height=45,
            width=150,
            corner_radius=10,
            fg_color="#31d645",
            hover_color="#19d42f"
        )
        self.encrypt_button.pack(side="left", padx=10)
        
        self.decrypt_button = ctk.CTkButton(
            self.button_frame,
            text="Şifre Çöz",
            command=self._decrypt_file,
            state="disabled",
            font=("Helvetica", 14, "bold"),
            height=45,
            width=150,
            corner_radius=10,
            fg_color="#e01d1d",
            hover_color="#ed1313"
        )
        self.decrypt_button.pack(side="left", padx=10)
        
        self.status_label = ctk.CTkLabel(
            self.content_frame,
            text="",
            font=("Helvetica", 13),
            text_color="#9ca3af"
        )
        self.status_label.pack(pady=10)

    def _setup_drag_drop(self):
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self._handle_drop)

    def _handle_drop(self, event):
        file_path = event.data
        if file_path.startswith('{'):
            file_path = file_path[1:-1]
        if self.file_handler.is_valid_txt_file(file_path):
            self._load_file(file_path)
            
        else:
            messagebox.showerror("Hata", "Lütfen geçerli bir .txt dosyası seçin!")

    def _select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")]
        )
        if file_path:
            self._load_file(file_path)
            
        self.remove_button.pack(side="left", padx=10)

    def _remove_file(self):
        self.file_handler.clear()
        self.file_label.configure(text="Henüz dosya seçilmedi")
        self.encrypt_button.configure(state="disabled")
        self.decrypt_button.configure(state="disabled")
        self.remove_button.configure(state="disabled")
        self._update_status("Dosya kaldırıldı")
        self.remove_button.pack_forget()

    def _load_file(self, file_path: str):
        if self.file_handler.read_file(file_path):
            self.file_label.configure(text=os.path.basename(file_path))
            encrypted = False
            try:
                from .encryption import TextEncryptor
                encryptor = TextEncryptor()
                keyfile_path = encryptor._get_keyfile_path(file_path)
                if os.path.exists(keyfile_path):
                    encrypted = True
            except Exception:
                encrypted = False
            if encrypted:
                self.encrypt_button.configure(state="disabled")
                self._update_status("Bu dosya zaten şifrelenmiş! Tekrar şifrelenemez.")
            else:
                self.encrypt_button.configure(state="normal")
            self.decrypt_button.configure(state="normal")
            self.remove_button.pack(side="left", padx=10)
            self.remove_button.configure(state="normal")
            self._update_status("Dosya başarıyla yüklendi")
        else:
            messagebox.showerror("Hata", "Dosya okunamadı!")

    def _encrypt_file(self):
        key = self.key_entry.get()
        if not key:
            messagebox.showerror("Hata", "Lütfen bir şifreleme anahtarı girin!")
            return
        
        file_path = self.file_handler.current_file
        self.encryptor.set_key(key, file_path)
        
        if self.file_handler.is_file_encrypted():
            content = self.file_handler.get_original_content()
        else:
            content = self.file_handler.get_file_content()
            self.file_handler.original_content = content
        
        if content:
            try:
                encrypted_content = self.encryptor.encrypt(content)
                if self.file_handler.write_file(encrypted_content):
                    
                    self.file_handler.set_encrypted(True)
                    self._update_status("Dosya başarıyla şifrelendi!")
                    messagebox.showinfo("Başarılı", "Dosya başarıyla şifrelendi!")
                    self.encrypt_button.configure(state="disabled")
                else:
                    messagebox.showerror("Hata", "Dosya yazılamadı!")
            except Exception as e:
                messagebox.showerror("Hata", f"Şifreleme hatası: {str(e)}")

    def _decrypt_file(self):
        key = self.key_entry.get()
        if not key:
            messagebox.showerror("Hata", "Lütfen bir şifreleme anahtarı girin!")
            return
        
        file_path = self.file_handler.current_file
        self.encryptor.key = key
        
        if self.file_handler.is_file_encrypted():
            content = self.file_handler.get_file_content()
        else:
            content = self.file_handler.get_original_content()
        
        if content:
            try:
                decrypted_content = self.encryptor.decrypt(content, file_path)
                if self.file_handler.write_file(decrypted_content):
                    
                    self.file_handler.set_encrypted(False)
                    self._update_status("Dosya başarıyla çözüldü!")
                    messagebox.showinfo("Başarılı", "Dosya başarıyla çözüldü!")
                    self.encrypt_button.configure(state="normal")
                else:
                    messagebox.showerror("Hata", "Dosya yazılamadı!")
            except Exception as e:
                messagebox.showerror("Hata", f"Şifre çözme hatası: {str(e)}")
            except ValueError as ve:
                messagebox.showerror("Hata", f"Anahtar uyuşmuyor: {str(ve)}")

    def run(self):
        self.window.mainloop()
