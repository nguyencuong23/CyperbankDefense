# -*- coding: utf-8 -*-
"""
HỆ THỐNG MÃ HÓA NGÂN HÀNG - CYBERBANK DEFENSE GAME
Mixin quản lý Tab 1: Điều hành bảo mật (GameTabMixin)
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import uuid
from datetime import datetime, timedelta

from config import (
    BG_MAIN, BG_PANEL, BG_CARD, ACCENT, SUCCESS, WARNING, DANGER,
    TEXT_LIGHT, TEXT_DARK, TERMINAL_BG
)

class GameTabMixin:
    """Mixin cung cấp giao diện và lô-gích chơi game cho BankingApp"""
    
    def setup_tab_game(self):
        # Chia bố cục trái (Giao dịch cần duyệt) - phải (Nhật ký sự kiện + Hướng dẫn)
        self.tab_game.columnconfigure(0, weight=5)
        self.tab_game.columnconfigure(1, weight=4)
        self.tab_game.rowconfigure(0, weight=1)
        
        # --- CỘT TRÁI: GIAO DỊCH CHỜ DUYỆT ---
        frame_left = tk.Frame(self.tab_game, bg=BG_MAIN)
        frame_left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Tiêu đề khu vực
        lbl_sec_title = tk.Label(frame_left, text="HỒ SƠ GIAO DỊCH ĐANG ĐẾN (TRANSACTION QUEUE)", font=("Helvetica", 12, "bold"), fg=TEXT_LIGHT, bg=BG_MAIN)
        lbl_sec_title.pack(anchor="w", pady=5)
        
        # Card chứa thông tin giao dịch đang xử lý
        self.canvas_card = tk.Canvas(frame_left, bg=BG_PANEL, highlightthickness=1, highlightbackground=ACCENT, height=360)
        self.canvas_card.pack(fill="x", pady=5)
        
        # Vẽ các nhãn thông tin giao dịch lên Card
        self.draw_transaction_card_skeleton()
        
        # Khung chứa các nút kiểm thử bảo mật (Duyệt theo quy trình)
        lbl_steps_title = tk.Label(frame_left, text="QUY TRÌNH KIỂM TRA AN NINH BẮT BUỘC:", font=("Helvetica", 10, "bold"), fg=WARNING, bg=BG_MAIN)
        lbl_steps_title.pack(anchor="w", pady=10)
        
        frame_actions = tk.Frame(frame_left, bg=BG_MAIN)
        frame_actions.pack(fill="x", pady=5)
        
        self.btn_step_rsa = tk.Button(frame_actions, text="1. Xác thực RSA-PSS [Phím 1]", font=("Helvetica", 9, "bold"), bg=BG_CARD, fg=TEXT_LIGHT, relief="flat", height=2, command=self.action_verify_rsa)
        self.btn_step_rsa.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.btn_step_sha = tk.Button(frame_actions, text="2. Kiểm tra SHA-512 [Phím 2]", font=("Helvetica", 9, "bold"), bg=BG_CARD, fg=TEXT_LIGHT, relief="flat", height=2, command=self.action_verify_sha)
        self.btn_step_sha.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.btn_step_aes = tk.Button(frame_actions, text="3. Giải mã AES-GCM [Phím 3]", font=("Helvetica", 9, "bold"), bg=BG_CARD, fg=TEXT_LIGHT, relief="flat", height=2, command=self.action_verify_aes)
        self.btn_step_aes.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        self.btn_step_replay = tk.Button(frame_actions, text="4. Kiểm tra Anti-Replay [Phím 4]", font=("Helvetica", 9, "bold"), bg=BG_CARD, fg=TEXT_LIGHT, relief="flat", height=2, command=self.action_verify_replay)
        self.btn_step_replay.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        frame_actions.columnconfigure(0, weight=1)
        frame_actions.columnconfigure(1, weight=1)
        frame_actions.columnconfigure(2, weight=1)
        frame_actions.columnconfigure(3, weight=1)
        
        # Nút quyết định cuối cùng
        frame_decisions = tk.Frame(frame_left, bg=BG_MAIN)
        frame_decisions.pack(fill="x", pady=15)
        
        self.btn_approve = tk.Button(frame_decisions, text="✔ DUYỆT GIAO DỊCH [Phím J]", font=("Helvetica", 11, "bold"), bg=SUCCESS, fg="white", activebackground=SUCCESS, relief="flat", height=2, command=self.action_approve)
        self.btn_approve.pack(side="left", fill="x", expand=True, padx=10)
        
        self.btn_reject = tk.Button(frame_decisions, text="🗙 CHẶN & BÁO ĐỘNG TẤN CÔNG [Phím K]", font=("Helvetica", 11, "bold"), bg=DANGER, fg="white", activebackground=DANGER, relief="flat", height=2, command=self.action_reject)
        self.btn_reject.pack(side="right", fill="x", expand=True, padx=10)

        # --- CỘT PHẢI: LOG MONITOR & BÀI HỌC ---
        frame_right = tk.Frame(self.tab_game, bg=BG_MAIN)
        frame_right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Nhật ký bảo mật thời gian thực
        lbl_log_title = tk.Label(frame_right, text="NHẬT KÝ BẢO MẬT & THREAT AUDIT LOGS", font=("Helvetica", 12, "bold"), fg=DANGER, bg=BG_MAIN)
        lbl_log_title.pack(anchor="w", pady=5)
        
        self.txt_logs = scrolledtext.ScrolledText(frame_right, bg=TERMINAL_BG, fg=TEXT_LIGHT, font=("Courier New", 9), height=23)
        self.txt_logs.pack(fill="both", expand=True, pady=5)
        
        # Chú thích học thuật
        frame_tips = tk.Frame(frame_right, bg=BG_PANEL, bd=1, relief="solid")
        frame_tips.pack(fill="x", pady=10)
        
        self.lbl_tips_title = tk.Label(frame_tips, text="💡 HƯỚNG DẪN DÀNH CHO ADMIN:", font=("Helvetica", 10, "bold"), fg=WARNING, bg=BG_PANEL, padx=10, pady=5)
        self.lbl_tips_title.pack(anchor="w")
        
        self.lbl_tips_desc = tk.Label(frame_tips, text="Cấp độ 1: Làm quen với quy trình. Kiểm tra tuần tự cả 4 bước để hiểu cách dữ liệu được mã hóa AES-GCM, ký số RSA-PSS và chống Replay trước khi ấn nút duyệt.", font=("Helvetica", 9), fg=TEXT_LIGHT, bg=BG_PANEL, justify="left", wraplength=480, padx=10, pady=5)
        self.lbl_tips_desc.pack(anchor="w")

    def draw_transaction_card_skeleton(self):
        """Vẽ cấu trúc hiển thị dữ liệu của một giao dịch"""
        self.canvas_card.delete("all")
        
        # Nền card
        self.canvas_card.create_rectangle(1, 1, 550, 359, fill=BG_PANEL, outline=ACCENT, width=2)
        
        # Glow bar ở trên đầu
        self.canvas_card.create_rectangle(2, 2, 548, 10, fill=ACCENT, outline="")
        
        # Nhãn
        self.canvas_card.create_text(20, 35, text="Tài khoản Người gửi:", font=("Helvetica", 10, "bold"), fill=TEXT_DARK, anchor="w")
        self.canvas_card.create_text(20, 65, text="Tài khoản Người nhận:", font=("Helvetica", 10, "bold"), fill=TEXT_DARK, anchor="w")
        self.canvas_card.create_text(20, 95, text="Số tiền Giao dịch:", font=("Helvetica", 10, "bold"), fill=TEXT_DARK, anchor="w")
        self.canvas_card.create_text(20, 125, text="Mã Nonce (Anti-Replay):", font=("Helvetica", 10, "bold"), fill=TEXT_DARK, anchor="w")
        self.canvas_card.create_text(20, 155, text="Thời gian (Timestamp):", font=("Helvetica", 10, "bold"), fill=TEXT_DARK, anchor="w")
        
        self.canvas_card.create_text(20, 200, text="Ciphertext (AES-GCM):", font=("Helvetica", 10, "bold"), fill=TEXT_DARK, anchor="w")
        self.canvas_card.create_text(20, 260, text="RSA-PSS Signature:", font=("Helvetica", 10, "bold"), fill=TEXT_DARK, anchor="w")
        self.canvas_card.create_text(20, 320, text="SHA-512 Integrity Hash:", font=("Helvetica", 10, "bold"), fill=TEXT_DARK, anchor="w")

        # Khởi tạo các biến text để update sau
        self.text_sender = self.canvas_card.create_text(180, 35, text="--", font=("Helvetica", 10), fill=TEXT_LIGHT, anchor="w")
        self.text_receiver = self.canvas_card.create_text(180, 65, text="--", font=("Helvetica", 10), fill=TEXT_LIGHT, anchor="w")
        self.text_amount = self.canvas_card.create_text(180, 95, text="--", font=("Helvetica", 10, "bold"), fill=SUCCESS, anchor="w")
        self.text_nonce = self.canvas_card.create_text(180, 125, text="--", font=("Courier New", 9), fill=TEXT_LIGHT, anchor="w")
        self.text_timestamp = self.canvas_card.create_text(180, 155, text="--", font=("Courier New", 9), fill=TEXT_LIGHT, anchor="w")
        
        self.text_ciphertext = self.canvas_card.create_text(20, 225, text="--", font=("Courier New", 8), fill=WARNING, anchor="w", width=510)
        self.text_signature = self.canvas_card.create_text(20, 285, text="--", font=("Courier New", 8), fill=ACCENT, anchor="w", width=510)
        self.text_hash = self.canvas_card.create_text(20, 340, text="--", font=("Courier New", 8), fill=SUCCESS, anchor="w", width=510)

    def log_event(self, message, type="info"):
        """Ghi sự kiện vào nhật ký với mã màu trực quan"""
        now = datetime.now().strftime("%H:%M:%S")
        prefix = f"[{now}] "
        
        self.txt_logs.config(state="normal")
        
        # Chọn màu sắc cho tag
        if type == "info":
            color_tag = "info_tag"
            color_fg = "#38BDF8"  # Light blue
        elif type == "success":
            color_tag = "success_tag"
            color_fg = "#34D399"  # Light green
        elif type == "warning":
            color_tag = "warning_tag"
            color_fg = "#FBBF24"  # Amber
        elif type == "danger":
            color_tag = "danger_tag"
            color_fg = "#F87171"  # Red
            
        self.txt_logs.insert(tk.END, prefix + message + "\n", color_tag)
        self.txt_logs.tag_config(color_tag, foreground=color_fg)
        self.txt_logs.see(tk.END)
        self.txt_logs.config(state="disabled")

    def generate_new_transaction(self):
        """Hệ thống tự động sinh các giao dịch (hợp lệ hoặc tấn công) dựa theo level hiện tại"""
        # Đặt lại trạng thái quy trình kiểm tra của người chơi
        self.step_rsa_verified = False
        self.step_sha_verified = False
        self.step_aes_verified = False
        self.step_replay_verified = False
        
        # Reset màu nút
        self.btn_step_rsa.config(bg=BG_CARD)
        self.btn_step_sha.config(bg=BG_CARD)
        self.btn_step_aes.config(bg=BG_CARD)
        self.btn_step_replay.config(bg=BG_CARD)
        
        # Dữ liệu giao dịch gốc
        sender_list = ["Alice (ACC-100204)", "David (ACC-220912)", "James (ACC-998811)", "Sophia (ACC-776612)"]
        receiver_list = ["Bob (ACC-887711)", "Eva (ACC-334455)", "Mary (ACC-554433)", "Wilson (ACC-112233)"]
        
        sender = random.choice(sender_list)
        receiver = random.choice(receiver_list)
        amount = f"${random.randint(5, 500) * 10}"
        
        nonce = uuid.uuid4().hex
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        plaintext = f"{sender}->{receiver}:{amount}"
        
        # 1. Mã hóa AES-GCM giao dịch
        session_key = self.crypto.session_key
        ciphertext_bytes, tag_bytes, gcm_nonce = self.crypto.encrypt_transaction_details(plaintext, session_key)
        
        ciphertext_hex = ciphertext_bytes.hex()
        tag_hex = tag_bytes.hex()
        gcm_nonce_hex = gcm_nonce.hex()
        
        # Gói tin đầy đủ
        ciphertext_packet = f"{ciphertext_hex}:{tag_hex}:{gcm_nonce_hex}"
        
        # 2. Chữ ký số RSA-PSS của khách hàng trên metadata
        signature_bytes = self.crypto.sign_metadata(sender, timestamp_str, nonce, self.client_priv_key)
        signature_hex = signature_bytes.hex()
        
        # 3. Hash tính toán toàn vẹn
        hash_val = self.crypto.calculate_sha512_hash(ciphertext_packet, timestamp_str)
        
        # Quyết định loại giao dịch dựa trên level
        tx_type = "VALID"
        attack_description = "Giao dịch Hợp lệ"
        
        if self.level == 1:
            tx_type = "VALID"
        elif self.level == 2:
            tx_type = random.choices(["VALID", "TAMPERED", "REPLAY"], weights=[60, 20, 20])[0]
        else:
            tx_type = random.choices(["VALID", "TAMPERED", "REPLAY", "EXPIRED", "WRONG_KEY"], weights=[40, 20, 20, 10, 10])[0]
            
        # Biến đổi gói tin nếu là cuộc tấn công
        modified_ciphertext_packet = ciphertext_packet
        modified_signature_hex = signature_hex
        modified_timestamp = timestamp_str
        modified_nonce = nonce
        modified_pub_key = self.client_pub_key
        
        if tx_type == "TAMPERED":
            attack_description = "Tấn công Sửa đổi dữ liệu (Tampering)"
            char_list = list(ciphertext_hex)
            idx = random.randint(0, len(char_list) - 1)
            char_list[idx] = 'f' if char_list[idx] != 'f' else '0'
            tampered_cipher = "".join(char_list)
            modified_ciphertext_packet = f"{tampered_cipher}:{tag_hex}:{gcm_nonce_hex}"
            
        elif tx_type == "REPLAY":
            attack_description = "Tấn công Phát lại (Replay Attack)"
            if self.crypto.nonce_registry:
                modified_nonce = list(self.crypto.nonce_registry)[0]
            else:
                modified_nonce = "fixed_nonce_already_used_991823"
                self.crypto.nonce_registry.add(modified_nonce)
                
        elif tx_type == "EXPIRED":
            attack_description = "Giao dịch Quá hạn (Timeout)"
            old_time = datetime.now() - timedelta(minutes=5)
            modified_timestamp = old_time.strftime("%Y-%m-%d %H:%M:%S")
            signature_bytes = self.crypto.sign_metadata(sender, modified_timestamp, nonce, self.client_priv_key)
            modified_signature_hex = signature_bytes.hex()
            hash_val = self.crypto.calculate_sha512_hash(modified_ciphertext_packet, modified_timestamp)
            
        elif tx_type == "WRONG_KEY":
            attack_description = "Tấn công Chữ ký giả mạo (Invalid Signature)"
            _, wrong_pub_key = self.crypto.generate_client_rsa_key()
            modified_pub_key = wrong_pub_key
            
        self.current_transaction = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "nonce": modified_nonce,
            "timestamp": modified_timestamp,
            "ciphertext": modified_ciphertext_packet,
            "signature": modified_signature_hex,
            "hash": hash_val,
            "true_type": tx_type,
            "description": attack_description,
            "client_pub_key": modified_pub_key,
            "raw_signature": bytes.fromhex(modified_signature_hex)
        }
        
        # Cập nhật thông tin giao dịch lên Card GUI
        self.canvas_card.itemconfig(self.text_sender, text=sender)
        self.canvas_card.itemconfig(self.text_receiver, text=receiver)
        self.canvas_card.itemconfig(self.text_amount, text=amount)
        self.canvas_card.itemconfig(self.text_nonce, text=modified_nonce)
        self.canvas_card.itemconfig(self.text_timestamp, text=modified_timestamp)
        
        # Cắt ngắn text hiển thị trên GUI cho đẹp mắt
        self.canvas_card.itemconfig(self.text_ciphertext, text=modified_ciphertext_packet[:75] + "...")
        self.canvas_card.itemconfig(self.text_signature, text=modified_signature_hex[:75] + "...")
        self.canvas_card.itemconfig(self.text_hash, text=hash_val[:75] + "...")
        
        self.log_event(f"Yêu cầu giao dịch mới được đẩy vào Queue xử lý ({attack_description}).", "info")

    def action_verify_rsa(self):
        tx = self.current_transaction
        if not tx: return
        
        valid = self.crypto.verify_metadata_signature(
            tx["sender"], tx["timestamp"], tx["nonce"], tx["raw_signature"], tx["client_pub_key"]
        )
        
        if valid:
            self.btn_step_rsa.config(bg=SUCCESS)
            self.log_event("XÁC THỰC RSA CHỮ KÝ SỐ: Chữ ký hợp lệ! Đảm bảo danh tính người gửi và tính toàn vẹn của metadata.", "success")
        else:
            self.btn_step_rsa.config(bg=DANGER)
            self.log_event("CẢNH BÁO RSA CHỮ KÝ SỐ: Chữ ký số không khớp! Có thể do sửa đổi metadata hoặc mạo danh khách hàng.", "danger")
            
        self.step_rsa_verified = True

    def action_verify_sha(self):
        tx = self.current_transaction
        if not tx: return
        
        calculated_hash = self.crypto.calculate_sha512_hash(tx["ciphertext"], tx["timestamp"])
        hash_match = (calculated_hash == tx["hash"])
        
        try:
            tx_time = datetime.strptime(tx["timestamp"], "%Y-%m-%d %H:%M:%S")
            age = (datetime.now() - tx_time).total_seconds()
            time_valid = (age <= 15)
        except:
            time_valid = False
            
        if hash_match and time_valid:
            self.btn_step_sha.config(bg=SUCCESS)
            self.log_event(f"KIỂM TRA HASH TOÀN VẸN: Hash trùng khớp! Giao dịch trong thời hạn hiệu lực ({age:.1f}s).", "success")
        elif not hash_match:
            self.btn_step_sha.config(bg=DANGER)
            self.log_event("CẢNH BÁO HASH TOÀN VẸN: Lỗi trùng khớp! Bản mã giao dịch (Ciphertext) đã bị thay đổi trên đường truyền.", "danger")
        else:
            self.btn_step_sha.config(bg=DANGER)
            self.log_event(f"CẢNH BÁO THỜI GIAN: Giao dịch đã quá hạn! Được gửi từ {age:.1f} giây trước (Giới hạn: 15 giây). Có dấu hiệu Replay.", "danger")
            
        self.step_sha_verified = True

    def action_verify_aes(self):
        tx = self.current_transaction
        if not tx: return
        
        try:
            parts = tx["ciphertext"].split(":")
            if len(parts) != 3:
                raise ValueError("Bản mã không đúng định dạng GCM")
            
            c_bytes = bytes.fromhex(parts[0])
            t_bytes = bytes.fromhex(parts[1])
            n_bytes = bytes.fromhex(parts[2])
            
            plaintext = self.crypto.decrypt_transaction_details(c_bytes, t_bytes, n_bytes, self.crypto.session_key)
            
            self.btn_step_aes.config(bg=SUCCESS)
            self.log_event(f"GIẢI MÃ AES-GCM THÀNH CÔNG! Nội dung giải mã: '{plaintext}'. Khớp khóa xác thực AEAD.", "success")
        except Exception as e:
            self.btn_step_aes.config(bg=DANGER)
            self.log_event(f"CẢNH BÁO AES-GCM: Giải mã thất bại! {str(e)}", "danger")
            
        self.step_aes_verified = True

    def action_verify_replay(self):
        tx = self.current_transaction
        if not tx: return
        
        if tx["nonce"] in self.crypto.nonce_registry:
            self.btn_step_replay.config(bg=DANGER)
            self.log_event(f"PHÁT HIỆN TẤN CÔNG GỬI LẠI (ANTI-REPLAY): Mã Nonce '{tx['nonce'][:12]}' đã tồn tại trong Database giao dịch thành công!", "danger")
        else:
            self.btn_step_replay.config(bg=SUCCESS)
            self.log_event(f"KIỂM TRA ANTI-REPLAY: Nonce '{tx['nonce'][:12]}...' hợp lệ (chưa từng sử dụng trước đây). Giao dịch được bảo vệ.", "success")
            
        self.step_replay_verified = True

    def bind_game_hotkeys(self):
        """Đăng ký phím tắt kiểm duyệt giao dịch"""
        def check_and_run(func):
            focus_w = self.focus_get()
            if focus_w and isinstance(focus_w, (tk.Entry, tk.Text)):
                return
            if hasattr(self, "decision_overlay") and self.decision_overlay is not None:
                return
            func()
            
        self.bind("1", lambda event: check_and_run(self.action_verify_rsa))
        self.bind("2", lambda event: check_and_run(self.action_verify_sha))
        self.bind("3", lambda event: check_and_run(self.action_verify_aes))
        self.bind("4", lambda event: check_and_run(self.action_verify_replay))
        self.bind("j", lambda event: check_and_run(self.action_approve))
        self.bind("k", lambda event: check_and_run(self.action_reject))
        self.bind("J", lambda event: check_and_run(self.action_approve))
        self.bind("K", lambda event: check_and_run(self.action_reject))

    def show_decision_overlay(self, title, message, is_success):
        """Hiển thị cửa sổ thông báo kết quả phán quyết kiểu Cyberpunk non-blocking (Hỗ trợ phím bất kỳ)"""
        self.unbind("1")
        self.unbind("2")
        self.unbind("3")
        self.unbind("4")
        self.unbind("j")
        self.unbind("k")
        self.unbind("J")
        self.unbind("K")
        
        # 1. Tạo Lớp phủ mờ nền sau
        self.decision_blur = tk.Frame(self, bg="#020617")
        self.decision_blur.place(x=0, y=0, relwidth=1, relheight=1)
        
        # 2. Hộp thông báo nổi lên ở giữa
        color_theme = SUCCESS if is_success else DANGER
        self.decision_overlay = tk.Frame(self.decision_blur, bg=BG_PANEL, highlightthickness=2, highlightbackground=color_theme, padx=30, pady=30)
        self.decision_overlay.place(relx=0.5, rely=0.5, anchor="center", width=550, height=300)
        
        icon = "🛡️ PHÒNG THỦ THÀNH CÔNG" if is_success else "🚨 BÁO ĐỘNG ĐỎ"
        lbl_status = tk.Label(self.decision_overlay, text=f"{icon}\n{title}", font=("Helvetica", 13, "bold"), fg=color_theme, bg=BG_PANEL, justify="center")
        lbl_status.pack(pady=(10, 15))
        
        lbl_msg = tk.Label(self.decision_overlay, text=message, font=("Helvetica", 10), fg=TEXT_LIGHT, bg=BG_PANEL, justify="center", wraplength=480)
        lbl_msg.pack(pady=(0, 20))
        
        lbl_hint = tk.Label(self.decision_overlay, text="[ BẤM PHÍM BẤT KỲ TRÊN BÀN PHÍM ĐỂ TIẾP TỤC ]", font=("Courier New", 9, "bold"), fg=WARNING, bg=BG_PANEL)
        lbl_hint.pack(pady=10)
        
        def blink():
            if hasattr(self, "decision_overlay") and self.decision_overlay:
                current_fg = lbl_hint.cget("fg")
                next_fg = BG_PANEL if current_fg == WARNING else WARNING
                lbl_hint.config(fg=next_fg)
                self.after(500, blink)
        blink()
        
        self.decision_overlay.focus_set()
        self.bind("<Key>", self.close_decision_overlay)

    def close_decision_overlay(self, event=None):
        """Đóng lớp phủ phán quyết và kiểm tra xem có sự kiện lên cấp chờ hiển thị không"""
        if hasattr(self, "decision_blur") and self.decision_blur:
            self.decision_blur.destroy()
            self.decision_blur = None
        self.decision_overlay = None
        self.unbind("<Key>")
        
        if hasattr(self, "level_up_pending") and self.level_up_pending is not None:
            pending = self.level_up_pending
            self.level_up_pending = None
            self.show_level_up_overlay(pending["title"], pending["message"])
        else:
            self.bind_game_hotkeys()
            self.generate_new_transaction()

    def show_level_up_overlay(self, title, message):
        """Hiển thị lớp phủ chúc mừng Thăng cấp kiểu Cyberpunk đặc biệt (Hỗ trợ phím bất kỳ)"""
        self.unbind("1")
        self.unbind("2")
        self.unbind("3")
        self.unbind("4")
        self.unbind("j")
        self.unbind("k")
        self.unbind("J")
        self.unbind("K")
        
        self.decision_blur = tk.Frame(self, bg="#020617")
        self.decision_blur.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.decision_overlay = tk.Frame(self.decision_blur, bg=BG_PANEL, highlightthickness=3, highlightbackground=WARNING, padx=30, pady=30)
        self.decision_overlay.place(relx=0.5, rely=0.5, anchor="center", width=580, height=350)
        
        lbl_status = tk.Label(self.decision_overlay, text="⚡ THĂNG CẤP QUẢN TRỊ VIÊN ⚡", font=("Helvetica", 15, "bold"), fg=WARNING, bg=BG_PANEL, justify="center")
        lbl_status.pack(pady=(10, 15))
        
        lbl_msg = tk.Label(self.decision_overlay, text=message, font=("Helvetica", 10), fg=TEXT_LIGHT, bg=BG_PANEL, justify="center", wraplength=520)
        lbl_msg.pack(pady=(0, 25))
        
        lbl_hint = tk.Label(self.decision_overlay, text="[ BẤM PHÍM BẤT KỲ TRÊN BÀN PHÍM ĐỂ KÍCH HOẠT HỆ THỐNG MỚI ]", font=("Courier New", 9, "bold"), fg=SUCCESS, bg=BG_PANEL)
        lbl_hint.pack(pady=10)
        
        def blink():
            if hasattr(self, "decision_overlay") and self.decision_overlay:
                current_fg = lbl_hint.cget("fg")
                next_fg = BG_PANEL if current_fg == SUCCESS else SUCCESS
                lbl_hint.config(fg=next_fg)
                self.after(500, blink)
        blink()
        
        self.decision_overlay.focus_set()
        self.bind("<Key>", self.close_level_up_overlay)

    def close_level_up_overlay(self, event=None):
        """Đóng màn hình thăng cấp và khôi phục phím tắt"""
        if hasattr(self, "decision_blur") and self.decision_blur:
            self.decision_blur.destroy()
            self.decision_blur = None
        self.decision_overlay = None
        self.unbind("<Key>")
        
        self.bind_game_hotkeys()
        self.generate_new_transaction()

    def action_approve(self):
        tx = self.current_transaction
        if not tx: return
        
        if self.level == 1 and not (self.step_rsa_verified and self.step_sha_verified and self.step_aes_verified and self.step_replay_verified):
            messagebox.showwarning("Quy trình bảo mật bắt buộc", "Ở Cấp độ 1, bạn cần bấm thực hiện đủ cả 4 bước Kiểm Tra Bảo Mật để làm quen với hệ thống trước khi Duyệt!", parent=self)
            return
            
        is_attack = (tx["true_type"] != "VALID")
        
        if not is_attack:
            self.score += 100
            self.crypto.nonce_registry.add(tx["nonce"])
            self.log_event(f"✔ GIAO DỊCH ĐÃ ĐƯỢC CHẤP THUẬN. Tài khoản người nhận nhận được {tx['amount']}. Cộng 100 điểm.", "success")
            
            self.update_game_state()
            self.show_decision_overlay(
                "DUYỆT GIAO DỊCH THÀNH CÔNG",
                f"Đã phê duyệt giao dịch hợp lệ của {tx['sender']} gửi {tx['amount']} thành công!\n\n💰 Cộng: +100 điểm.",
                True
            )
        else:
            self.score = max(0, self.score - 150)
            self.integrity_alarms += 1
            self.log_event(f"❌ THỦNG LƯỚI BẢO MẬT! Bạn đã duyệt một giao dịch TẤN CÔNG ({tx['description']}). Ngân hàng bị tổn thất tài chính! Trừ 150 điểm.", "danger")
            
            self.update_game_state()
            self.show_decision_overlay(
                "SỰ CỐ BẢO MẬT NGHIÊM TRỌNG (LỌT LƯỚI TẤN CÔNG)",
                f"CẢNH BÁO! Bạn đã cho phép lọt lưới cuộc tấn công: {tx['description']}.\nTin tặc đã chiếm đoạt {tx['amount']} thành công!\n\n🔴 Trừ: -150 điểm.",
                False
            )

    def action_reject(self):
        tx = self.current_transaction
        if not tx: return
        
        is_attack = (tx["true_type"] != "VALID")
        
        if is_attack:
            self.score += 100
            self.attacks_blocked += 1
            self.log_event(f"🛡️ PHÒNG THỦ THÀNH CÔNG! Bạn đã phát hiện và chặn đứng: {tx['description']}. Cộng 100 điểm.", "success")
            
            self.update_game_state()
            self.show_decision_overlay(
                "PHÒNG THỦ THÀNH CÔNG",
                f"🛡️ Ngăn chặn và cô lập thành công cuộc tấn công: {tx['description']}!\n\n💰 Cộng: +100 điểm.",
                True
            )
        else:
            self.score = max(0, self.score - 50)
            self.log_event(f"⚠ PHẢN HỒI SAI LẦM: Bạn đã từ chối một giao dịch HOÀN TOÀN HỢP LỆ của {tx['sender']}. Khách hàng khiếu nại! Trừ 50 điểm.", "warning")
            
            self.update_game_state()
            self.show_decision_overlay(
                "SAI LẦM NGHIỆP VỤ BẢO MẬT",
                f"Khách hàng khiếu nại gay gắt vì giao dịch hợp lệ trị giá {tx['amount']} bị từ chối oan!\n\n⚠️ Trừ: -50 điểm.",
                False
            )

    def update_game_state(self):
        """Cập nhật giao diện điểm số, level và hướng dẫn"""
        leveled_up = False
        tips_text = ""
        
        if self.score >= 500 and self.level == 1:
            self.level = 2
            self.log_event("CHÚC MỪNG! Bạn đã thăng cấp lên LEVEL 2. Các mối đe dọa thực tế đã bắt đầu xuất hiện!", "warning")
            tips_text = "Cấp độ 2: Tấn công xuất hiện! Tin tặc sẽ cố gắng gửi lại các giao dịch cũ (Replay) hoặc sửa đổi dữ liệu (Tampering). Hãy cẩn thận kiểm tra các trường Nonce, Hash và Decryption GCM để nhận diện."
            self.lbl_tips_desc.config(text=tips_text)
            leveled_up = True
            
        elif self.score >= 1200 and self.level == 2:
            self.level = 3
            self.log_event("CẢNH BÁO KHẨN CẤP! Bạn đã thăng cấp lên LEVEL 3. Bạn phải đối đầu với toàn bộ các loại tấn công dồn dập!", "danger")
            tips_text = "Cấp độ 3 (Cyber Warfare): Tấn công dồn dập với tần suất cao. Bạn sẽ gặp cả giao dịch quá hạn (Expired Timestamp), chữ ký mạo danh (Wrong RSA Key). Kiểm tra nhanh chóng và quyết đoán!"
            self.lbl_tips_desc.config(text=tips_text)
            leveled_up = True
            
        if leveled_up:
            self.level_up_pending = {
                "title": f"🎉 CHÚC MỪNG: BẠN ĐÃ THĂNG CẤP LÊN LEVEL {self.level}!",
                "message": f"Tuyệt vời! Bạn đã tích lũy đủ điểm kinh nghiệm an ninh hệ thống.\n\n🤖 CHI TIẾT CẤP ĐỘ MỚI:\n{tips_text}"
            }
            
        self.lbl_level.config(text=f"LEVEL: {self.level}", fg=WARNING if self.level == 2 else (DANGER if self.level == 3 else SUCCESS))
        self.lbl_score.config(text=f"ĐIỂM: {self.score}")
        self.lbl_blocked.config(text=f"NGĂN CHẶN: {self.attacks_blocked}")
