# -*- coding: utf-8 -*-
"""
HỆ THỐNG MÃ HÓA NGÂN HÀNG - CYBERBANK DEFENSE GAME
Đề tài 23: Bài Tập Lớn - Nhập Môn An Toàn Bảo Mật Thông Tin
Ngôn ngữ: Python 3
Mô tả: Trò chơi giáo dục & mô phỏng bảo mật dành cho quản trị viên an ninh ngân hàng.
Lớp ứng dụng chính và điều phối các mô-đun.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import hashlib
import os

# Import các mô-đun cấu hình và mật mã học
from config import (
    BG_MAIN, BG_PANEL, BG_CARD, ACCENT, SUCCESS, WARNING, DANGER,
    TEXT_LIGHT, TEXT_DARK
)
from crypto import CryptoEngine

# Import các Mixin quản lý giao diện Tab
from gui.game_tab import GameTabMixin
from gui.lab_tab import LabTabMixin
from gui.benchmark_tab import BenchmarkTabMixin
from gui.theory_tab import TheoryTabMixin

class BankingApp(tk.Tk, GameTabMixin, LabTabMixin, BenchmarkTabMixin, TheoryTabMixin):
    """Giao diện chính và Luồng xử lý game CyberBank Defense"""
    def __init__(self):
        super().__init__()
        self.title("CYBERBANK DEFENSE v2.0 - HỆ THỐNG MÃ HÓA NGÂN HÀNG")
        self.configure(bg=BG_MAIN)
        self.state('zoomed') # Kích hoạt toàn màn hình ngay khi khởi động
        
        # Đường dẫn tệp lưu thông tin đăng nhập
        import sys
        if getattr(sys, 'frozen', False):
            self.credentials_path = os.path.join(os.path.dirname(sys.executable), "credentials.json")
        else:
            self.credentials_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "credentials.json")
        
        # Khởi tạo lõi mật mã học
        self.crypto = CryptoEngine()
        
        # Điểm số và trạng thái game
        self.player_name = "Cường Hacker"
        self.score = 0
        self.level = 1
        self.attacks_blocked = 0
        self.integrity_alarms = 0
        
        # Khởi tạo dữ liệu khách hàng
        self.client_priv_key, self.client_pub_key = self.crypto.generate_client_rsa_key()
        self.current_transaction = None
        self.transaction_history = []
        
        # Trạng thái các bước kiểm tra của người chơi
        self.step_rsa_verified = False
        self.step_sha_verified = False
        self.step_aes_verified = False
        self.step_replay_verified = False
        
        # Khởi tạo tệp đăng nhập và đồng bộ
        self.init_credentials_file()
        
        # Hiển thị màn hình đăng nhập dạng full-screen frame
        self.show_login_screen()

    def init_credentials_file(self):
        """Khởi tạo tệp credentials.json lưu tài khoản bảo mật nếu chưa tồn tại hoặc di trú và đồng bộ hóa mật khẩu"""
        default_user = "Group 23 - ATBM"
        default_pass = "atbm_key_2026"
        default_hash = hashlib.sha256(default_pass.encode('utf-8')).hexdigest()
        
        if not os.path.exists(self.credentials_path):
            import sys
            bundled_creds_path = ""
            if hasattr(sys, '_MEIPASS'):
                bundled_creds_path = os.path.join(sys._MEIPASS, "credentials.json")
                
            if bundled_creds_path and os.path.exists(bundled_creds_path):
                try:
                    import shutil
                    shutil.copy(bundled_creds_path, self.credentials_path)
                except Exception:
                    pass
            else:
                default_creds = {
                    "username": default_user,
                    "password": default_pass,
                    "password_sha256": default_hash
                }
                try:
                    with open(self.credentials_path, "w", encoding="utf-8") as f:
                        json.dump(default_creds, f, indent=4, ensure_ascii=False)
                except Exception:
                    pass
        else:
            try:
                with open(self.credentials_path, "r", encoding="utf-8") as f:
                    creds = json.load(f)
                
                updated = False
                
                if "password" not in creds:
                    if creds.get("password_sha256") == default_hash:
                        creds["password"] = default_pass
                    else:
                        creds["password"] = "atbm_key_2026"
                    updated = True
                
                current_pass = creds.get("password", default_pass)
                current_hash = creds.get("password_sha256", "")
                computed_hash = hashlib.sha256(current_pass.encode('utf-8')).hexdigest()
                
                if current_hash != computed_hash:
                    creds["password_sha256"] = computed_hash
                    updated = True
                
                if updated:
                    with open(self.credentials_path, "w", encoding="utf-8") as f:
                        json.dump(creds, f, indent=4, ensure_ascii=False)
            except Exception:
                pass

    def show_login_screen(self):
        """Hiển thị màn hình chào mừng / đăng nhập của Quản trị viên dạng Full-screen Frame"""
        self.frame_login = tk.Frame(self, bg=BG_MAIN)
        self.frame_login.pack(fill="both", expand=True)
        
        import sys
        if hasattr(sys, '_MEIPASS'):
            bg_image_path = os.path.join(sys._MEIPASS, "background.png")
        else:
            bg_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "background.png")
        self.login_bg_image = None
        
        lbl_bg = tk.Label(self.frame_login, bg=BG_MAIN)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)
        
        if os.path.exists(bg_image_path):
            try:
                self.login_bg_image = tk.PhotoImage(file=bg_image_path)
                lbl_bg.config(image=self.login_bg_image)
            except Exception as e:
                lbl_bg.config(text=f"[Lỗi tải background.png: Không đúng định dạng PNG]\n{str(e)}", fg=DANGER, font=("Helvetica", 10), compound="center")
        else:
            lbl_bg.config(text="[Thêm tệp 'background.png' vào thư mục dự án để làm hình nền đăng nhập]", fg=TEXT_DARK, font=("Helvetica", 10), compound="center")
        
        frame_center = tk.Frame(self.frame_login, bg=BG_PANEL, highlightthickness=1, highlightbackground=ACCENT, padx=40, pady=40)
        frame_center.place(relx=0.5, rely=0.5, anchor="center", width=550, height=450)
        
        lbl_title = tk.Label(frame_center, text="CYBERBANK DEFENSE SYSTEM v2.0", font=("Helvetica", 18, "bold"), fg=ACCENT, bg=BG_PANEL)
        lbl_title.pack(pady=(10, 5))
        
        lbl_sub = tk.Label(frame_center, text="HỆ THỐNG MÃ HÓA NGÂN HÀNG & MÔ PHỎNG BẢO MẬT", font=("Helvetica", 10, "bold"), fg=TEXT_LIGHT, bg=BG_PANEL)
        lbl_sub.pack(pady=(0, 20))
        
        lbl_desc = tk.Label(frame_center, text="Môn học: Nhập môn An toàn và Bảo mật thông tin\nĐề tài 23: Phát triển game mang tính giáo dục và mô phỏng bảo mật\n\nVui lòng đăng ký thông tin Quản trị viên An ninh của nhóm để kích hoạt khóa phiên bảo mật.", font=("Helvetica", 9), fg=TEXT_DARK, bg=BG_PANEL, justify="center", wraplength=450)
        lbl_desc.pack(pady=(0, 20))
        
        frame_inputs = tk.Frame(frame_center, bg=BG_PANEL)
        frame_inputs.pack(pady=10)
        frame_inputs.columnconfigure(1, weight=1)
        
        pref_user = "Cuong123"
        pref_pass = "atbm_key_2026"
        try:
            with open(self.credentials_path, "r", encoding="utf-8") as f:
                creds = json.load(f)
            pref_user = creds.get("username", pref_user)
            pref_pass = creds.get("password", pref_pass)
        except Exception:
            pass
        
        tk.Label(frame_inputs, text="Tên Người Chơi:", font=("Helvetica", 10, "bold"), fg=TEXT_DARK, bg=BG_PANEL).grid(row=0, column=0, sticky="w", pady=8)
        
        frame_user_container = tk.Frame(frame_inputs, bg=BG_CARD, highlightthickness=1, highlightbackground="black", bd=0)
        frame_user_container.grid(row=0, column=1, padx=15, pady=8, sticky="we")
        
        self.ent_name = tk.Entry(frame_user_container, font=("Helvetica", 10), bg=BG_CARD, fg=TEXT_LIGHT, insertbackground=TEXT_LIGHT, bd=0, highlightthickness=0)
        self.ent_name.insert(0, pref_user)
        self.ent_name.pack(side="left", fill="both", expand=True, padx=8, pady=5)
        
        tk.Label(frame_inputs, text="Mật khẩu bảo vệ (Local Key):", font=("Helvetica", 10, "bold"), fg=TEXT_DARK, bg=BG_PANEL).grid(row=1, column=0, sticky="w", pady=8)
        
        frame_pass_container = tk.Frame(frame_inputs, bg=BG_CARD, highlightthickness=1, highlightbackground="black", bd=0)
        frame_pass_container.grid(row=1, column=1, padx=15, pady=8, sticky="we")
        
        self.ent_pass = tk.Entry(frame_pass_container, font=("Helvetica", 10), bg=BG_CARD, fg=TEXT_LIGHT, show="*", insertbackground=TEXT_LIGHT, bd=0, highlightthickness=0)
        self.ent_pass.insert(0, pref_pass)
        self.ent_pass.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=5)
        
        def toggle_password_visibility():
            if self.ent_pass.cget("show") == "*":
                self.ent_pass.config(show="")
                btn_eye.config(text="🙈")
            else:
                self.ent_pass.config(show="*")
                btn_eye.config(text="👁")
                
        btn_eye = tk.Button(frame_pass_container, text="👁", font=("Helvetica", 9), bg=BG_CARD, fg=TEXT_LIGHT, activebackground=BG_CARD, activeforeground=TEXT_LIGHT, bd=0, relief="flat", padx=8, pady=0, cursor="hand2", command=toggle_password_visibility)
        btn_eye.pack(side="right", fill="y", padx=(0, 2))
        
        def on_login():
            name = self.ent_name.get().strip()
            password = self.ent_pass.get().strip()
            if not name or not password:
                messagebox.showerror("Lỗi nhập liệu", "Vui lòng điền đầy đủ Tên và Khóa bảo mật để dẫn xuất khóa!", parent=self)
                return
                
            try:
                with open(self.credentials_path, "r", encoding="utf-8") as f:
                    creds = json.load(f)
                
                stored_user = creds.get("username", "Group 23 - ATBM")
                stored_hash = creds.get("password_sha256", "")
                
                entered_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
                
                if name != stored_user or entered_hash != stored_hash:
                    messagebox.showerror("Đăng nhập thất bại", "Tên người chơi hoặc mật khẩu bảo vệ không chính xác!", parent=self)
                    return
            except Exception:
                if name != "Group 23 - ATBM" or password != "atbm_key_2026":
                    messagebox.showerror("Đăng nhập thất bại", "Thông tin đăng nhập không chính xác hoặc tệp credentials.json bị lỗi!", parent=self)
                    return
            
            self.player_name = name
            
            # Sử dụng PBKDF2 để tạo khóa đối xứng từ mật khẩu người dùng nhập
            salt = b"atbm_salt_fixed"
            self.crypto.session_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000, 16)
            
            self.frame_login.destroy()
            
            # Xây dựng các Widget của Dashboard chính
            self.create_widgets()
            
            self.lbl_admin_name.config(text=f"Quản trị viên: {self.player_name}")
            self.log_event(f"Người chơi '{self.player_name}' đăng nhập thành công.", "success")
            self.log_event("Khóa mã hóa phiên đối xứng đã được dẫn xuất bằng PBKDF2.", "success")
            self.log_event("Cặp khóa RSA 2048-bit của Ngân hàng đã được sinh tự động.", "info")
            self.log_event("Tiêu chuẩn bảo mật áp dụng: AES-GCM (128-bit), RSA-PSS, SHA-512, Nonce + Timestamp chống Replay.", "info")
            
            # Sinh giao dịch đầu tiên
            self.generate_new_transaction()
            self.bind_game_hotkeys()
            
        btn_login = tk.Button(frame_center, text="⚡ KHỞI ĐỘNG HỆ THỐNG GIAO DIỆN ⚡", font=("Helvetica", 11, "bold"), bg=SUCCESS, fg="white", activebackground=SUCCESS, bd=0, relief="flat", padx=20, pady=10, command=on_login)
        btn_login.pack(pady=15)

    def open_settings_window(self):
        """Mở cửa sổ cấu hình Tên người chơi và Mật khẩu mới, tự động băm SHA-256 và lưu file json"""
        self.overlay_frame = tk.Frame(self, bg="#020617")
        self.overlay_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        lbl_lock = tk.Label(self.overlay_frame, text="🔒 CYBERBANK SECURE LOCK - ĐANG CẤU HÌNH TÀI KHOẢN...", font=("Courier New", 12, "bold"), fg="#334155", bg="#020617")
        lbl_lock.place(relx=0.5, rely=0.35, anchor="center")
        
        win_settings = tk.Toplevel(self)
        win_settings.title("CẤU HÌNH TÀI KHOẢN BẢO MẬT")
        win_settings.configure(bg=BG_MAIN)
        win_settings.resizable(False, False)
        
        win_width = 450
        win_height = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - win_width) // 2
        y = (screen_height - win_height) // 2
        win_settings.geometry(f"{win_width}x{win_height}+{x}+{y}")
        
        win_settings.transient(self)
        win_settings.grab_set()
        
        pref_user = "Cuong123"
        pref_pass = "Cuong123"
        try:
            with open(self.credentials_path, "r", encoding="utf-8") as f:
                creds = json.load(f)
            pref_user = creds.get("username", pref_user)
            pref_pass = creds.get("password", pref_pass)
        except Exception:
            pass
            
        lbl_title = tk.Label(win_settings, text="⚙️ CẤU HÌNH TÀI KHOẢN AN NINH", font=("Helvetica", 13, "bold"), fg=ACCENT, bg=BG_MAIN)
        lbl_title.pack(pady=15)
        
        frame_inputs = tk.Frame(win_settings, bg=BG_MAIN)
        frame_inputs.pack(pady=10, padx=20, fill="x")
        frame_inputs.columnconfigure(1, weight=1)
        
        # Tên người chơi
        tk.Label(frame_inputs, text="Tên người chơi mới:", font=("Helvetica", 10, "bold"), fg=TEXT_DARK, bg=BG_MAIN).grid(row=0, column=0, sticky="w", pady=10)
        frame_user = tk.Frame(frame_inputs, bg=BG_CARD, highlightthickness=1, highlightbackground=TEXT_DARK, bd=0)
        frame_user.grid(row=0, column=1, padx=10, pady=10, sticky="we")
        ent_username = tk.Entry(frame_user, font=("Helvetica", 10), bg=BG_CARD, fg=TEXT_LIGHT, insertbackground=TEXT_LIGHT, bd=0)
        ent_username.insert(0, pref_user)
        ent_username.pack(side="left", fill="both", expand=True, padx=8, pady=5)
        
        # Mật khẩu mới
        tk.Label(frame_inputs, text="Mật khẩu mới:", font=("Helvetica", 10, "bold"), fg=TEXT_DARK, bg=BG_MAIN).grid(row=1, column=0, sticky="w", pady=10)
        frame_pass = tk.Frame(frame_inputs, bg=BG_CARD, highlightthickness=1, highlightbackground=TEXT_DARK, bd=0)
        frame_pass.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        ent_password = tk.Entry(frame_pass, font=("Helvetica", 10), bg=BG_CARD, fg=TEXT_LIGHT, show="*", insertbackground=TEXT_LIGHT, bd=0)
        ent_password.insert(0, pref_pass)
        ent_password.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=5)
        
        def toggle_pass():
            if ent_password.cget("show") == "*":
                ent_password.config(show="")
                btn_eye_set.config(text="🙈")
            else:
                ent_password.config(show="*")
                btn_eye_set.config(text="👁")
                
        btn_eye_set = tk.Button(frame_pass, text="👁", font=("Helvetica", 9), bg=BG_CARD, fg=TEXT_LIGHT, activebackground=BG_CARD, activeforeground=TEXT_LIGHT, bd=0, relief="flat", padx=8, cursor="hand2", command=toggle_pass)
        btn_eye_set.pack(side="right", fill="y", padx=(0, 2))
        
        def close_settings():
            self.overlay_frame.destroy()
            win_settings.destroy()
            
        win_settings.protocol("WM_DELETE_WINDOW", close_settings)
        
        def save_settings():
            new_user = ent_username.get().strip()
            new_pass = ent_password.get().strip()
            if not new_user or not new_pass:
                messagebox.showerror("Lỗi nhập liệu", "Vui lòng điền đầy đủ Tên người chơi và Mật khẩu mới!", parent=win_settings)
                return
                
            new_hash = hashlib.sha256(new_pass.encode('utf-8')).hexdigest()
            new_creds = {
                "username": new_user,
                "password": new_pass,
                "password_sha256": new_hash
            }
            
            try:
                with open(self.credentials_path, "w", encoding="utf-8") as f:
                    json.dump(new_creds, f, indent=4, ensure_ascii=False)
                    
                self.player_name = new_user
                self.lbl_admin_name.config(text=f"Quản trị viên: {self.player_name}")
                
                # Cập nhật lại khóa phiên đối xứng
                salt = b"atbm_salt_fixed"
                self.crypto.session_key = hashlib.pbkdf2_hmac('sha256', new_pass.encode('utf-8'), salt, 100000, 16)
                
                self.log_event(f"Tài khoản quản trị được thay đổi thành công: '{new_user}'. Khóa phiên PBKDF2 được dẫn xuất lại.", "success")
                messagebox.showinfo("Thành công", "Đã cập nhật cấu hình tài khoản và lưu vào credentials.json thành công!", parent=win_settings)
                close_settings()
            except Exception as e:
                messagebox.showerror("Lỗi lưu trữ", f"Không thể ghi dữ liệu vào credentials.json: {str(e)}", parent=win_settings)
                
        frame_buttons = tk.Frame(win_settings, bg=BG_MAIN)
        frame_buttons.pack(pady=20)
        
        btn_save = tk.Button(frame_buttons, text="💾 LƯU CẤU HÌNH", font=("Helvetica", 10, "bold"), bg=SUCCESS, fg="white", activebackground=SUCCESS, bd=0, relief="flat", padx=15, pady=8, cursor="hand2", command=save_settings)
        btn_save.pack(side="left", padx=10)
        
        btn_cancel = tk.Button(frame_buttons, text="❌ HỦY BỎ", font=("Helvetica", 10, "bold"), bg=DANGER, fg="white", activebackground=DANGER, bd=0, relief="flat", padx=15, pady=8, cursor="hand2", command=close_settings)
        btn_cancel.pack(side="left", padx=10)

    def create_widgets(self):
        """Xây dựng toàn bộ giao diện dashboard chính"""
        # --- TOP HEADER ---
        frame_header = tk.Frame(self, bg=BG_PANEL, height=80)
        frame_header.pack(fill="x", side="top")
        frame_header.pack_propagate(False)
        
        lbl_title = tk.Label(frame_header, text="CYBERBANK DEFENSE SYSTEM v2.0", font=("Helvetica", 16, "bold"), fg=ACCENT, bg=BG_PANEL)
        lbl_title.pack(side="left", padx=20, pady=10)
        
        self.lbl_admin_name = tk.Label(frame_header, text="Quản trị viên: --", font=("Helvetica", 11, "bold"), fg=TEXT_LIGHT, bg=BG_PANEL)
        self.lbl_admin_name.pack(side="left", padx=30)
        
        btn_settings = tk.Button(frame_header, text="⚙️ Cấu hình", font=("Helvetica", 9, "bold"), bg=BG_CARD, fg=TEXT_LIGHT, activebackground=BG_CARD, activeforeground=TEXT_LIGHT, bd=1, relief="solid", highlightthickness=0, padx=12, pady=5, cursor="hand2", command=self.open_settings_window)
        btn_settings.pack(side="right", padx=15, pady=15)
        
        self.frame_stats = tk.Frame(frame_header, bg=BG_PANEL)
        self.frame_stats.pack(side="right", padx=20)
        
        self.lbl_level = tk.Label(self.frame_stats, text="LEVEL: 1", font=("Helvetica", 11, "bold"), fg=WARNING, bg=BG_PANEL, padx=10)
        self.lbl_level.grid(row=0, column=0)
        
        self.lbl_score = tk.Label(self.frame_stats, text="ĐIỂM: 0", font=("Helvetica", 11, "bold"), fg=SUCCESS, bg=BG_PANEL, padx=10)
        self.lbl_score.grid(row=0, column=1)
        
        self.lbl_blocked = tk.Label(self.frame_stats, text="NGĂN CHẶN: 0", font=("Helvetica", 11, "bold"), fg=DANGER, bg=BG_PANEL, padx=10)
        self.lbl_blocked.grid(row=0, column=2)

        # --- TABS CONTROL ---
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background=BG_MAIN)
        style.configure('TNotebook.Tab', background=BG_PANEL, foreground=TEXT_LIGHT, padding=[15, 6], font=('Helvetica', 10, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', ACCENT)], foreground=[('selected', 'white')])

        # Khởi tạo các Tab
        self.tab_game = tk.Frame(self.notebook, bg=BG_MAIN)
        self.tab_lab = tk.Frame(self.notebook, bg=BG_MAIN)
        self.tab_benchmark = tk.Frame(self.notebook, bg=BG_MAIN)
        self.tab_theory = tk.Frame(self.notebook, bg=BG_MAIN)
        
        self.notebook.add(self.tab_game, text=" 🛡️ ĐIỀU HÀNH BẢO MẬT ")
        self.notebook.add(self.tab_lab, text=" 🧪 PHÒNG THỬ NGHIỆM TẤN CÔNG ")
        self.notebook.add(self.tab_benchmark, text=" 📊 KIỂM THỬ HIỆU NĂNG ")
        self.notebook.add(self.tab_theory, text=" 🎮 HƯỚNG DẪN CHƠI GAME ")
        
        # Xây dựng các Tab (gọi các phương thức từ Mixin)
        self.setup_tab_game()
        self.setup_tab_lab()
        self.setup_tab_benchmark()
        self.setup_tab_theory()

# KHỞI CHẠY CHƯƠNG TRÌNH
if __name__ == "__main__":
    app = BankingApp()
    app.mainloop()
