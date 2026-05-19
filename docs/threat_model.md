# TÀI LIỆU PHÂN TÍCH MÔ HÌNH HIỂM HỌA (THREAT MODELING - STRIDE)

Tài liệu này chi tiết hóa việc phân tích mô hình hiểm họa (Threat Model) cho hệ thống **CyberBank Defense** (Đề tài BTL số 23), tuân thủ định hướng chuyên sâu và báo cáo học thuật.

---

## 1. Xác định tài sản cần bảo vệ (Assets)
*   **Thông tin giao dịch khách hàng (Transaction Data):** Plaintext của giao dịch chứa tên tài khoản người gửi, tên tài khoản người nhận và số tiền giao dịch (Ví dụ: `Alice->Bob:$5,000`). Bản thân dữ liệu này cần được giữ bí mật để tránh rò rỉ thông tin cá nhân và thông tin tài chính.
*   **Khóa mật mã học (Keys):**
    -   **Session Key (Khóa phiên đối xứng):** Dùng để mã hóa/giải mã AES-GCM. Nếu lộ khóa phiên, toàn bộ giao dịch của phiên đó sẽ bị lộ.
    -   **RSA Private Key của Khách hàng:** Dùng để ký số RSA-PSS. Nếu lộ, tin tặc có thể giả mạo danh tính khách hàng để tạo chữ ký số hợp lệ.
*   **Tính đúng đắn của Số dư Ngân hàng (Financial Balance):** Ngăn chặn việc hacker rút cắp tiền bằng cách chỉnh sửa số tiền chuyển hoặc gửi lại nhiều lần một giao dịch hợp lệ.
*   **Nhật ký Giao dịch và An ninh (Audit Logs):** Ghi lại dấu vết nghiệp vụ và phát hiện tấn công để phục vụ điều tra sau này.

---

## 2. Phân tích Chi tiết Hiểm họa theo STRIDE

### 2.1 Spoofing (Mạo danh thực thể)
*   **Mối đe dọa:** Hacker nghe lén được định dạng gói tin, tự tạo ra một yêu cầu chuyển tiền từ tài khoản của nạn nhân (Ví dụ: `Alice->Hacker:$10,000`) và đẩy lên cổng ngân hàng.
*   **Hậu quả:** Ngân hàng bị thất thoát tiền, khách hàng bị mất tài sản oan uổng.
*   **Giải pháp phòng ngự (Countermeasure):**
    -   Mọi giao dịch bắt buộc phải đính kèm **Chữ ký số RSA-PSS 2048-bit** được ký bằng Khóa riêng tư của Khách hàng (`Private_Client`).
    -   Cổng ngân hàng dùng Khóa công khai của khách hàng (`Public_Client`) để xác minh. Kẻ tấn công không có `Private_Client` nên không thể tạo ra chữ ký hợp lệ. Bất kỳ nỗ lực giả mạo nào đều bị phát hiện ngay lập tức ở Bước 1 của quy trình kiểm tra bảo mật.

### 2.2 Tampering (Sửa đổi dữ liệu)
*   **Mối đe dọa:** Hacker can thiệp đường truyền (tấn công Man-in-the-Middle) và thay đổi dữ liệu trong gói tin (Ví dụ: đổi số tài khoản đích từ `Bob` thành `Hacker` hoặc đổi số tiền từ `$100` thành `$10,000`).
*   **Hậu quả:** Giao dịch bị thực hiện sai mục đích, sai đối tượng, gây thiệt hại nghiêm trọng.
*   **Giải pháp phòng ngự (Countermeasure):**
    -   Thông tin giao dịch được mã hóa đối xứng bằng **AES-GCM (AEAD)**. Trong chế độ GCM, quá trình mã hóa tự động sinh ra một Thẻ xác thực **Authentication Tag (MAC)** 16-byte bảo chứng cho cả bản mã và các dữ liệu liên quan.
    -   Hệ thống còn tính toán mã băm **SHA-512** trên toàn bộ bản mã và timestamp.
    -   Khi giải mã, cổng ngân hàng đối chiếu Hash SHA-512 và xác thực MAC Tag. Nếu hacker thay đổi dù chỉ 1 bit của Ciphertext trên đường truyền, quá trình giải mã AES-GCM sẽ thất bại ngay lập tức (`MAC check failed`), bảo vệ toàn vẹn tuyệt đối.

### 2.3 Repudiation (Chối bỏ trách nhiệm)
*   **Mối đe dọa:** Khách hàng thực hiện một lệnh chuyển tiền hợp lệ, nhưng sau đó có ý đồ xấu chối bỏ rằng mình không thực hiện lệnh đó để yêu cầu ngân hàng hoàn lại tiền.
*   **Hậu quả:** Ngân hàng bị tổn thất tài chính và gặp khó khăn trong việc đối soát pháp lý.
*   **Giải pháp phòng ngự (Countermeasure):**
    -   Chữ ký số **RSA-PSS** cung cấp tính chất **Không thể chối bỏ (Non-repudiation)**. 
    -   Vì Khóa riêng tư chỉ có duy nhất khách hàng giữ độc quyền, nên sự tồn tại của một chữ ký số hợp lệ khớp với khóa công khai là bằng chứng pháp lý không thể phủ nhận rằng chính khách hàng đó đã tạo ra giao dịch.

### 2.4 Information Disclosure (Rò rỉ thông tin)
*   **Mối đe dọa:** Tin tặc sử dụng các công cụ Wireshark hoặc nghe lén mạng WiFi để chụp lại các gói tin truyền qua mạng nhằm thu thập số tài khoản và thông tin giao dịch của khách hàng.
*   **Hậu quả:** Vi phạm nghiêm trọng luật bảo vệ dữ liệu cá nhân của ngành tài chính (như PCI-DSS), làm mất uy tín ngân hàng.
*   **Giải pháp phòng ngự (Countermeasure):**
    -   Dữ liệu thô (Plaintext) chứa chi tiết giao dịch được mã hóa hoàn toàn thành Ciphertext ngẫu nhiên bằng thuật toán **AES-128-GCM**.
    -   Tin tặc nghe lén chỉ thu thập được các chuỗi Hex vô nghĩa và không thể giải mã nếu không có khóa phiên. Khóa phiên được dẫn xuất và chia sẻ an toàn qua cơ chế bắt tay bảo mật ban đầu.

### 2.5 Denial of Service / Replay Attack (Tấn công phát lại)
*   **Mối đe dọa:** Hacker chặn (capture) một gói tin giao dịch chuyển tiền hợp lệ và gửi lại (replay) gói tin đó liên tục cho máy chủ ngân hàng (Ví dụ: gửi lại giao dịch `Alice->Bob:$1,000` 50 lần).
*   **Hậu quả:** Bob nhận được $50,000 từ tài khoản của Alice mà Alice không hề hay biết, gây sụp đổ tài chính hệ thống.
*   **Giải pháp phòng ngự (Countermeasure):**
    -   **Mã Nonce độc nhất:** Mỗi giao dịch bắt buộc chứa một mã Nonce (UUID v4 ngẫu nhiên). Cổng ngân hàng lưu trữ tất cả các Nonce đã sử dụng thành công vào Registry Database. Nếu nhận gói tin chứa Nonce trùng lặp -> Từ chối lập tức.
    -   **Giới hạn thời gian (Timestamp):** Gói tin chứa Timestamp thời gian tạo. Cổng ngân hàng chỉ chấp nhận các gói tin có Timestamp chênh lệch không quá 15 giây so với thời gian máy chủ. Nếu hacker thu giữ gói tin và phát lại muộn -> Quá thời hạn hiệu lực -> Từ chối lập tức.

### 2.6 Elevation of Privilege (Leo thang đặc quyền)
*   **Mối đe dọa:** Hacker cố gắng bẻ khóa tài khoản Quản trị viên an ninh ngân hàng (Admin) để chiếm quyền điều hành bảo mật và duyệt khống các giao dịch.
*   **Hậu quả:** Toàn bộ hệ thống ngân hàng bị hacker kiểm soát.
*   **Giải pháp phòng ngự (Countermeasure):**
    -   Ứng dụng yêu cầu đăng nhập quản trị viên nghiêm ngặt.
    -   Mật khẩu quản trị viên được xử lý thông qua thuật toán băm chậm **PBKDF2** kèm **Salt** với 100,000 vòng lặp để dẫn xuất khóa đối xứng. Đảm bảo hacker không thể tấn công từ điển (Dictionary Attack) hay đoán trước khóa đối xứng kể cả khi bộ nhớ đệm bị theo dõi.

---

## 3. Tổng kết Phân tích Rủi ro An ninh
Nhờ áp dụng đầy đủ các kỹ thuật chuyên sâu (AES-GCM, RSA-PSS, SHA-512, PBKDF2, Nonce + Timestamp), **CyberBank Defense** chứng minh khả năng phòng vệ chủ động, triệt tiêu 100% các rủi ro bảo mật chính trong môi trường ngân hàng số hóa.
