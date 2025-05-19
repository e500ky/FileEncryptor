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

        # Tema ayarları
        ctk.set_appearance_mode("dark")
        
        # Pencere arka plan rengini ayarla
        self.window.configure(bg="#1a1a1a")
        
        self.encryptor = TextEncryptor()
        self.file_handler = FileHandler()
        self.status_timer = None
        
        self._setup_ui()
        self._setup_drag_drop()

    def _clear_status(self):
        """Durum mesajını temizler"""
        self.status_label.configure(text="")
        self.status_timer = None

    def _update_status(self, message: str, duration: int = 3000):
        """Durum mesajını günceller ve belirli süre sonra temizler"""
        self.status_label.configure(text=message)
        
        # Önceki zamanlayıcıyı iptal et
        if self.status_timer:
            self.window.after_cancel(self.status_timer)
        
        # Yeni zamanlayıcı ayarla
        self.status_timer = self.window.after(duration, self._clear_status)

    def _setup_ui(self):
        """Arayüz bileşenlerini oluşturur"""
        # Ana frame
        self.main_frame = ctk.CTkFrame(
            self.window,
            fg_color="transparent",
            corner_radius=0
        )
        self.main_frame.pack(fill="both", expand=True)
        
        # İçerik frame'i
        self.content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#2b2b2b",
            corner_radius=15
        )
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Başlık
        self.title_label = ctk.CTkLabel(
            self.content_frame,
            text="TXT Dosya Şifreleyici",
            font=("Helvetica", 28, "bold"),
            text_color="#ffffff"
        )
        self.title_label.pack(pady=(30, 20))
        
        # Sürükle-bırak alanı
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
        
        # Dosya seçme butonu
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
        
        # Dosya bilgisi frame'i
        self.file_info_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.file_info_frame.pack(pady=10)
        
        # Dosya kaldırma butonu
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
       
        # Dosya yolu etiketi
        self.file_label = ctk.CTkLabel(
            self.file_info_frame,
            text="Henüz dosya seçilmedi",
            font=("Helvetica", 13),
            text_color="#9ca3af"
        )
        self.file_label.pack(side="left", padx=(1, 0))
        
        # Şifreleme anahtarı girişi
        self.key_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.key_frame.pack(fill="x", padx=40, pady=20)
        
        # Anahtar girişi için container frame
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
        
        # Butonlar için frame
        self.button_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.button_frame.pack(pady=20)
        
        # Şifreleme butonu
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
        
        # Şifre çözme butonu
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
        
        # Durum etiketi
        self.status_label = ctk.CTkLabel(
            self.content_frame,
            text="",
            font=("Helvetica", 13),
            text_color="#9ca3af"
        )
        self.status_label.pack(pady=10)

    def _setup_drag_drop(self):
        """Sürükle-bırak özelliğini ayarlar"""
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self._handle_drop)

    def _handle_drop(self, event):
        """Sürüklenen dosyayı işler"""
        file_path = event.data
        # Windows'ta dosya yolu düzeltmesi
        if file_path.startswith('{'):
            file_path = file_path[1:-1]
        if self.file_handler.is_valid_txt_file(file_path):
            self._load_file(file_path)
        else:
            messagebox.showerror("Hata", "Lütfen geçerli bir .txt dosyası seçin!")

    def _select_file(self):
        """Dosya seçme dialogunu açar"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")]
        )
        if file_path:
            self._load_file(file_path)
            
        self.remove_button.pack(side="left", padx=10)

    def _remove_file(self):
        """Seçili dosyayı kaldırır"""
        self.file_handler.clear()
        self.file_label.configure(text="Henüz dosya seçilmedi")
        self.encrypt_button.configure(state="disabled")
        self.decrypt_button.configure(state="disabled")
        self.remove_button.configure(state="disabled")
        self._update_status("Dosya kaldırıldı")
        self.remove_button.pack_forget()

    def _load_file(self, file_path: str):
        """Dosyayı yükler ve arayüzü günceller"""
        if self.file_handler.read_file(file_path):
            self.file_label.configure(text=os.path.basename(file_path))
            self.encrypt_button.configure(state="normal")
            self.decrypt_button.configure(state="normal")
            self.remove_button.configure(state="normal")
            self._update_status("Dosya başarıyla yüklendi")
        else:
            messagebox.showerror("Hata", "Dosya okunamadı!")

    def _encrypt_file(self):
        """Dosyayı şifreler"""
        key = self.key_entry.get()
        if not key:
            messagebox.showerror("Hata", "Lütfen bir şifreleme anahtarı girin!")
            return
        
        file_path = self.file_handler.current_file
        self.encryptor.set_key(key, file_path)  # Sadece şifrelerken anahtarı kaydet
        
        # Dosya zaten şifreliyse orijinal içeriği kullan
        if self.file_handler.is_file_encrypted():
            content = self.file_handler.get_original_content()
        else:
            content = self.file_handler.get_file_content()
            # Orijinal içeriği kaydet
            self.file_handler.original_content = content
        
        if content:
            try:
                encrypted_content = self.encryptor.encrypt(content)
                if self.file_handler.write_file(encrypted_content):
                    
                    self.file_handler.set_encrypted(True)
                    self._update_status("Dosya başarıyla şifrelendi!")
                    messagebox.showinfo("Başarılı", "Dosya başarıyla şifrelendi!")
                else:
                    messagebox.showerror("Hata", "Dosya yazılamadı!")
            except Exception as e:
                messagebox.showerror("Hata", f"Şifreleme hatası: {str(e)}")

    def _decrypt_file(self):
        """Dosyayı şifresini çözer"""
        key = self.key_entry.get()
        if not key:
            messagebox.showerror("Hata", "Lütfen bir şifreleme anahtarı girin!")
            return
        
        file_path = self.file_handler.current_file
        self.encryptor.key = key  # Sadece bellekte anahtarı ayarla, dosyaya kaydetme!
        
        if self.file_handler.is_file_encrypted():
            # Şifrelenmiş dosyayı çöz
            content = self.file_handler.get_file_content()
        else:
            # Dosya şifreli değilse orijinal içeriği kullan
            content = self.file_handler.get_original_content()
        
        if content:
            try:
                decrypted_content = self.encryptor.decrypt(content, file_path)
                if self.file_handler.write_file(decrypted_content):
                    
                    self.file_handler.set_encrypted(False)
                    self._update_status("Dosya başarıyla çözüldü!")
                    messagebox.showinfo("Başarılı", "Dosya başarıyla çözüldü!")
                else:
                    messagebox.showerror("Hata", "Dosya yazılamadı!")
            except Exception as e:
                messagebox.showerror("Hata", f"Şifre çözme hatası: {str(e)}")
            except ValueError as ve:
                messagebox.showerror("Hata", f"Anahtar uyuşmuyor: {str(ve)}")

    def run(self):
        """Uygulamayı başlatır"""
        self.window.mainloop()