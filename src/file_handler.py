from typing import Optional
import os

class FileHandler:
    def __init__(self):
        self.current_file: Optional[str] = None
        self.file_content: Optional[str] = None
        self.original_content: Optional[str] = None
        self.is_processing: bool = False
        self.is_encrypted: bool = False
        self.original_filename: Optional[str] = None

    def read_file(self, file_path: str) -> bool:
        """Dosyayı okur ve içeriğini saklar"""
        try:
            if not file_path.lower().endswith('.txt'):
                return False
            
            with open(file_path, 'r', encoding='utf-8') as file:
                self.file_content = file.read()
                self.original_content = self.file_content
                self.current_file = file_path
                self.original_filename = file_path
                self.is_encrypted = False
                return True
        except Exception as e:
            print(f"Dosya okuma hatası: {str(e)}")
            return False

    def write_file(self, content: str, file_path: Optional[str] = None) -> bool:
        """İçeriği dosyaya yazar"""
        try:
            target_path = file_path or self.current_file
            if not target_path:
                return False

            with open(target_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            self.file_content = content
            return True
        except Exception as e:
            print(f"Dosya yazma hatası: {str(e)}")
            return False

    def rename_file_when_encrypted(self) -> bool:
        """Dosya şifrelendiğinde adını değiştirir"""
        if not self.current_file:
            return False
        
        # Zaten şifrelenmiş ise işlem yapma
        if "(Şifrelendi)" in self.current_file:
            return True
            
        dir_name = os.path.dirname(self.current_file)
        file_name = os.path.basename(self.current_file)
        name, ext = os.path.splitext(file_name)
        
        encrypted_name = f"{name}{ext}"
        encrypted_path = os.path.join(dir_name, encrypted_name)
        
        try:
            # Eğer aynı isimde bir dosya varsa, onu sil
            if os.path.exists(encrypted_path):
                os.remove(encrypted_path)
                
            # Dosyayı yeniden adlandır
            os.rename(self.current_file, encrypted_path)
            self.current_file = encrypted_path
            return True
        except Exception as e:
            print(f"Dosya adı değiştirme hatası: {str(e)}")
            return False
    
    def rename_file_when_decrypted(self) -> bool:
        """Dosya şifresi çözüldüğünde adını orijinal adına çevirir"""
        if not self.current_file:
            return False
            
        # Şifrelenmiş değilse işlem yapma
        if "(Şifrelendi)" not in self.current_file:
            return True
            
        dir_name = os.path.dirname(self.current_file)
        file_name = os.path.basename(self.current_file)
        
        # (Şifrelendi) kısmını kaldır
        decrypted_name = file_name.replace("(Şifrelendi)", "")
        decrypted_path = os.path.join(dir_name, decrypted_name)
        
        try:
            # Eğer aynı isimde bir dosya varsa, onu sil
            if os.path.exists(decrypted_path):
                os.remove(decrypted_path)
                
            # Dosyayı yeniden adlandır
            os.rename(self.current_file, decrypted_path)
            self.current_file = decrypted_path
            return True
        except Exception as e:
            print(f"Dosya adı değiştirme hatası: {str(e)}")
            return False

    def get_file_content(self) -> Optional[str]:
        """Mevcut dosya içeriğini döndürür"""
        return self.file_content
    
    def get_original_content(self) -> Optional[str]:
        """Orijinal dosya içeriğini döndürür"""
        return self.original_content

    def set_encrypted(self, is_encrypted: bool):
        """Dosyanın şifrelenmiş olup olmadığını ayarlar"""
        self.is_encrypted = is_encrypted

    def is_file_encrypted(self) -> bool:
        """Dosyanın şifrelenmiş olup olmadığını döndürür"""
        return self.is_encrypted

    def clear(self):
        """Mevcut dosya ve içeriği temizler"""
        self.current_file = None
        self.file_content = None
        self.original_content = None
        self.is_processing = False
        self.is_encrypted = False
        self.original_filename = None

    def is_valid_txt_file(self, file_path: str) -> bool:
        """Dosyanın geçerli bir .txt dosyası olup olmadığını kontrol eder"""
        return os.path.isfile(file_path) and file_path.lower().endswith('.txt') 