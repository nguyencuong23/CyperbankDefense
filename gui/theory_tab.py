# -*- coding: utf-8 -*-
"""
HỆ THỐNG MÃ HÓA NGÂN HÀNG - CYBERBANK DEFENSE GAME
Mixin quản lý Tab 4: Hướng dẫn chơi game (TheoryTabMixin)
"""

import tkinter as tk
from tkinter import scrolledtext

from config import BG_PANEL, TEXT_LIGHT

class TheoryTabMixin:
    """Mixin cung cấp giao diện và tài liệu hướng dẫn cho BankingApp"""
    
    def setup_tab_theory(self):
        # Dùng canvas cuộn hiển thị Cẩm nang Hướng dẫn chơi game chi tiết
        self.tab_theory.columnconfigure(0, weight=1)
        self.tab_theory.rowconfigure(0, weight=1)
        
        txt_theory = scrolledtext.ScrolledText(self.tab_theory, bg=BG_PANEL, fg=TEXT_LIGHT, font=("Helvetica", 11), padx=20, pady=20)
        txt_theory.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        content = """🎮 CẨM NANG HƯỚNG DẪN CHƠI GAME & ĐIỀU HÀNH AN NINH CYBERBANK

Chào mừng bạn đến với Cổng kiểm soát an ninh tối cao của Ngân hàng CyberBank!
Dưới đây là hướng dẫn chi tiết và các bước vận hành hệ thống để bạn hoàn thành nhiệm vụ xuất sắc và đạt điểm tối đa (+100 điểm).

---
🛡️ PHẦN I: MỤC TIÊU NHIỆM VỤ CỦA BẠN

Bạn đóng vai là "Quản trị viên An ninh" tối cao của Ngân hàng CyberBank.
Hệ thống sẽ liên tục tiếp nhận các giao dịch chuyển tiền tự động từ khách hàng gửi về hàng đợi.
Nhiệm vụ của bạn là:
1. Thẩm định bảo mật từng giao dịch để phát hiện các cuộc tấn công mạng của Hacker.
2. Phê duyệt (Approve) ngay lập tức đối với các giao dịch HỢP LỆ để thông suốt dòng tiền.
3. Chặn đứng & Phát báo động (Block & Alarm) đối với các giao dịch bị HACKER TẤN CÔNG (giả mạo, sửa đổi số tiền, phát lại gói tin cũ).

* Điểm số: Bạn sẽ được cộng 10 điểm cho mỗi phán quyết chính xác và bị trừ điểm nếu quyết định sai!

---
⚡ PHẦN II: 4 BƯỚC THẨM ĐỊNH BẢO MẬT CHỦ ĐỘNG

Khi một giao dịch mới xuất hiện ở màn hình "🛡️ ĐIỀU HÀNH BẢO MẬT":
Ở nửa bên trái, bạn sẽ nhìn thấy thông tin giao dịch bao gồm số tiền, người gửi, bản mã hóa AES, chữ ký số RSA, mã băm SHA-512, mã Nonce độc nhất và Timestamp của gói tin.

Để thẩm định, hãy lần lượt click vào 4 nút kiểm tra bảo mật ở khung bên phải:

1. Bước 1: 🔑 KIỂM TRA CHỮ KÝ RSA (RSA Signature Check)
   - Mục đích: Xác minh danh tính người gửi tiền xem có đúng là chủ tài khoản không.
   - Nguyên lý: Sử dụng thuật toán ký số RSA-PSS 2048-bit.
   - Kết quả: Nếu chữ ký không khớp (FAIL) -> Hacker đang giả mạo người gửi!

2. Bước 2: 🔍 KIỂM TRA TOÀN VẸN HASH SHA-512 (SHA-512 Integrity Check)
   - Mục đích: Kiểm tra xem gói tin giao dịch có bị sửa đổi nội dung trên đường truyền mạng hay không.
   - Nguyên lý: Sử dụng hàm băm bảo mật SHA-512 để băm toàn bộ gói tin và đối chiếu băm đính kèm.
   - Kết quả: Nếu băm không khớp (FAIL) -> Gói tin đã bị Hacker thay đổi thông tin (ví dụ: đổi số tài khoản nhận tiền).

3. Bước 3: 🔒 GIẢI MÃ & KIỂM TRA MAC AES-GCM (Decrypt & AEAD Verify)
   - Mục đích: Giải mã dữ liệu giao dịch và kiểm tra Thẻ xác thực (Authentication Tag) bảo mật.
   - Nguyên lý: Sử dụng thuật toán AES-128-GCM (mã hóa có xác thực).
   - Kết quả: Nếu giải mã thất bại hoặc sai thẻ xác thực MAC (FAIL) -> Hacker đã can thiệp thay đổi bản mã giao dịch!

4. Bước 4: ⏱️ KIỂM TRA PHÁT LẠI - NONCE & TIMESTAMP (Anti-Replay Verification)
   - Mục đích: Chặn đứng tấn công phát lại (Hacker chặn gói tin giao dịch cũ hợp lệ rồi gửi đi gửi lại nhiều lần để rút trộm tiền).
   - Nguyên lý: Đối chiếu mã số dùng một lần (Nonce UUID) trong Database và kiểm tra xem Timestamp ký số có bị trễ quá 15 giây hay không.
   - Kết quả: Nếu trùng Nonce cũ hoặc thời gian trễ quá 15 giây (FAIL) -> Đây là cuộc tấn công Replay Attack!

---
👉 PHẦN III: ĐƯA RA PHÁN QUYẾT CUỐI CÙNG

Sau khi đã click chạy đủ 4 bước kiểm tra bảo mật ở trên, hãy nhìn vào kết quả thẩm định:
- Nếu TẤT CẢ 4 BƯỚC ĐỀU BÁO XANH (OK - Đạt chuẩn): Giao dịch hoàn toàn an toàn và hợp pháp!
  👉 Hãy click nút màu xanh: [⚡ PHÊ DUYỆT GIAO DỊCH]
- Nếu CÓ ÍT NHẤT 1 BƯỚC BÁO ĐỎ (FAIL - Thất bại): Đây chắc chắn là giao dịch bị tấn công!
  👉 Hãy click nút màu đỏ: [🚨 CHẶN & BÁO ĐỘNG TẤN CÔNG]

Hệ thống sẽ ngay lập tức ghi nhận phán quyết của bạn, cập nhật điểm số và tải giao dịch tiếp theo lên hàng đợi!

---
🧪 PHẦN IV: THỰC HÀNH TẠI "PHÒNG THỬ NGHIỆM TẤN CÔNG" (SANDBOX LAB)

Bạn muốn tận mắt xem Hacker tấn công thế nào và hệ thống phòng thủ phản ứng ra sao?
Hãy chuyển sang Tab "🧪 PHÒNG THỬ NGHIỆM TẤN CÔNG". Tại đây bạn đóng vai Hacker mũ đen và có thể kích hoạt 4 kiểu tấn công thực tế vào giao dịch hiện tại:
- Sửa đổi Bản mã: Xem AES-GCM phát hiện sửa dữ liệu nhạy cảm cực nhạy ra sao.
- Phát lại Nonce cũ: Xem Registry của Ngân hàng từ chối Nonce đã sử dụng thế nào.
- Làm hết hạn gói tin: Đưa thời gian ký lùi về quá khứ để xem máy chủ từ chối gói tin quá hạn thế nào.
- Giả mạo chữ ký RSA: Mạo danh chữ ký của Alice để xem khóa công khai RSA phát hiện ra sao.

* Mọi thông tin phản hồi, lỗi giải mã, lỗi xác thực chữ ký sẽ được in chi tiết trên Terminal giả lập Cyberpunk ở bên dưới để bạn dễ dàng quan sát, chụp ảnh đưa vào Báo cáo bài tập lớn!

Chúc bạn có những trải nghiệm học tập và chơi game tuyệt vời cùng CyberBank Defense!
"""
        txt_theory.insert(tk.END, content)
        txt_theory.config(state="disabled")
