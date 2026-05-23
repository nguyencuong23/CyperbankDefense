# -*- coding: utf-8 -*-
"""
HỆ THỐNG MÃ HÓA NGÂN HÀNG - CYBERBANK DEFENSE GAME
Mixin quản lý Tab 2: Phòng thử nghiệm tấn công (LabTabMixin)
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import time
import uuid
from datetime import datetime, timedelta

from config import (
    BG_MAIN, BG_PANEL, BG_CARD, ACCENT, SUCCESS, WARNING, DANGER,
    TEXT_LIGHT, TEXT_DARK, TERMINAL_BG
)

class LabTabMixin:
    """Mixin cung cấp giao diện và lô-gích của phòng thử nghiệm tấn công cho BankingApp"""
    
    def setup_tab_lab(self):
        self.tab_lab.columnconfigure(0, weight=1)
        self.tab_lab.columnconfigure(1, weight=1)
        self.tab_lab.rowconfigure(0, weight=1)
        
        # --- CỘT TRÁI: KHU VỰC CỦA HACKER (SIMULATION) ---
        frame_hacker = tk.Frame(self.tab_lab, bg=BG_PANEL, bd=1, relief="solid")
        frame_hacker.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        tk.Label(frame_hacker, text="👹 KHU VỰC KHỞI TẠO & GIẢ LẬP TẤN CÔNG", font=("Helvetica", 12, "bold"), fg=DANGER, bg=BG_PANEL).pack(pady=10)
        
        # Form nhập liệu giao dịch
        frame_form = tk.Frame(frame_hacker, bg=BG_PANEL)
        frame_form.pack(fill="x", padx=20, pady=5)
        
        tk.Label(frame_form, text="Người gửi (Sender):", font=("Helvetica", 10), fg=TEXT_LIGHT, bg=BG_PANEL).grid(row=0, column=0, sticky="w", pady=5)
        self.ent_lab_sender = tk.Entry(frame_form, font=("Helvetica", 10), bg=BG_CARD, fg=TEXT_LIGHT, width=25, insertbackground=TEXT_LIGHT)
        self.ent_lab_sender.insert(0, "Hacker_Anonymous")
        self.ent_lab_sender.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(frame_form, text="Người nhận (Receiver):", font=("Helvetica", 10), fg=TEXT_LIGHT, bg=BG_PANEL).grid(row=1, column=0, sticky="w", pady=5)
        self.ent_lab_receiver = tk.Entry(frame_form, font=("Helvetica", 10), bg=BG_CARD, fg=TEXT_LIGHT, width=25, insertbackground=TEXT_LIGHT)
        self.ent_lab_receiver.insert(0, "Hacker_Destination")
        self.ent_lab_receiver.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(frame_form, text="Số tiền ($):", font=("Helvetica", 10), fg=TEXT_LIGHT, bg=BG_PANEL).grid(row=2, column=0, sticky="w", pady=5)
        self.ent_lab_amount = tk.Entry(frame_form, font=("Helvetica", 10), bg=BG_CARD, fg=TEXT_LIGHT, width=25, insertbackground=TEXT_LIGHT)
        self.ent_lab_amount.insert(0, "$999000")
        self.ent_lab_amount.grid(row=2, column=1, padx=10, pady=5)
        
        # Các nút tạo gói tin
        btn_gen_normal = tk.Button(frame_hacker, text="🛡️ Bước 1: Khởi tạo Giao dịch & Ký số (Hợp lệ)", font=("Helvetica", 10, "bold"), bg=ACCENT, fg="white", activebackground=ACCENT, relief="flat", command=self.lab_generate_valid)
        btn_gen_normal.pack(fill="x", padx=30, pady=10)
        
        # Các tùy chọn tấn công
        lbl_attack_title = tk.Label(frame_hacker, text="CẤU HÌNH PHƯƠNG THỨC TẤN CÔNG (ATTACK INTERFACE):", font=("Helvetica", 10, "bold"), fg=WARNING, bg=BG_PANEL)
        lbl_attack_title.pack(anchor="w", padx=20, pady=10)
        
        frame_attack_options = tk.Frame(frame_hacker, bg=BG_PANEL)
        frame_attack_options.pack(fill="x", padx=20, pady=5)
        
        self.lab_attack_var = tk.StringVar(value="NONE")
        
        tk.Radiobutton(frame_attack_options, text="Không tấn công (Giao dịch gửi đi hợp lệ)", font=("Helvetica", 9), variable=self.lab_attack_var, value="NONE", bg=BG_PANEL, fg=TEXT_LIGHT, selectcolor=BG_PANEL, activebackground=BG_PANEL).pack(anchor="w", pady=2)
        tk.Radiobutton(frame_attack_options, text="Sửa đổi dữ liệu (Tamper 1 byte trong Ciphertext)", font=("Helvetica", 9), variable=self.lab_attack_var, value="TAMPER", bg=BG_PANEL, fg=TEXT_LIGHT, selectcolor=BG_PANEL, activebackground=BG_PANEL).pack(anchor="w", pady=2)
        tk.Radiobutton(frame_attack_options, text="Tấn công phát lại (Replay cùng mã Nonce cũ đã dùng)", font=("Helvetica", 9), variable=self.lab_attack_var, value="REPLAY", bg=BG_PANEL, fg=TEXT_LIGHT, selectcolor=BG_PANEL, activebackground=BG_PANEL).pack(anchor="w", pady=2)
        tk.Radiobutton(frame_attack_options, text="Làm trễ/Hết hạn thời gian (Gửi gói tin sau 10 phút)", font=("Helvetica", 9), variable=self.lab_attack_var, value="EXPIRE", bg=BG_PANEL, fg=TEXT_LIGHT, selectcolor=BG_PANEL, activebackground=BG_PANEL).pack(anchor="w", pady=2)
        tk.Radiobutton(frame_attack_options, text="Ký số giả mạo (Sử dụng khóa RSA sai/khác)", font=("Helvetica", 9), variable=self.lab_attack_var, value="WRONG_KEY", bg=BG_PANEL, fg=TEXT_LIGHT, selectcolor=BG_PANEL, activebackground=BG_PANEL).pack(anchor="w", pady=2)
        
        # Nút thực hiện tấn công và gửi đến ngân hàng
        btn_send_attack = tk.Button(frame_hacker, text="⚡ GỬI GIAO DỊCH ĐẾN CỔNG THANH TOÁN BANK", font=("Helvetica", 11, "bold"), bg=DANGER, fg="white", activebackground=DANGER, relief="flat", command=self.lab_send_to_bank)
        btn_send_attack.pack(fill="x", padx=30, pady=20)

        # --- CỘT PHẢI: PHẢN ỨNG CỦA CỔNG BẢO MẬT NGÂN HÀNG ---
        frame_defender = tk.Frame(self.tab_lab, bg=BG_MAIN)
        frame_defender.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        tk.Label(frame_defender, text="🏦 CỔNG BẢO MẬT & PHÂN TÍCH LỖI NGÂN HÀNG", font=("Helvetica", 12, "bold"), fg=SUCCESS, bg=BG_MAIN).pack(pady=10)
        
        # Màn hình Terminal phân tích của Cổng Thanh toán
        self.txt_lab_terminal = scrolledtext.ScrolledText(frame_defender, bg=TERMINAL_BG, fg=TEXT_LIGHT, font=("Courier New", 9), height=25)
        self.txt_lab_terminal.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Nút xóa terminal log
        btn_clear_lab = tk.Button(frame_defender, text="Dọn sạch Terminal", font=("Helvetica", 9), bg=BG_CARD, fg=TEXT_LIGHT, relief="flat", command=self.lab_clear_terminal)
        btn_clear_lab.pack(anchor="e", padx=10, pady=5)
        
        # Dữ liệu nội bộ Sandbox
        self.lab_tx_data = None
        self.lab_client_priv, self.lab_client_pub = self.crypto.generate_client_rsa_key()

    def lab_log(self, message, level="info"):
        """Ghi log vào terminal sandbox"""
        self.txt_lab_terminal.config(state="normal")
        now = datetime.now().strftime("%H:%M:%S")
        prefix = f"[{now}] "
        
        if level == "success":
            color = "#10B981"  # Green
            tag = "l_success"
        elif level == "error":
            color = "#EF4444"  # Red
            tag = "l_error"
        elif level == "warning":
            color = "#F59E0B"  # Yellow
            tag = "l_warn"
        else:
            color = "#38BDF8"  # Blue
            tag = "l_info"
            
        self.txt_lab_terminal.insert(tk.END, prefix + message + "\n", tag)
        self.txt_lab_terminal.tag_config(tag, foreground=color)
        self.txt_lab_terminal.see(tk.END)
        self.txt_lab_terminal.config(state="disabled")

    def lab_clear_terminal(self):
        self.txt_lab_terminal.config(state="normal")
        self.txt_lab_terminal.delete("1.0", tk.END)
        self.txt_lab_terminal.config(state="disabled")

    def lab_generate_valid(self):
        """Sandbox: Tạo giao dịch gốc hợp lệ đầy đủ chữ ký và mã hóa"""
        sender = self.ent_lab_sender.get().strip()
        receiver = self.ent_lab_receiver.get().strip()
        amount = self.ent_lab_amount.get().strip()
        
        if not sender or not receiver or not amount:
            messagebox.showerror("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin giao dịch!", parent=self)
            return
            
        nonce = uuid.uuid4().hex
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        plaintext = f"{sender}->{receiver}:{amount}"
        
        # AES-GCM Encryption
        ciphertext_bytes, tag_bytes, gcm_nonce = self.crypto.encrypt_transaction_details(plaintext, self.crypto.session_key)
        ciphertext_packet = f"{ciphertext_bytes.hex()}:{tag_bytes.hex()}:{gcm_nonce.hex()}"
        
        # RSA-PSS Sign
        signature_bytes = self.crypto.sign_metadata(sender, timestamp_str, nonce, self.lab_client_priv)
        
        # SHA-512 Hash
        hash_val = self.crypto.calculate_sha512_hash(ciphertext_packet, timestamp_str)
        
        self.lab_tx_data = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "nonce": nonce,
            "timestamp": timestamp_str,
            "ciphertext": ciphertext_packet,
            "signature": signature_bytes.hex(),
            "hash": hash_val,
            "client_pub_key": self.lab_client_pub,
            "raw_signature": signature_bytes
        }
        
        self.lab_log("--- GIAO DỊCH AN TOÀN ĐÃ KHỞI TẠO THÀNH CÔNG ---", "success")
        self.lab_log(f"Plaintext: '{plaintext}'")
        self.lab_log(f"Khóa Phiên AES: {self.crypto.session_key.hex()[:24]}...")
        self.lab_log(f"Bản mã AES-GCM (Ciphertext): {ciphertext_bytes.hex()[:32]}...")
        self.lab_log(f"Chữ ký số RSA-PSS: {signature_bytes.hex()[:32]}...")
        self.lab_log(f"Mã Hash SHA-512: {hash_val[:32]}...")
        self.lab_log(f"Tham số phụ: Nonce={nonce[:12]}..., Time={timestamp_str}")

    def lab_send_to_bank(self):
        """Gửi giao dịch từ sandbox qua hệ thống phòng thủ của cổng ngân hàng để kiểm định"""
        if not self.lab_tx_data:
            messagebox.showerror("Lỗi", "Vui lòng bấm nút 'Bước 1: Khởi tạo Giao dịch' trước!", parent=self)
            return
            
        attack_type = self.lab_attack_var.get()
        
        # Bản sao dữ liệu để thao tác
        sender = self.lab_tx_data["sender"]
        receiver = self.lab_tx_data["receiver"]
        amount = self.lab_tx_data["amount"]
        nonce = self.lab_tx_data["nonce"]
        timestamp = self.lab_tx_data["timestamp"]
        ciphertext = self.lab_tx_data["ciphertext"]
        signature_hex = self.lab_tx_data["signature"]
        hash_val = self.lab_tx_data["hash"]
        client_pub_key = self.lab_tx_data["client_pub_key"]
        
        self.lab_log(f"🚀 Đang gửi giao dịch đến cổng thanh toán Ngân hàng (Cấu hình: {attack_type})...")
        
        # 1. ÁP DỤNG CÁC PHƯƠNG THỨC TẤN CÔNG GIẢ LẬP
        if attack_type != "REPLAY":
            self.crypto.nonce_registry.discard(nonce)

        if attack_type == "TAMPER":
            self.lab_log("😈 Hacker can thiệp đường truyền: Thay thế 1 byte trong Ciphertext!", "warning")
            parts = ciphertext.split(":")
            c_hex = parts[0]
            c_list = list(c_hex)
            c_list[0] = 'f' if c_list[0] != 'f' else '0'
            modified_c = "".join(c_list)
            ciphertext = f"{modified_c}:{parts[1]}:{parts[2]}"
            
        elif attack_type == "REPLAY":
            self.lab_log("😈 Hacker cố gắng gửi lại gói tin cũ (Replay Attack)!", "warning")
            self.crypto.nonce_registry.add(nonce)
            
        elif attack_type == "EXPIRE":
            self.lab_log("😈 Gói tin bị trễ hoặc Hacker phát lại sau 10 phút!", "warning")
            old_time = datetime.now() - timedelta(minutes=10)
            timestamp = old_time.strftime("%Y-%m-%d %H:%M:%S")
            signature_bytes = self.crypto.sign_metadata(sender, timestamp, nonce, self.lab_client_priv)
            signature_hex = signature_bytes.hex()
            hash_val = self.crypto.calculate_sha512_hash(ciphertext, timestamp)
            
        elif attack_type == "WRONG_KEY":
            self.lab_log("😈 Hacker cố gắng ký giả mạo bằng cặp khóa RSA tự tạo!", "warning")
            wrong_priv, wrong_pub = self.crypto.generate_client_rsa_key()
            signature_bytes = self.crypto.sign_metadata(sender, timestamp, nonce, wrong_priv)
            signature_hex = signature_bytes.hex()
            client_pub_key = wrong_pub
            
        # 2. HỆ THỐNG PHÒNG THỦ CỦA NGÂN HÀNG BẮT ĐẦU HOẠT ĐỘNG
        time.sleep(0.5)
        self.lab_log("🏦 --- HỆ THỐNG PHÒNG THỦ NGÂN HÀNG: ĐANG PHÂN TÍCH GÓI TIN ---")
        
        # BƯỚC A: Kiểm tra chữ ký số RSA-PSS
        self.lab_log("Bước 1: Xác minh danh tính người gửi (Xác thực chữ ký số RSA-PSS)...")
        sig_bytes = bytes.fromhex(signature_hex)
        sig_ok = self.crypto.verify_metadata_signature(sender, timestamp, nonce, sig_bytes, client_pub_key)
        
        if not sig_ok:
            self.lab_log("🚨 BÁO ĐỘNG ĐỎ: Chữ ký số RSA-PSS KHÔNG hợp lệ! Giao dịch bị giả mạo danh tính.", "error")
            self.lab_log("🚫 CỔNG THANH TOÁN: TỪ CHỐI GIAO DỊCH & GHI NHẬN LỖI PHÂN QUYỀN (Access Denied).", "error")
            return
        self.lab_log("✔ Bước 1 OK: Chữ ký số RSA-PSS hợp lệ. Danh tính khách hàng đã được xác minh.", "success")
        
        # BƯỚC B: Kiểm tra chống phát lại
        self.lab_log("Bước 2: Phân tích chống phát lại (Anti-replay Audit)...")
        try:
            self.crypto.check_anti_replay(nonce, timestamp)
            self.lab_log("✔ Bước 2 OK: Nonce chưa từng sử dụng và Timestamp nằm trong giới hạn cho phép.", "success")
        except Exception as e:
            self.lab_log(f"🚨 BÁO ĐỘNG ĐỎ: Phát hiện cuộc tấn công phát lại hoặc trễ hạn! Lý do: {str(e)}", "error")
            self.lab_log("🚫 CỔNG THANH TOÁN: TỪ CHỐI GIAO DỊCH & THIẾT LẬP CẢNH BÁO REPLAY (Security Alert).", "error")
            return
            
        # BƯỚC C: Kiểm tra tính toàn vẹn gói tin
        self.lab_log("Bước 3: Kiểm tra tính toàn vẹn gói tin truyền tải (SHA-512 Hash Verification)...")
        calculated_hash = self.crypto.calculate_sha512_hash(ciphertext, timestamp)
        if calculated_hash != hash_val:
            self.lab_log("🚨 BÁO ĐỘNG ĐỎ: Hash SHA-512 không trùng khớp! Bản mã bị can thiệp trên kênh truyền.", "error")
            self.lab_log("🚫 CỔNG THANH TOÁN: TỪ CHỐI GIAO DỊCH & GHI LOG LỖI TOÀN VẸN (Integrity Error).", "error")
            return
        self.lab_log("✔ Bước 3 OK: Hash SHA-512 trùng khớp. Tính toàn vẹn gói tin được bảo đảm.", "success")
        
        # BƯỚC D: Giải mã và Kiểm tra MAC
        self.lab_log("Bước 4: Giải mã dữ liệu và kiểm tra thẻ xác thực mật mã (AES-GCM Decryption)...")
        try:
            parts = ciphertext.split(":")
            c_bytes = bytes.fromhex(parts[0])
            t_bytes = bytes.fromhex(parts[1])
            n_bytes = bytes.fromhex(parts[2])
            
            decrypted_plaintext = self.crypto.decrypt_transaction_details(c_bytes, t_bytes, n_bytes, self.crypto.session_key)
            
            self.lab_log("✔ Bước 4 OK: Giải mã AES-GCM thành công. Thẻ xác thực (Authentication Tag) hợp lệ.", "success")
            self.lab_log(f"🎉 GIAO DỊCH ĐƯỢC CHẤP NHẬN AN TOÀN! Nội dung giao dịch: '{decrypted_plaintext}'", "success")
        except Exception as e:
            self.lab_log(f"🚨 BÁO ĐỘNG ĐỎ: Thẻ xác thực mật mã AES-GCM bị lỗi! Dữ liệu bị thay đổi trong quá trình truyền.", "error")
            self.lab_log(f"Chi tiết kỹ thuật: {str(e)}", "error")
            self.lab_log("🚫 CỔNG THANH TOÁN: TỪ CHỐI GIAO DỊCH & GHI LOG LỖI GIẢI MÃ MẬT MÃ (Decryption Error).", "error")
