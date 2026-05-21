# -*- coding: utf-8 -*-
"""
HỆ THỐNG MÃ HÓA NGÂN HÀNG - CYBERBANK DEFENSE GAME
Mô-đun mật mã học (CryptoEngine)
"""

from datetime import datetime
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes

class CryptoEngine:
    """Bộ máy xử lý mật mã học của Ngân hàng (AES-GCM, RSA-PSS, SHA-512, Anti-Replay)"""
    def __init__(self):
        # Khởi tạo khóa RSA cho Ngân hàng nhận (Receiver Bank)
        # Sử dụng kích thước khóa 2048-bit để đảm bảo an toàn cao
        self.bank_key = RSA.generate(2048)
        self.bank_private_key = self.bank_key.export_key()
        self.bank_public_key = self.bank_key.publickey().export_key()
        
        # Danh sách lưu các Nonce đã sử dụng để chống tấn công phát lại (Anti-replay Registry)
        self.nonce_registry = set()
        
        # Khóa phiên đối xứng dùng chung (Session Key) - AES 128-bit
        self.session_key = get_random_bytes(16)

    def generate_client_rsa_key(self):
        """Tạo cặp khóa RSA cho khách hàng gửi (Sender Client)"""
        client_key = RSA.generate(2048)
        private_key = client_key.export_key()
        public_key = client_key.publickey().export_key()
        return private_key, public_key

    def sign_metadata(self, sender, timestamp, nonce, client_private_key):
        """Ký số metadata giao dịch bằng RSA-PSS kết hợp SHA-512 (Chứng thực danh tính & Chống chối bỏ)"""
        metadata = f"{sender}|{timestamp}|{nonce}"
        key = RSA.import_key(client_private_key)
        h = SHA512.new(metadata.encode('utf-8'))
        signer = pss.new(key)
        signature = signer.sign(h)
        return signature

    def verify_metadata_signature(self, sender, timestamp, nonce, signature, client_public_key):
        """Xác minh chữ ký số RSA-PSS của khách hàng gửi"""
        metadata = f"{sender}|{timestamp}|{nonce}"
        try:
            key = RSA.import_key(client_public_key)
            h = SHA512.new(metadata.encode('utf-8'))
            verifier = pss.new(key)
            verifier.verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False

    def encrypt_transaction_details(self, plaintext, session_key):
        """Mã hóa thông tin giao dịch bằng thuật toán đối xứng nâng cao AES-GCM (Đảm bảo tính Bí mật & Xác thực AEAD)"""
        cipher = AES.new(session_key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode('utf-8'))
        # Trả về ciphertext, tag (MAC check), và nonce tự động tạo của GCM
        return ciphertext, tag, cipher.nonce

    def decrypt_transaction_details(self, ciphertext, tag, nonce, session_key):
        """Giải mã và xác thực tính toàn vẹn của giao dịch bằng AES-GCM"""
        try:
            cipher = AES.new(session_key, AES.MODE_GCM, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            return plaintext.decode('utf-8')
        except ValueError:
            # Nếu tag không khớp (dữ liệu bị thay đổi dù chỉ 1 byte), AES-GCM sẽ báo lỗi ngay lập tức
            raise ValueError("LỖI XÁC THỰC MẬT MÃ (MAC check failed): Ciphertext bị sửa đổi hoặc sai khóa!")

    def calculate_sha512_hash(self, ciphertext, timestamp):
        """Tính mã băm SHA-512 cho bản mã kèm thời gian để kiểm tra tính toàn vẹn tối đa"""
        ciphertext_bytes = ciphertext.encode('utf-8') if isinstance(ciphertext, str) else ciphertext
        timestamp_bytes = timestamp.encode('utf-8') if isinstance(timestamp, str) else timestamp
        data = ciphertext_bytes + timestamp_bytes
        h = SHA512.new(data)
        return h.hexdigest()

    def check_anti_replay(self, nonce, timestamp_str, max_age_seconds=15):
        """Cơ chế phòng thủ chủ động Anti-replay bằng cách kiểm tra Nonce trùng lặp và Timestamp hết hạn"""
        # 1. Kiểm tra Nonce trùng lặp
        if nonce in self.nonce_registry:
            raise Exception(f"TẤN CÔNG PHÁT LẠI PHÁT HIỆN: Nonce '{nonce[:10]}...' đã tồn tại trong Database của Ngân hàng!")
            
        # 2. Kiểm tra Timestamp hết hạn
        try:
            tx_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            now_time = datetime.now()
            age = (now_time - tx_time).total_seconds()
            
            if age > max_age_seconds:
                raise Exception(f"LỖI THỜI GIAN HẾT HẠN: Giao dịch đã được tạo trước đó {age:.1f} giây (Giới hạn cho phép: {max_age_seconds} giây).")
        except ValueError:
            raise Exception("LỖI ĐỊNH DẠNG: Định dạng thời gian (timestamp) không hợp lệ.")
            
        # Nếu hợp lệ, ghi nhận nonce vào Database
        self.nonce_registry.add(nonce)
        return True
