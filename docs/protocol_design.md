# TÀI LIỆU THIẾT KẾ GIAO THỨC TRUYỀN TẢI BẢO MẬT (PROTOCOL DESIGN)

Tài liệu này trình bày thiết kế chi tiết về mặt kỹ thuật của giao thức truyền tải bảo mật áp dụng trong hệ thống **CyberBank Defense** (Đề tài BTL số 23), đáp ứng các yêu cầu kiểm thử và mô tả báo cáo.

---

## 1. Các Thực Thể Tham Gia Giao Thức (Entities)
1.  **Client (Khách hàng gửi):** Thiết bị của khách hàng khởi tạo yêu cầu giao dịch tài chính. Sở hữu cặp khóa RSA công khai/riêng tư (`Public_Client`, `Private_Client`) dùng để xác thực.
2.  **Cổng Bảo Mật Ngân Hàng (Bank Gateway):** Máy chủ trung tâm của ngân hàng tiếp nhận giao dịch. Sở hữu cặp khóa RSA công khai/riêng tư (`Public_Bank`, `Private_Bank`) và cơ sở dữ liệu registry.
3.  **Kênh truyền mạng:** Kênh truyền dẫn dữ liệu không an toàn (Internet), có nguy cơ bị hacker nghe lén, sửa đổi hoặc phát lại gói tin.

---

## 2. Các Bước Thực Hiện Quy Trình Bảo Mật Chi Tiết

Giao thức được phân chia thành 3 giai đoạn chính:

### Giai đoạn 1: Bắt tay (Handshake) & Tạo khóa phiên (Session Key)
1.  **Đăng nhập Quản trị viên:** Quản trị viên nhập mật khẩu bảo vệ trên giao diện.
2.  **Dẫn xuất khóa PBKDF2:** Hệ thống áp dụng hàm dẫn xuất khóa **PBKDF2** trên mật khẩu thô và chuỗi Salt tĩnh:
    $$\text{SessionKey} = \text{PBKDF2}(\text{Password}, \text{Salt}, \text{iterations}=100000, \text{key\_length}=16 \text{ bytes})$$
    Khóa phiên này được sử dụng chung cho việc mã hóa/giải mã đối xứng các thông tin giao dịch trong suốt phiên làm việc.

### Giai đoạn 2: Xác thực & Ký số (RSA-PSS Digital Signature)
Để chứng minh danh tính và chống chối bỏ trách nhiệm, Client tạo chữ ký số trên metadata của giao dịch:
1.  **Chuẩn bị Metadata:** 
    $$\text{Metadata} = \text{Sender} \parallel \text{Timestamp} \parallel \text{Nonce}$$
    *Trong đó: Nonce là mã UUID v4 độc nhất; Timestamp là mốc thời gian tạo giao dịch chính xác.*
2.  **Ký số RSA-PSS:** Client sử dụng khóa riêng của mình (`Private_Client`) kết hợp hàm băm **SHA-512** và cơ chế ngẫu nhiên hóa PSS để tạo ra chữ ký:
    $$\text{Signature} = \text{RSA-PSS.Sign}(\text{Private\_Client}, \text{SHA-512}(\text{Metadata}))$$

### Giai đoạn 3: Mã hóa dữ liệu & Kiểm tra tính toàn vẹn (AES-GCM & SHA-512)
Để bảo mật tuyệt đối số tiền chuyển và tài khoản thụ hưởng, Client thực hiện mã hóa và băm toàn vẹn:
1.  **Mã hóa AES-GCM:** Client sử dụng khóa phiên đối xứng `SessionKey` mã hóa thông tin giao dịch (`Plaintext = Sender->Receiver:Amount`) dưới chế độ GCM:
    $$(\text{Ciphertext}, \text{Tag}, \text{GCM\_Nonce}) = \text{AES-GCM.Encrypt}(\text{SessionKey}, \text{Plaintext})$$
    *Trong đó: Tag là Thẻ xác thực mật mã 16-byte bảo chứng; GCM\_Nonce là tham số IV ngẫu nhiên.*
2.  **Đóng gói gói tin mã hóa:**
    $$\text{Ciphertext\_Packet} = \text{Ciphertext} \parallel \text{Tag} \parallel \text{GCM\_Nonce}$$
3.  **Tính mã băm toàn vẹn:** Client tính toán hash SHA-512 trên bản mã và timestamp gửi đi:
    $$\text{Hash} = \text{SHA-512}(\text{Ciphertext\_Packet} \parallel \text{Timestamp})$$
4.  **Truyền tải:** Gói tin hoàn chỉnh gửi đi qua mạng chứa:
    $$\text{Packet} = \{ \text{Metadata}, \text{Signature}, \text{Ciphertext\_Packet}, \text{Hash} \}$$

---

## 3. Quy Trình Tiếp Nhận & Xác Thực tại Cổng Ngân Hàng (Gateway Audit)

Khi nhận được gói tin giao dịch từ mạng gửi đến, Cổng bảo mật Ngân hàng tiến hành kiểm tra tuần tự 4 bước bảo mật:

```
[Nhận Gói Tin] 
      │
      ▼
┌────────────────────────────────────────────────────────┐
│ BƯỚC 1: Xác minh Chữ ký số RSA-PSS của Khách hàng      │
│ ─► RSA-PSS.Verify(Public_Client, Metadata, Signature)  │
└───────────────────────────┬────────────────────────────┘
                            │
                  ┌─────────┴─────────┐
                  ▼ Hợp lệ            ▼ Sai Chữ ký
┌───────────────────────────────────┐ ┌──────────────────────────────────┐
│ BƯỚC 2: Kiểm tra Timestamp        │ │ TỪ CHỐI GIAO DỊCH                │
│ ─► Age = Hiện tại - Timestamp     │ │ Log: [CRITICAL] Mạo danh thực thể│
│ ─► Yêu cầu: Age <= 15 giây        │ └──────────────────────────────────┘
└─────────────────┬─────────────────┘
                  │
        ┌─────────┴─────────┐
        ▼ Chưa Quá hạn      ▼ Quá hạn (> 15s)
┌───────────────────────────────────┐ ┌──────────────────────────────────┐
│ BƯỚC 3: Đối chiếu mã Nonce        │ │ TỪ CHỐI GIAO DỊCH                │
│ ─► Kiểm tra Nonce trong Database  │ │ Log: [WARNING] Giao dịch quá hạn │
└─────────────────┬─────────────────┘ └──────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        ▼ Chưa tồn tại      ▼ Đã tồn tại (Trùng)
┌───────────────────────────────────┐ ┌──────────────────────────────────┐
│ BƯỚC 4: Kiểm tra Hash & AES-GCM   │ │ TỪ CHỐI GIAO DỊCH                │
│ ─► SHA-512(Ciphertext||Time)      │ │ Log: [CRITICAL] Tấn công phát lại│
│ ─► AES-GCM.Decrypt(SessionKey)    │ └──────────────────────────────────┘
└─────────────────┬─────────────────┘
                  │
        ┌─────────┴─────────┐
        ▼ Khớp Hash & Tag   ▼ MAC Tag lỗi / Sai Hash
┌───────────────────────────────────┐ ┌──────────────────────────────────┐
│ CHẤP THUẬN GIAO DỊCH (ACK)        │ │ TỪ CHỐI GIAO DỊCH                │
│ ─► Cộng tiền cho tài khoản nhận   │ │ Log: [CRITICAL] Lỗi toàn vẹn/MAC │
│ ─► Lưu Nonce vào Registry         │ └──────────────────────────────────┘
└───────────────────────────────────┘
```

---

## 4. Tại Sao Thiết Kế Giao Thức Này An Toàn Tuyệt Đối?

1.  **Phòng ngừa Tấn công Trung gian (MITM) & Thay đổi dữ liệu:** Bất kỳ sự sửa đổi nào trên `Ciphertext_Packet` hoặc `Timestamp` đều dẫn đến sự sai lệch mã băm **SHA-512** ở Bước 3. Thậm chí nếu kẻ tấn công thông minh sửa đổi cả mã băm, quá trình giải mã **AES-GCM** ở Bước 4 cũng sẽ thất bại do Thẻ xác thực **Tag** (được tính toán mật mã bằng SessionKey) không trùng khớp, đảm bảo an toàn tuyệt đối.
2.  **Phòng ngừa Tấn công Phát lại (Replay Attack):** Kẻ tấn công thu giữ gói tin và phát lại lập tức sẽ bị chặn lại ở Bước 3 do hệ thống phát hiện **Nonce trùng lặp**. Nếu kẻ tấn công đợi lâu mới phát lại, Timestamp của gói tin sẽ cũ hơn 15 giây và bị từ chối ở Bước 2 do **Hết hạn thời gian**.
3.  **Phòng ngừa Giả mạo thực thể:** Kẻ tấn công không thể tự tạo ra giao dịch hợp lệ nhân danh nạn nhân do không sở hữu Khóa riêng tư (`Private_Client`). Bất kỳ nỗ lực tạo chữ ký giả mạo nào đều bị cổng ngân hàng phát hiện và từ chối ở Bước 1.
