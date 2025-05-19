import pickle
import os
import hashlib

class TextEncryptor:
    def __init__(self):
        self.key = None

    def _get_keyfile_path(self, file_path: str) -> str:
        base_path = file_path.replace('(Şifrelendi)', '')
        file_hash = hashlib.sha256(base_path.encode('utf-8')).hexdigest()
        key_file = f"key_{file_hash}.pickle"
        key_path = os.path.join(os.path.expanduser('~'), '.encryptor', key_file)
        return key_path

    def set_key(self, key: str, file_path: str):
        self.key = key
        key_path = self._get_keyfile_path(file_path)
        os.makedirs(os.path.dirname(key_path), exist_ok=True)
        with open(key_path, 'wb') as f:
            pickle.dump(self.key, f)

    def _process_key(self, text_length: int) -> list:
        if not self.key:
            raise ValueError("Şifreleme anahtarı ayarlanmamış!")
        
        key_bytes = [ord(c) for c in self.key]
        return [key_bytes[i % len(key_bytes)] for i in range(text_length)]

    def encrypt(self, text: str) -> str:
        if not text:
            return ""
        
        text_bytes = [ord(c) for c in text]
        key_bytes = self._process_key(len(text_bytes))
        
        encrypted_bytes = []
        for i in range(len(text_bytes)):
            encrypted_byte = text_bytes[i] ^ key_bytes[i]
            encrypted_bytes.append(encrypted_byte)
        
        return ''.join(chr(b) for b in encrypted_bytes)

    def decrypt(self, encrypted_text: str, file_path: str) -> str:
        if not encrypted_text:
            return ""
        
        if not self.key:
            raise ValueError("Şifreleme anahtarı ayarlanmamış!")
        
        key_path = self._get_keyfile_path(file_path)
        
        try:
            with open(key_path, 'rb') as f:
                saved_key = pickle.load(f)
                
            if saved_key != self.key:
                raise ValueError("Anahtar uyuşmuyor!")
        except (FileNotFoundError, pickle.PickleError):
            raise ValueError("Anahtar dosyası bulunamadı veya bozuk!")
        
        text_bytes = [ord(c) for c in encrypted_text]
        key_bytes = self._process_key(len(text_bytes))
        
        decrypted_bytes = []
        for i in range(len(text_bytes)):
            decrypted_byte = text_bytes[i] ^ key_bytes[i]
            decrypted_bytes.append(decrypted_byte)
        
        try:
            os.remove(key_path)
        except Exception:
            pass
        
        return ''.join(chr(b) for b in decrypted_bytes)
