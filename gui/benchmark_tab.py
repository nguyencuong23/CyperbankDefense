# -*- coding: utf-8 -*-
"""
HỆ THỐNG MÃ HÓA NGÂN HÀNG - CYBERBANK DEFENSE GAME
Mixin quản lý Tab 3: Kiểm thử hiệu năng (BenchmarkTabMixin)
"""

import tkinter as tk
import time

from Crypto.Cipher import AES, DES, DES3
from Crypto.Hash import SHA512, SHA256
from Crypto.Random import get_random_bytes

from config import (
    BG_MAIN, BG_PANEL, BG_CARD, ACCENT, SUCCESS, WARNING, DANGER,
    TEXT_LIGHT, TEXT_DARK, TERMINAL_BG
)

class BenchmarkTabMixin:
    """Mixin cung cấp giao diện và lô-gích so sánh hiệu năng mật mã cho BankingApp"""
    
    def setup_tab_benchmark(self):
        self.tab_benchmark.columnconfigure(0, weight=4)
        self.tab_benchmark.columnconfigure(1, weight=6)
        self.tab_benchmark.rowconfigure(0, weight=1)
        
        # --- CỘT TRÁI: ĐIỀU KHIỂN & CẤU HÌNH BENCHMARK ---
        frame_ctrl = tk.Frame(self.tab_benchmark, bg=BG_PANEL, bd=1, relief="solid")
        frame_ctrl.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        tk.Label(frame_ctrl, text="⚙️ CẤU HÌNH ĐO LƯỜNG HIỆU NĂNG", font=("Helvetica", 11, "bold"), fg=TEXT_LIGHT, bg=BG_PANEL).pack(pady=15)
        
        # Lựa chọn Kích thước dữ liệu mẫu để mã hóa
        tk.Label(frame_ctrl, text="Chọn kích thước dữ liệu thử nghiệm:", font=("Helvetica", 10), fg=TEXT_LIGHT, bg=BG_PANEL).pack(anchor="w", padx=20, pady=5)
        self.bench_size_var = tk.StringVar(value="100KB")
        
        frame_sizes = tk.Frame(frame_ctrl, bg=BG_PANEL)
        frame_sizes.pack(fill="x", padx=20, pady=5)
        
        tk.Radiobutton(frame_sizes, text="Nhỏ (10 KB)", font=("Helvetica", 9), variable=self.bench_size_var, value="10KB", bg=BG_PANEL, fg=TEXT_LIGHT, selectcolor=BG_PANEL, activebackground=BG_PANEL).pack(side="left", padx=5)
        tk.Radiobutton(frame_sizes, text="Vừa (100 KB)", font=("Helvetica", 9), variable=self.bench_size_var, value="100KB", bg=BG_PANEL, fg=TEXT_LIGHT, selectcolor=BG_PANEL, activebackground=BG_PANEL).pack(side="left", padx=5)
        tk.Radiobutton(frame_sizes, text="Lớn (1 MB)", font=("Helvetica", 9), variable=self.bench_size_var, value="1MB", bg=BG_PANEL, fg=TEXT_LIGHT, selectcolor=BG_PANEL, activebackground=BG_PANEL).pack(side="left", padx=5)
        
        # Lựa chọn số vòng lặp kiểm thử
        tk.Label(frame_ctrl, text="Số vòng lặp (Iterations):", font=("Helvetica", 10), fg=TEXT_LIGHT, bg=BG_PANEL).pack(anchor="w", padx=20, pady=5)
        self.bench_iter_var = tk.IntVar(value=10)
        spin_iter = tk.Spinbox(frame_ctrl, from_=1, to=100, textvariable=self.bench_iter_var, font=("Helvetica", 10), bg=BG_CARD, fg=TEXT_LIGHT, width=10, buttonbackground=BG_PANEL)
        spin_iter.pack(anchor="w", padx=20, pady=5)
        
        # Nút chạy đo lường
        btn_run_bench = tk.Button(frame_ctrl, text="🚀 CHẠY ĐÁNH GIÁ SO SÁNH", font=("Helvetica", 11, "bold"), bg=SUCCESS, fg="white", activebackground=SUCCESS, relief="flat", command=self.run_performance_benchmark)
        btn_run_bench.pack(fill="x", padx=20, pady=25)
        
        # Kết quả dạng văn bản dưới nút điều khiển
        tk.Label(frame_ctrl, text="BẢNG SỐ LIỆU ĐO LƯỜNG THỰC TẾ:", font=("Helvetica", 10, "bold"), fg=WARNING, bg=BG_PANEL).pack(anchor="w", padx=20, pady=5)
        self.txt_bench_results = tk.Text(frame_ctrl, bg=TERMINAL_BG, fg=TEXT_LIGHT, font=("Courier New", 9), height=15)
        self.txt_bench_results.pack(fill="both", expand=True, padx=15, pady=10)

        # --- CỘT PHẢI: BIỂU ĐỒ TRỰC QUAN (LIVE CHART) ---
        frame_chart = tk.Frame(self.tab_benchmark, bg=BG_MAIN)
        frame_chart.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        tk.Label(frame_chart, text="📊 BIỂU ĐỒ SO SÁNH TỐC ĐỘ XỬ LÝ ( throughput - cao hơn tốt hơn )", font=("Helvetica", 11, "bold"), fg=ACCENT, bg=BG_MAIN).pack(pady=10)
        
        # Sử dụng Canvas vẽ biểu đồ cột
        self.canvas_chart = tk.Canvas(frame_chart, bg=BG_PANEL, highlightthickness=1, highlightbackground=ACCENT)
        self.canvas_chart.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Vẽ lưới biểu đồ ban đầu
        self.draw_empty_chart()

    def draw_empty_chart(self):
        """Vẽ khung biểu đồ trống"""
        self.canvas_chart.delete("all")
        
        # Vẽ các trục tọa độ
        self.canvas_chart.create_line(70, 40, 70, 360, fill=TEXT_DARK, width=2)   # Trục Y
        self.canvas_chart.create_line(70, 360, 520, 360, fill=TEXT_DARK, width=2) # Trục X
        
        # Tiêu đề trục
        self.canvas_chart.create_text(30, 200, text="Tốc độ (MB/s)", font=("Helvetica", 9, "bold"), fill=TEXT_LIGHT, angle=90)
        self.canvas_chart.create_text(300, 385, text="Các thuật toán Mã hóa và Băm", font=("Helvetica", 9, "bold"), fill=TEXT_LIGHT)
        
        # Mốc giá trị trục Y giả lập
        for i in range(5):
            y = 360 - i * 70
            self.canvas_chart.create_line(65, y, 70, y, fill=TEXT_DARK)
            self.canvas_chart.create_text(50, y, text=str(i * 25), font=("Helvetica", 8), fill=TEXT_DARK)

    def run_performance_benchmark(self):
        """Chạy đánh giá so sánh hiệu năng các thuật toán: AES-GCM, 3DES, DES, SHA-512, SHA-256"""
        size_str = self.bench_size_var.get()
        iterations = self.bench_iter_var.get()
        
        # Xác định kích thước byte thực tế
        if size_str == "10KB":
            data_size = 10 * 1024
        elif size_str == "100KB":
            data_size = 100 * 1024
        else:
            data_size = 1024 * 1024 # 1 MB
            
        self.txt_bench_results.delete("1.0", tk.END)
        self.txt_bench_results.insert(tk.END, f"--- BẮT ĐẦU ĐO LƯỜNG HIỆU NĂNG ---\n")
        self.txt_bench_results.insert(tk.END, f"Dữ liệu mẫu: {size_str} ({data_size:,} bytes)\n")
        self.txt_bench_results.insert(tk.END, f"Số lần chạy trung bình: {iterations}\n")
        self.txt_bench_results.insert(tk.END, "Vui lòng đợi hệ thống tính toán...\n\n")
        self.update()
        
        # Sinh dữ liệu mẫu ngẫu nhiên
        test_data = get_random_bytes(data_size)
        
        results = {}
        
        # 1. BENCHMARK AES-GCM
        t_start = time.perf_counter()
        for _ in range(iterations):
            key = get_random_bytes(16)
            cipher = AES.new(key, AES.MODE_GCM)
            c, tag = cipher.encrypt_and_digest(test_data)
        t_end = time.perf_counter()
        t_aes = (t_end - t_start) / iterations
        throughput_aes = (data_size / (1024 * 1024)) / t_aes if t_aes > 0 else 0
        results["AES-GCM"] = throughput_aes
        self.txt_bench_results.insert(tk.END, f"AES-GCM (128-bit):\n  - Time: {t_aes*1000:.3f} ms\n  - Speed: {throughput_aes:.2f} MB/s\n\n")
        self.update()

        # 2. BENCHMARK Triple DES (3DES)
        t_start = time.perf_counter()
        for _ in range(iterations):
            key = DES3.adjust_key_parity(get_random_bytes(24))
            cipher = DES3.new(key, DES3.MODE_ECB)
            pad_len = 8 - (len(test_data) % 8)
            padded = test_data + bytes([pad_len] * pad_len)
            c = cipher.encrypt(padded)
        t_end = time.perf_counter()
        t_3des = (t_end - t_start) / iterations
        throughput_3des = (data_size / (1024 * 1024)) / t_3des if t_3des > 0 else 0
        results["3DES"] = throughput_3des
        self.txt_bench_results.insert(tk.END, f"Triple DES (3DES):\n  - Time: {t_3des*1000:.3f} ms\n  - Speed: {throughput_3des:.2f} MB/s\n\n")
        self.update()

        # 3. BENCHMARK DES
        t_start = time.perf_counter()
        for _ in range(iterations):
            key = get_random_bytes(8)
            cipher = DES.new(key, DES.MODE_ECB)
            pad_len = 8 - (len(test_data) % 8)
            padded = test_data + bytes([pad_len] * pad_len)
            c = cipher.encrypt(padded)
        t_end = time.perf_counter()
        t_des = (t_end - t_start) / iterations
        throughput_des = (data_size / (1024 * 1024)) / t_des if t_des > 0 else 0
        results["DES"] = throughput_des
        self.txt_bench_results.insert(tk.END, f"DES (Legacy):\n  - Time: {t_des*1000:.3f} ms\n  - Speed: {throughput_des:.2f} MB/s\n\n")
        self.update()

        # 4. BENCHMARK SHA-256
        t_start = time.perf_counter()
        for _ in range(iterations):
            h = SHA256.new(test_data)
            digest = h.digest()
        t_end = time.perf_counter()
        t_sha256 = (t_end - t_start) / iterations
        throughput_sha256 = (data_size / (1024 * 1024)) / t_sha256 if t_sha256 > 0 else 0
        results["SHA-256"] = throughput_sha256
        self.txt_bench_results.insert(tk.END, f"SHA-256:\n  - Time: {t_sha256*1000:.3f} ms\n  - Speed: {throughput_sha256:.2f} MB/s\n\n")
        self.update()

        # 5. BENCHMARK SHA-512
        t_start = time.perf_counter()
        for _ in range(iterations):
            h = SHA512.new(test_data)
            digest = h.digest()
        t_end = time.perf_counter()
        t_sha512 = (t_end - t_start) / iterations
        throughput_sha512 = (data_size / (1024 * 1024)) / t_sha512 if t_sha512 > 0 else 0
        results["SHA-512"] = throughput_sha512
        self.txt_bench_results.insert(tk.END, f"SHA-512:\n  - Time: {t_sha512*1000:.3f} ms\n  - Speed: {throughput_sha512:.2f} MB/s\n\n")
        
        self.txt_bench_results.insert(tk.END, "--- ĐO LƯỜNG HOÀN TẤT ---")
        
        # Vẽ kết quả lên Biểu đồ
        self.draw_benchmark_chart(results)

    def draw_benchmark_chart(self, results):
        """Vẽ biểu đồ cột trực quan dựa trên kết quả đo lường thực tế"""
        self.canvas_chart.delete("all")
        
        # Tìm giá trị lớn nhất để căn tỉ lệ (Scale) biểu đồ
        max_val = max(results.values())
        if max_val == 0: max_val = 1
        
        # Làm tròn max_val lên để vẽ trục tọa độ Y cho đẹp
        y_max_label = int(max_val * 1.2)
        if y_max_label < 10: y_max_label = 10
        
        # Vẽ lại trục tọa độ
        self.canvas_chart.create_line(70, 40, 70, 340, fill=TEXT_LIGHT, width=2)   # Trục Y
        self.canvas_chart.create_line(70, 340, 520, 340, fill=TEXT_LIGHT, width=2) # Trục X
        
        self.canvas_chart.create_text(30, 190, text="Tốc độ xử lý (MB/s)", font=("Helvetica", 9, "bold"), fill=TEXT_LIGHT, angle=90)
        self.canvas_chart.create_text(295, 380, text="Các thuật toán được so sánh", font=("Helvetica", 9, "bold"), fill=TEXT_LIGHT)
        
        # Vẽ các mốc tọa độ trục Y
        for i in range(6):
            y_val = (y_max_label / 5) * i
            y_pos = 340 - (300 / 5) * i
            self.canvas_chart.create_line(65, y_pos, 70, y_pos, fill=TEXT_DARK)
            self.canvas_chart.create_text(45, y_pos, text=f"{y_val:.1f}", font=("Helvetica", 8), fill=TEXT_DARK)
            
        # Vẽ cột cho các thuật toán
        colors = {
            "AES-GCM": SUCCESS,
            "DES": WARNING,
            "3DES": DANGER,
            "SHA-256": ACCENT,
            "SHA-512": "#A855F7" # Purple
        }
        
        keys = list(results.keys())
        bar_width = 45
        gap = 40
        
        for idx, name in enumerate(keys):
            val = results[name]
            
            # Tính chiều cao cột
            bar_height = (val / y_max_label) * 300
            
            x1 = 90 + idx * (bar_width + gap)
            y1 = 340 - bar_height
            x2 = x1 + bar_width
            y2 = 340
            
            # Vẽ cột
            color = colors.get(name, ACCENT)
            self.canvas_chart.create_rectangle(x1, y1, x2, y2, fill=color, outline="white", width=1)
            
            # Ghi số liệu trên đỉnh cột
            self.canvas_chart.create_text((x1 + x2)/2, y1 - 10, text=f"{val:.1f}", font=("Helvetica", 8, "bold"), fill=TEXT_LIGHT)
            
            # Nhãn tên cột
            self.canvas_chart.create_text((x1 + x2)/2, 355, text=name, font=("Helvetica", 9, "bold"), fill=TEXT_LIGHT)
            
        # Vẽ khung giải thích (Legend)
        self.canvas_chart.create_rectangle(380, 20, 520, 110, fill=BG_MAIN, outline=TEXT_DARK)
        self.canvas_chart.create_rectangle(390, 30, 405, 40, fill=SUCCESS, outline="")
        self.canvas_chart.create_text(415, 35, text="AES-GCM (Nhanh nhất)", font=("Helvetica", 7), fill=TEXT_LIGHT, anchor="w")
        self.canvas_chart.create_rectangle(390, 50, 405, 60, fill=DANGER, outline="")
        self.canvas_chart.create_text(415, 55, text="3DES (Chậm, cổ điển)", font=("Helvetica", 7), fill=TEXT_LIGHT, anchor="w")
        self.canvas_chart.create_rectangle(390, 70, 405, 80, fill=ACCENT, outline="")
        self.canvas_chart.create_text(415, 75, text="SHA-256", font=("Helvetica", 7), fill=TEXT_LIGHT, anchor="w")
        self.canvas_chart.create_rectangle(390, 90, 405, 100, fill="#A855F7", outline="")
        self.canvas_chart.create_text(415, 95, text="SHA-512 (An toàn cao)", font=("Helvetica", 7), fill=TEXT_LIGHT, anchor="w")
