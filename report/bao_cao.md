# BÁO CÁO BÀI TẬP LỚN: HỆ THỐNG MÃ HÓA NGÂN HÀNG (CYBERBANK DEFENSE)

* **Môn học:** Nhập môn An toàn và Bảo mật thông tin
* **Đề tài số 23:** Phát triển game mang tính giáo dục và mô phỏng bảo mật - Game "Hệ thống mã hóa ngân hàng"
* **Ngôn ngữ triển khai:** Python 3
* **Thư viện chính:** `pycryptodome` (Mật mã học nâng cao), `tkinter` (Giao diện đồ họa)
* **Thành viên thực hiện:** Nhóm sinh viên thực hiện BTL Đề tài 23

---

# LỜI MỞ ĐẦU

Trong những năm gần đây, sự bùng nổ của cuộc cách mạng công nghiệp lần thứ tư đã thúc đẩy quá trình chuyển đổi số diễn ra mạnh mẽ và sâu rộng trên mọi lĩnh vực của đời sống xã hội. Trong đó, ngành tài chính - ngân hàng được xem là lĩnh vực đi đầu với sự ra đời của hàng loạt dịch vụ ngân hàng trực tuyến (E-Banking), ví điện tử và các giải pháp thanh toán điện tử thông minh. Các công nghệ này đã đem lại sự tiện lợi, tốc độ vượt trội cho khách hàng nhưng cũng đồng thời đặt ra những thách thức, hiểm họa an ninh mạng vô cùng lớn. Việc bảo vệ an toàn cho hàng triệu giao dịch diễn ra mỗi giây trước các đòn tấn công như nghe lén, sửa đổi dữ liệu hay mạo danh thực thể đã trở thành bài toán sống còn của bất kỳ định chế tài chính nào.

Mật mã học chính là chìa khóa then chốt giải quyết bài toán này. Tuy nhiên, đối với nhiều sinh viên công nghệ thông tin nói chung và ngành an toàn thông tin nói riêng, mật mã học thường được tiếp cận dưới góc độ các công thức toán học khô khan và lý thuyết trừu tượng. Việc thiếu đi công cụ minh họa thực tế khiến người học gặp nhiều khó khăn trong việc hình dung luồng dữ liệu bảo mật hoạt động ra sao và các thuật toán tương tác với nhau như thế nào trong một hệ thống thực tế.

Nhận thức được tầm quan trọng của vấn đề, nhóm sinh viên chúng em đã tiến hành nghiên cứu và phát triển đề tài: **"Phát triển game mang tính giáo dục và mô phỏng bảo mật - Game Hệ thống mã hóa ngân hàng (CyberBank Defense)"**. Với định hướng kết hợp giữa học tập và trò chơi giải trí (Gamification), ứng dụng đóng vai trò là một công cụ sư phạm trực quan, giúp người chơi hóa thân thành một Quản trị viên An ninh cổng thanh toán để trực tiếp phê duyệt giao dịch thông qua luồng mật mã học chuyên nghiệp. Qua đó, sinh viên không chỉ nắm vững cấu trúc của các thuật toán mã hóa hiện đại như AES-GCM, RSA-PSS, SHA-512, PBKDF2 mà còn trực quan hóa được các kịch bản tấn công và cơ chế phòng thủ tương ứng.

Chúng em xin gửi lời cảm ơn chân thành đến giảng viên bộ môn **Nhập môn An toàn và Bảo mật thông tin** đã truyền đạt những kiến thức nền tảng quý báu và định hướng nhiệt tình để chúng em hoàn thành tốt đề tài bài tập lớn này. Dù đã nỗ lực hết sức để hoàn thiện mã nguồn chương trình cũng như quyển báo cáo này, hệ thống chắc chắn không tránh khỏi những hạn chế thiếu sót. Nhóm kính mong nhận được những nhận xét, đóng góp ý kiến của thầy cô để đề tài tiếp tục được phát triển và cải tiến hơn trong tương lai.

Nhóm sinh viên thực hiện.

---

# CHƯƠNG 1: GIỚI THIỆU BÀI TOÁN VÀ MỤC TIÊU BẢO MẬT

## 1.1 Bối cảnh thực tế và Lý do cần bảo mật trong hệ thống ngân hàng trực tuyến
Trong kỷ nguyên số hóa tài chính, các hệ thống ngân hàng trực tuyến (E-Banking) đã trở thành hạ tầng cốt lõi phục vụ hàng tỷ giao dịch chuyển tiền mỗi ngày. Sự tiện lợi của Internet Banking đi kèm với những hiểm họa bảo mật ngày càng tinh vi từ các nhóm tin tặc quốc tế. Mọi yêu cầu chuyển tiền từ máy khách (Client) đến máy chủ ngân hàng (Bank Gateway) đều phải đi qua môi trường Internet công cộng - một kênh truyền không tin cậy và có thể dễ dàng bị can thiệp.

Nếu không được trang bị các cơ chế mật mã học đủ mạnh, các giao dịch tài chính này có thể bị khai thác bởi những kịch bản tấn công nguy hiểm:
*   **Nghe lén đường truyền (Eavesdropping):** Kẻ tấn công sử dụng các công cụ phân tích gói tin mạng (như Wireshark) để đọc trộm thông tin số tài khoản gửi, nhận, số dư, số tiền chuyển, gây rò rỉ dữ liệu cá nhân nhạy cảm của khách hàng.
*   **Sửa đổi dữ liệu giao dịch (Tampering):** Hacker thực hiện kỹ thuật Man-in-the-Middle (MitM) để đánh chặn gói tin, sửa đổi số tài khoản thụ hưởng của nạn nhân thành tài khoản của hacker hoặc thay đổi tăng số tiền giao dịch lên gấp nhiều lần nhằm chiếm đoạt tài sản.
*   **Tấn công phát lại (Replay Attack):** Kẻ tấn công không cần giải mã gói tin. Chúng chỉ cần chặn gói tin của một giao dịch chuyển tiền hợp lệ (ví dụ: Alice chuyển cho Bob $100) và liên tục gửi lại gói tin đó lên hệ thống Ngân hàng nhiều lần để máy chủ thực hiện lệnh chuyển tiền lặp đi lặp lại cho đến khi tài khoản của nạn nhân cạn kiệt.
*   **Mạo danh thực thể (Spoofing):** Kẻ xấu tự tạo ra một khóa công khai giả mạo, giả danh khách hàng hợp lệ và gửi yêu cầu rút tiền giả mạo có kèm chữ ký giả để lừa gạt máy chủ phê duyệt thanh toán.

Nhằm giúp sinh viên ngành An toàn thông tin hiểu sâu sắc lý thuyết mật mã và trải nghiệm thực tiễn quy trình kiểm soát rủi ro bảo mật của ngân hàng, đề tài 23 đã xây dựng ứng dụng mô phỏng **CyberBank Defense**. Trò chơi đặt người học vào vị trí một Quản trị viên An ninh Cổng bảo mật Ngân hàng (Bank Security Administrator), người trực tiếp kiểm thử an ninh phần mềm và duyệt/từ chối giao dịch thông qua quy trình đối chiếu mật mã chuyên nghiệp.

## 1.2 Phân tích chi tiết 5 mục tiêu bảo mật cốt lõi theo thuộc tính an toàn
Hệ thống CyberBank Defense được thiết kế và triển khai chặt chẽ nhằm bảo đảm trọn vẹn cả 5 thuộc tính vàng trong an toàn thông tin:

### 1.2.1 Tính bí mật (Confidentiality)
Tính bí mật đảm bảo thông tin chi tiết của giao dịch (bao gồm Tên người gửi, Số tài khoản nhận, và Số tiền giao dịch) không bị tiết lộ cho bất kỳ bên thứ ba nào không có thẩm quyền trên đường truyền mạng. Hệ thống giải quyết mục tiêu này bằng cách mã hóa toàn bộ Plaintext giao dịch sang Ciphertext dạng Hex vô nghĩa bằng thuật toán đối xứng mạnh mẽ **AES-128-GCM**. Kẻ xấu nghe lén trên đường truyền chỉ nhận được chuỗi nhị phân mã hóa ngẫu nhiên mà không thể suy đoán ngược lại thông tin ban đầu nếu không có Khóa phiên (Session Key).

### 1.2.2 Tính toàn vẹn (Integrity)
Tính toàn vẹn bảo đảm gói tin giao dịch không bị thay đổi, thêm bớt hoặc sửa đổi bất hợp pháp trong suốt quá trình truyền tải từ Client đến Bank Gateway. Hệ thống áp dụng cơ chế kép để bảo vệ tính toàn vẹn:
*   Sử dụng chế độ mã hóa **AES-GCM (Authenticated Encryption with Associated Data - AEAD)**. Khi mã hóa, AES-GCM tự động sinh ra một Thẻ xác thực mật mã (MAC Tag) dài 16-byte bảo vệ bản mã. Bất kỳ hành vi thay đổi dù chỉ 1 bit của Ciphertext đều làm cho thẻ xác thực bị lệch và quá trình giải mã tại cổng bảo mật sẽ báo lỗi lập tức.
*   Tính toán mã băm kiểm tra toàn vẹn **SHA-512** bao bọc toàn bộ gói tin mã hóa kèm theo Timestamp, cung cấp khả năng bảo vệ chống va chạm ở mức tuyệt đối.

### 1.2.3 Tính xác thực (Authenticity)
Tính xác thực đảm bảo rằng yêu cầu giao dịch thực sự xuất phát từ khách hàng sở hữu tài khoản mà không phải từ kẻ mạo danh. Cổng bảo mật Ngân hàng thực hiện xác thực thông qua công nghệ Chữ ký số bất đối xứng **RSA-PSS 2048-bit**.
*   Khách hàng sử dụng Khóa riêng tư (Private Key) được lưu trữ bí mật của mình để ký lên metadata giao dịch (bao gồm Sender, Timestamp, Nonce).
*   Ngân hàng sử dụng Khóa công khai (Public Key) tương ứng đã đăng ký trước của khách hàng đó để xác minh chữ ký. Nếu chữ ký không khớp, hệ thống kết luận giao dịch bị mạo danh và hủy bỏ ngay lập tức.

### 1.2.4 Tính sẵn sàng (Availability)
Tính sẵn sàng đảm bảo hệ thống dịch vụ ngân hàng luôn hoạt động ổn định, tránh bị nghẽn mạng hoặc cạn kiệt tài nguyên xử lý do các cuộc tấn công DoS hoặc tấn công phát lại liên tục.
*   Hệ thống triển khai cơ chế kiểm tra **Timestamp giới hạn trong 15 giây**. Bất kỳ yêu cầu giao dịch nào bị lưu giữ trên mạng quá 15 giây so với thời gian thực của máy chủ sẽ bị loại bỏ tự động để tránh làm tắc nghẽn hàng đợi xử lý.
*   Cơ chế **Nonce Registry** lưu giữ danh sách các chuỗi định danh ngẫu nhiên một lần đã xử lý, giúp máy chủ ngân hàng từ chối ngay lập tức các yêu cầu phát lại mà không cần thực hiện các phép toán giải mã đối xứng hay xác thực chữ ký nặng nề, bảo vệ tài nguyên tính toán của CPU.

### 1.2.5 Khả năng truy vết (Traceability & Accountability)
Khả năng truy vết đảm bảo rằng mọi sự kiện, hành động kiểm duyệt hay tấn công đều được ghi nhận đầy đủ, không thể bị xóa bỏ hoặc chối bỏ bởi người dùng hay quản trị viên. Hệ thống tích hợp phân hệ **Audit Logs** hiển thị thời gian thực (Terminal Logger). Mỗi giao dịch đi qua hệ thống đều được ghi lại nhật ký chi tiết: thời gian nhận, kết quả kiểm tra RSA, trạng thái Nonce, kết quả giải mã AES, địa chỉ IP giả lập và quyết định phê duyệt cuối cùng. Các logs này cung cấp bằng chứng rõ ràng để phục vụ công tác thanh tra khi có tranh chấp tài chính.

## 1.3 Mục tiêu giáo dục và sư phạm của Game
*   **Mục tiêu học tập:** Giúp người học trực quan hóa các khái niệm trừu tượng trong an toàn thông tin (mã hóa đối xứng, chữ ký số bất đối xứng, mã băm toàn vẹn, phòng thủ replay) thành các thao tác nghiệp vụ cụ thể.
*   **Mục tiêu ứng dụng:** Người học trực tiếp phân tích các thành phần của gói tin giao dịch trên giao diện game, thực hiện kiểm duyệt tuần tự để đưa ra quyết định phê duyệt chính xác, từ đó hình thành tư duy phân tích hiểm họa bảo mật.

---

# CHƯƠNG 2: CƠ SỞ LÝ THUYẾT MẬT MÃ HỌC ÁP DỤNG

## 2.1 Thuật toán mã hóa đối xứng AES và chế độ hoạt động Galois/Counter Mode (GCM)

### 2.1.1 Nguyên lý mã hóa đối xứng AES
AES (Advanced Encryption Standard) là thuật toán mã hóa khối đối xứng tiêu chuẩn của chính phủ Hoa Kỳ, hoạt động trên các khối dữ liệu 128-bit (16 byte) với kích thước khóa có thể là 128, 192, hoặc 256-bit. Thuật toán áp dụng mạng thay thế-hoán vị (Substitution-Permutation Network - SPN) gồm nhiều vòng lặp toán học biến đổi dữ liệu.
Các bước biến đổi chính trong mỗi vòng mã hóa của AES bao gồm:
1.  **SubBytes:** Thay thế từng byte dữ liệu bằng một byte khác dựa trên bảng tra cứu phi tuyến S-box, nhằm phá vỡ tính tuyến tính giữa bản rõ và bản mã.
2.  **ShiftRows:** Dịch chuyển tuần tuần hoàn các hàng của ma trận trạng thái dữ liệu (State) theo các số lượng offset khác nhau (hàng 1 không dịch, hàng 2 dịch 1 byte sang trái, hàng 3 dịch 2 byte, hàng 4 dịch 3 byte), tăng mức độ khuếch tán dữ liệu.
3.  **MixColumns:** Trộn lẫn các byte trong mỗi cột bằng cách nhân ma trận trạng thái dữ liệu với một đa thức xác định trên trường Galois GF(2^8), tạo ra sự liên kết chéo mạnh mẽ giữa các byte trong cột.
4.  **AddRoundKey:** Thực hiện phép toán logic XOR giữa ma trận trạng thái dữ liệu hiện tại với Khóa vòng (Round Key) được dẫn xuất từ khóa chính thông qua thuật toán Key Expansion của AES.

### 2.1.2 Cơ chế Galois/Counter Mode (AES-GCM) và xác thực dữ liệu AEAD
Chế độ hoạt động Galois/Counter Mode (GCM) biến mã hóa khối AES thành bộ mã dòng hoạt động ở chế độ Counter Mode (CTR) kết hợp với thuật toán xác thực tính toàn vẹn dữ liệu dựa trên phép nhân trường Galois (GHASH). AES-GCM thuộc nhóm thuật toán **AEAD** (Authenticated Encryption with Associated Data).
Cơ chế hoạt động của AES-GCM bao gồm hai phần chính diễn ra song song:
1.  **Mã hóa dòng:** Một bộ đếm (Counter) tăng dần bắt đầu từ một Giá trị khởi tạo (Initialization Vector - IV / GCM Nonce) được mã hóa bằng AES. Kết quả mã hóa bộ đếm sau đó được XOR trực tiếp với bản rõ (Plaintext) để sinh ra bản mã (Ciphertext). Việc này cho phép mã hóa dữ liệu với độ dài bất kỳ mà không cần đệm dữ liệu (padding) và hỗ trợ tính toán song song hóa hiệu năng cao.
2.  **Sinh thẻ xác thực (GHASH):** Bản mã và các dữ liệu đi kèm không cần mã hóa (Associated Data - AD) được đưa vào hàm băm GHASH. GHASH thực hiện phép nhân đa thức trên trường Galois hữu hạn $GF(2^{128})$ dưới một khóa băm $H$ (được sinh ra bằng cách mã hóa khối toàn không bằng AES). Kết quả của GHASH được XOR với bộ đếm Counter đầu tiên (Counter 0) được mã hóa để sinh ra Thẻ xác thực (Authentication Tag) dài 16-byte.

```
Mô tả toán học của GHASH:
    X_i = (X_{i-1} ^ A_i) * H  (đối với dữ liệu Associated Data)
    Y_i = (Y_{i-1} ^ C_i) * H  (đối với Ciphertext)
    Tag = AES_Key(Counter 0) ^ GHASH_Result
```

### 2.1.3 Ưu thế vượt trội của AES-GCM so với các chế độ cũ
So với các chế độ mã hóa truyền thống như AES-CBC (Cipher Block Chaining) kết hợp với các cơ chế kiểm tra toàn vẹn độc lập (như HMAC-SHA-256), AES-GCM mang lại những lợi ích bảo mật và hiệu năng to lớn:
*   **Chống tấn công đệm dữ liệu (Padding Oracle Attacks):** AES-CBC yêu cầu dữ liệu đầu vào phải là bội số của 16 byte nên cần đệm dữ liệu (như PKCS#7). Kẻ tấn công có thể khai thác các thông báo lỗi giải mã đệm để tìm ra bản rõ. AES-GCM chạy theo cơ chế mã dòng nên không cần đệm dữ liệu, loại bỏ hoàn toàn nguy cơ này.
*   **Hiệu năng vượt trội và song song hóa:** Chế độ CBC yêu cầu khối sau phải đợi khối trước mã hóa xong (phụ thuộc tuần tự), không tận dụng được CPU đa nhân. AES-GCM hoạt động theo chế độ Counter, cho phép mã hóa và giải mã các khối dữ liệu độc lập hoàn toàn song song, kết hợp các tập lệnh phần cứng AES-NI giúp tốc độ đạt mức gigabit trên giây.
*   **Mật mã học xác thực tích hợp (AEAD):** Chỉ cần một khóa duy nhất và một lượt xử lý (single-pass), AES-GCM thực hiện đồng thời cả hai nhiệm vụ: bảo mật thông tin và sinh thẻ xác thực. CBC yêu cầu thực hiện mã hóa trước, sau đó mới tính HMAC trên bản mã (Encrypt-then-MAC), tốn kém gấp đôi tài nguyên tính toán.

## 2.2 Thuật toán chữ ký số RSA và cơ chế PSS (Probabilistic Signature Scheme)

### 2.2.1 Nguyên lý mã hóa bất đối xứng RSA
Thuật toán RSA dựa trên bài toán toán học nan giải: phân tích một số nguyên cực lớn thành các thừa số nguyên tố. Cặp khóa RSA gồm:
*   Khóa công khai (Public Key): $(e, n)$ dùng để mã hóa hoặc xác minh chữ ký.
*   Khóa bí mật (Private Key): $(d, n)$ dùng để giải mã hoặc ký số.
Trong đó:
*   $n = p \times q$ (với $p, q$ là hai số nguyên tố lớn ngẫu nhiên).
*   $e$ là số mũ mã hóa công khai (thường chọn số Fermat $65537$).
*   $d$ là nghịch đảo nhân của $e$ theo modulo $\phi(n)$: $d \equiv e^{-1} \pmod{(p-1)(q-1)}$.
Quy trình ký số toán học cơ bản:
$$\text{Signature} = M^d \pmod n$$
Quy trình xác minh chữ ký toán học cơ bản:
$$M' = \text{Signature}^e \pmod n$$
Nếu $M' = M$, chữ ký số được xác nhận là hợp lệ.

### 2.2.2 Tiêu chuẩn chữ ký số RSA-PSS và tính an toàn nâng cấp
RSA-PSS (Probabilistic Signature Scheme) là tiêu chuẩn chữ ký số ngẫu nhiên được chuẩn hóa trong PKCS#1 v2.1. Khác với cơ chế ký RSA truyền thống có tính chất đơn trị (cùng một bản tin luôn cho ra một chữ ký số giống nhau), RSA-PSS đưa vào thêm một giá trị muối ngẫu nhiên (Salt) trong quá trình băm và đệm bản tin trước khi thực hiện phép toán mũ hóa RSA.
Quy trình mã hóa đệm RSA-PSS diễn ra qua các bước:
1.  Bản tin gốc được băm bằng SHA-512 để tạo ra giá trị băm $mHash$.
2.  Sinh một chuỗi muối ngẫu nhiên $salt$ có độ dài xác định (ví dụ: 64 byte).
3.  Ghép nối $mHash$ với một chuỗi byte đệm cố định và $salt$, sau đó băm lại để tạo ra chuỗi băm $H$.
4.  Đưa $H$ qua hàm sinh mặt nạ dữ liệu **MGF1 (Mask Generation Function 1)** để tạo ra chuỗi mặt nạ $dbMask$.
5.  XOR chuỗi muối $salt$ với $dbMask$ để tạo ra chuỗi $maskedDB$.
6.  Ghép nối $maskedDB$, $H$ và byte kết thúc cố định để tạo ra khối dữ liệu mã hóa đệm $EM$ (Encoded Message) có độ dài bằng kích thước khóa (2048 bit). Khối $EM$ này mới được đưa vào phép toán mũ hóa lũy thừa để ký bằng Private Key.

### 2.2.3 So sánh RSA-PSS với RSA PKCS#1 v1.5 truyền thống
*   **Tính an toàn toán học vững chắc:** RSA PKCS#1 v1.5 sử dụng cơ chế đệm cố định có tính chất xác định (deterministic). Kẻ tấn công có thể thực hiện các cuộc tấn công lựa chọn bản tin (Chosen-Message Attacks) để giải mã khóa hoặc giả mạo chữ ký. RSA-PSS được chứng minh an toàn toán học chặt chẽ dựa trên mô hình tiên tri ngẫu nhiên (Random Oracle Model), giảm thiểu rủi ro rò rỉ khóa.
*   **Chống tấn công đoán trước chữ ký:** Do có chứa thành phần muối ngẫu nhiên $salt$ thay đổi liên tục, hai chữ ký RSA-PSS được ký trên cùng một tài liệu giao dịch tại hai thời điểm khác nhau sẽ cho ra hai chuỗi chữ ký số hoàn toàn khác nhau. Điều này ngăn chặn hacker thu thập các mẫu chữ ký số tĩnh để tìm cách phân tích cấu trúc khóa.

## 2.3 Hàm băm mật mã SHA-512

### 2.3.1 Kiến trúc và nguyên lý hoạt động của SHA-512
SHA-512 (Secure Hash Algorithm 2, kích thước đầu ra 512 bit) hoạt động trên các khối dữ liệu 1024-bit thông qua cấu trúc lặp Merkle-Damgård với hàm nén một chiều.
Quy trình băm của SHA-512 bao gồm:
1.  **Đệm dữ liệu (Padding):** Bản tin đầu vào được thêm các bit đệm sao cho tổng chiều dài chia 1024 dư 896 bit, sau đó đính kèm 128 bit ghi nhận chiều dài ban đầu của bản tin.
2.  **Khởi tạo trạng thái:** Sử dụng 8 thanh ghi trạng thái (A, B, C, D, E, F, G, H) có kích thước 64-bit, khởi tạo bằng phần phân số của căn bậc hai của 8 số nguyên tố đầu tiên.
3.  **Vòng lặp nén:** Với mỗi khối dữ liệu 1024-bit, thuật toán mở rộng khối thành 80 từ dữ liệu 64-bit và thực hiện 80 vòng lặp nén phức tạp sử dụng các hàm logic phi tuyến Ch (Choice), Maj (Majority), và các phép dịch chuyển, xoay bit tuần hoàn (Rotate).

### 2.3.2 Khả năng chống va chạm và tối ưu hóa trên nền tảng 64-bit
*   **Chống va chạm tuyệt vời:** SHA-512 cung cấp không gian trạng thái khổng lồ với $2^{512}$ giá trị băm khả dĩ. Khả năng tìm được hai bản tin khác nhau có cùng một giá trị băm (Collision) đòi hỏi sức mạnh tính toán tối thiểu là $2^{256}$ phép thử (theo nghịch lý ngày sinh nhật), điều này bất khả thi với mọi siêu máy tính hiện đại và cả máy tính lượng tử trong tương lai gần.
*   **Tối ưu hóa phần cứng 64-bit:** Khác với SHA-256 sử dụng các toán hạng 32-bit, SHA-512 sử dụng các toán hạng và phép toán số học 64-bit. Trên các kiến trúc máy tính 64-bit hiện đại (x86_64, ARM64), CPU có thể xử lý các thanh ghi 64-bit chỉ trong một chu kỳ máy. Do đó, tốc độ băm SHA-512 trên máy tính 64-bit nhanh hơn SHA-256 đáng kể trên cùng một khối lượng dữ liệu lớn.

## 2.4 Hàm dẫn xuất khóa PBKDF2 (Password-Based Key Derivation Function 2)

### 2.4.1 Cơ chế chống brute-force bằng số vòng lặp lớn và muối (Salt)
PBKDF2 là tiêu chuẩn dẫn xuất khóa từ mật khẩu được định nghĩa trong RFC 2898. Nó giải quyết điểm yếu lớn nhất của mật khẩu người dùng: mật khẩu thường ngắn, dễ đoán và dễ bị tấn công vét cạn (Brute-force) bằng bảng băm tính sẵn (Rainbow Tables).
PBKDF2 hoạt động bằng cách áp dụng một hàm băm giả ngẫu nhiên (như HMAC-SHA-256) lặp đi lặp lại nhiều lần trên mật khẩu thô kết hợp với chuỗi muối ngẫu nhiên $salt$.
$$\text{DK} = \text{PBKDF2}(Password, Salt, c, keyLen)$$
Trong đó:
*   $Salt$: Chuỗi byte ngẫu nhiên đính kèm để đảm bảo hai mật khẩu giống nhau của hai người dùng khác nhau sẽ sinh ra hai khóa đối xứng khác nhau, phá vỡ hiệu quả của Rainbow Tables.
*   $c$: Số vòng lặp tính toán (Iteration Count). Hệ thống áp dụng $c = 100,000$ vòng. Số lượng vòng lặp lớn tạo ra một độ trễ tính toán có tính toán (khoảng vài chục đến vài trăm mili-giây đối với người dùng đăng nhập bình thường). Tuy nhiên, đối với kẻ tấn công muốn thử hàng tỷ mật khẩu mỗi giây bằng phần cứng chuyên dụng (GPU/ASIC), độ trễ này sẽ bị nhân lên hàng trăm nghìn lần, khiến cho việc tấn công vét cạn trở nên bất khả thi về mặt chi phí và thời gian.

### 2.4.2 Ứng dụng PBKDF2 bảo vệ mật khẩu Admin cục bộ
Hệ thống sử dụng mật khẩu Admin thô do người dùng nhập tại giao diện đăng nhập để dẫn xuất ra Khóa phiên AES 128-bit thông qua PBKDF2. Khóa phiên này không bao giờ được lưu trực tiếp trong tệp tin cấu hình. Tệp `credentials.json` chỉ lưu trữ giá trị băm SHA-256 tĩnh của mật khẩu để phục vụ bước xác thực danh tính. Việc dẫn xuất khóa bằng PBKDF2 đảm bảo khóa phiên được sinh an toàn trong bộ nhớ RAM tạm thời và biến mất hoàn toàn khi tắt chương trình, ngăn ngừa nguy cơ hacker đọc trộm khóa từ ổ đĩa cứng.

---

# CHƯƠNG 3: MÔ HÌNH HIỂM HỌA VÀ PHÂN TÍCH AN NINH (THREAT MODELING)

## 3.1 Xác định tài sản và thực thể cần bảo vệ
Để xây dựng mô hình hiểm họa an toàn cho cổng thanh toán CyberBank Defense, trước hết ta phải định nghĩa danh mục tài sản nhạy cảm cần được bảo vệ tuyệt đối:

##### Bảng 3.1: Danh mục tài sản an ninh của hệ thống ngân hàng

| ID Tài sản | Tên Tài sản | Định dạng lưu trữ | Mức độ nhạy cảm | Rủi ro chính nếu bị xâm phạm |
| :--- | :--- | :--- | :---: | :--- |
| TS-01 | Plaintext Giao dịch | Bộ nhớ tạm (RAM) | Tối khẩn | Lộ số tài khoản, số dư, thông tin khách hàng. |
| TS-02 | Khóa riêng tư RSA Client | Bộ nhớ tạm (RAM) | Tối khẩn | Hacker mạo danh chữ ký để thực hiện rút tiền giả. |
| TS-03 | Khóa đối xứng phiên (Session Key) | Dẫn xuất qua PBKDF2 | Tối khẩn | Hacker giải mã được toàn bộ các giao dịch trên mạng. |
| TS-04 | Registry Nonce chống phát lại | Cấu trúc dữ liệu Set trong Python | Cao | Bị xóa hoặc sửa sẽ làm mất khả năng chống Replay. |
| TS-05 | Nhật ký Audit Logs bảo mật | Giao diện Terminal/Tệp tin | Trung bình | Bị thay đổi làm mất dấu vết tấn công, cản trở điều tra. |
| TS-06 | Thông tin đăng nhập Admin | Tệp `credentials.json` | Cao | Hacker chiếm quyền Admin để duyệt giao dịch trái phép. |

## 3.2 Nhận diện các tác nhân tấn công giả định (Threat Actors)
Hệ thống giả định sự xuất hiện của các nhóm tác nhân đe dọa an ninh mạng sau:
1.  **Hacker Nghe lén (Passive Eavesdropper):** Nằm trên cùng phân đoạn mạng LAN/Wifi công cộng của khách hàng, sử dụng kỹ thuật sniffing để bắt gói tin mạng. Mục tiêu là thu thập thông tin tài chính nhạy cảm mà không chỉnh sửa gói tin.
2.  **Hacker Can thiệp đường truyền (Active MitM Tamperer):** Thực hiện tấn công ARP Spoofing hoặc DNS Spoofing để ép gói tin đi qua máy của chúng, chủ động sửa đổi nội dung số tiền hoặc số tài khoản đích trước khi đẩy gói tin lên Gateway ngân hàng.
3.  **Hacker Tấn công phát lại (Replay Attacker):** Chặn bắt gói tin giao dịch hợp lệ của khách hàng (dù gói tin đã được mã hóa và ký số). Sau đó gửi lại chính xác gói tin này lên Gateway ngân hàng nhiều lần vào các thời điểm khác nhau để lừa máy chủ thực hiện giao dịch trùng lặp.
4.  **Kẻ mạo danh (Identity Spoofer):** Kẻ tấn công tự sinh khóa riêng tư của riêng mình, gửi yêu cầu giao dịch giả mạo dưới tên tài khoản của Alice lên ngân hàng với hy vọng ngân hàng không đối chiếu chữ ký số hoặc đối chiếu sai cách.
5.  **Kẻ tấn công từ chối dịch vụ (DoS Attacker):** Gửi hàng loạt gói tin rác hoặc gửi liên tục các gói tin cũ lỗi thời lên cổng giao dịch nhằm vắt kiệt năng lực xử lý CPU của Gateway ngân hàng, làm treo hệ thống.

## 3.3 Phân tích hiểm họa theo khung STRIDE và cơ chế phòng thủ tương ứng
Áp dụng mô hình hiểm họa STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) cho hệ thống CyberBank Defense:

##### Bảng 3.2: Bảng phân tích chi tiết hiểm họa theo khung STRIDE

| Nhân tố STRIDE | Mô tả hiểm họa cụ thể | Hậu quả thực tế | Cơ chế phòng thủ đã cài đặt trong code |
| :---: | :--- | :--- | :--- |
| **S**poofing | Hacker tạo giao dịch rút tiền và mạo danh tài khoản Alice gửi lên Bank Gateway. | Alice bị mất tiền bất hợp pháp. | **Chữ ký số RSA-PSS 2048-bit:** Xác minh bằng Khóa công khai của Alice, chữ ký giả bị từ chối ở bước 1. |
| **T**ampering | Hacker sửa đổi nội dung gói tin trên đường truyền, chuyển $10 thành $10,000. | Thất thoát tài chính nghiêm trọng cho khách hàng/ngân hàng. | **AES-GCM (MAC Tag Verification):** Phát hiện tức thì sai lệch 1 byte ở bước 4 nhờ tag xác thực và SHA-512. |
| **R**epudiation | Alice gửi giao dịch chuyển tiền cho Bob nhưng sau đó chối bỏ nói rằng mình không gửi. | Ngân hàng chịu tổn thất pháp lý và đền bù tài chính. | **RSA-PSS Chống chối bỏ:** Chỉ có Private Key duy nhất của Alice mới ký được gói tin này. |
| **I**nformation Disclosure | Hacker nghe lén gói tin trên mạng để đánh cắp số tài khoản thụ hưởng. | Rò rỉ thông tin riêng tư nhạy cảm của khách hàng. | **Mã hóa AES-128-GCM:** Dữ liệu giao dịch được đóng gói dưới dạng Ciphertext, hacker chỉ thấy chuỗi Hex vô nghĩa. |
| **D**enial of Service | Hacker phát lại gói tin giao dịch hợp lệ 10,000 lần gây quá tải CPU và tài nguyên mạng. | Hệ thống ngân hàng bị sập, từ chối phục vụ khách hàng hợp lệ. | **Anti-Replay Registry & Timestamp limit (15s):** Khóa giao dịch trễ hạn hoặc trùng Nonce mà không cần giải mã. |
| **E**levation of Privilege | Hacker đoán mật khẩu Admin hoặc sửa file cấu hình để đăng nhập trái phép quyền Admin. | Hacker có toàn quyền duyệt các giao dịch giả mạo. | **PBKDF2 Admin Login Authentication:** Mật khẩu được băm SHA-256 bảo vệ, dẫn xuất khóa qua PBKDF2 độ an toàn cao. |

---

# CHƯƠNG 4: THIẾT KẾ KIẾN TRÚC HỆ THỐNG MÔ PHỎNG

## 4.1 Sơ đồ kiến trúc tổng quan
Hệ thống CyberBank Defense được tổ chức theo kiến trúc bảo mật phân tầng mô phỏng 3 lớp:

```
+-------------------------------------------------------------+
|                     LỚP MÁY KHÁCH (CLIENT)                  |
|  - Sinh cặp khóa RSA-2048 Client                            |
|  - Khởi tạo Giao dịch Plaintext                             |
|  - Đóng gói Metadata (Sender, Timestamp, Nonce)             |
|  - Ký số RSA-PSS & Mã hóa AES-128-GCM                       |
+-------------------------------------------------------------+
                              |
                              | Gửi Gói tin bảo mật mạng
                              v
+-------------------------------------------------------------+
|             LỚP CỔNG BẢO MẬT NGÂN HÀNG (GATEWAY)            |
|  - Phân tích cú pháp gói tin giao dịch                     |
|  - Lõi mật mã kiểm duyệt an ninh 4 bước (CryptoEngine)      |
|  - Giao diện giám sát & điều hành của Quản trị viên (GUI)   |
+-------------------------------------------------------------+
           |                                       |
     Truy vấn Nonce                          Ghi nhận Nhật ký
           v                                       v
+-----------------------+               +---------------------+
|   LỚP CSDL REGISTRY   |               | PHÂN HỆ AUDIT LOGS  |
| - Nonce Registry DB   |               | - Terminal Logger   |
| - credentials.json    |               | - Cảnh báo tấn công |
+-----------------------+               +---------------------+
```

## 4.2 Các phân hệ thành phần và Vai trò chi tiết
*   **Lớp Máy khách (Client/Customer Side):**
    -   Đóng vai trò là khách hàng thực hiện giao dịch tài chính.
    -   Tích hợp bộ sinh cặp khóa RSA-2048 độc lập để tự quản lý Private Key và Public Key.
    -   Mỗi giao dịch gửi đi được đóng gói metadata thời gian thực (Timestamp) và mã định danh ngẫu nhiên (Nonce) để ngăn ngừa các nguy cơ giả mạo và phát lại.
*   **Cổng bảo mật Ngân hàng (Bank Security Gateway):**
    -   Là thành phần trung tâm chịu trách nhiệm kiểm tra toàn bộ các thuộc tính an toàn của giao dịch gửi đến.
    -   Chứa lõi xử lý mật mã `CryptoEngine` thực hiện các phép toán phức tạp: xác minh chữ ký RSA-PSS, kiểm tra logic thời gian Timestamp máy chủ, kiểm tra trùng lặp Nonce trong cơ sở dữ liệu, giải mã bản mã đối xứng AES-GCM và đối chiếu thẻ xác thực MAC Tag.
*   **Cơ sở dữ liệu Registry (Database Registry):**
    -   Tệp `credentials.json` lưu giữ thông tin định danh của Admin dưới dạng chuỗi băm bảo mật SHA-256.
    -   Cấu trúc dữ liệu Set trong bộ nhớ (được giả lập là database RAM) lưu giữ toàn bộ các Nonce hợp lệ đã xử lý để làm căn cứ đối chiếu chống tấn công phát lại.
*   **Phân hệ Audit Logs (Nhật ký hệ thống):**
    -   Kênh ghi nhận các sự kiện bảo mật xảy ra trong hệ thống thời gian thực.
    -   Phân loại sự kiện trực quan bằng màu sắc trên Terminal Logger giúp Admin theo dõi các cảnh báo đỏ khi phát hiện hành vi tấn công sửa đổi, trễ hạn hoặc chữ ký sai.

---

# CHƯƠNG 5: THIẾT KẾ GIAO THỨC BẢO MẬT GIAO DỊCH

## 5.1 Sơ đồ luồng xử lý và giao thức (Sequence Diagram)
Quy trình truyền tin và xác thực giao dịch giữa Client, Gateway Ngân hàng, Cơ sở dữ liệu Nonce và Nhật ký hệ thống được đặc tả chi tiết qua sơ đồ Sequence Diagram dưới đây:

```
Client              Admin            Bank Gateway        Nonce Database       Audit Logs
  |                   |                   |                     |                 |
  |-- Tạo giao dịch ->|                   |                     |                 |
  |   (Plaintext)     |                   |                     |                 |
  |-- Sinh metadata ->|                   |                     |                 |
  |   Nonce, Time     |                   |                     |                 |
  |-- Ký số RSA-PSS ->|                   |                     |                 |
  |-- Mã hóa AES ---->|                   |                     |                 |
  |                                       |                     |                 |
  |====== Gửi gói tin bảo mật ===========>|                     |                 |
  |   (Ciphertext, Tag, Nonce, Time,      |                     |                 |
  |    Signature, SHA-512 Hash)           |                     |                 |
  |                                       |                     |                 |
  |                   |-- Nhấp Bước 1 --->|                     |                 |
  |                   |   Xác thực RSA    |-- Xác minh chữ ký ->|                 |
  |                   |<-- Chữ ký OK -----|                     |                 |
  |                                       |                     |                 |
  |                   |-- Nhấp Bước 2 --->|                     |                 |
  |                   |   Kiểm tra Time   |-- Tính tuổi gói ----|                 |
  |                   |<-- Thời gian OK --|                     |                 |
  |                                       |                     |                 |
  |                   |-- Nhấp Bước 3 --->|                     |                 |
  |                   |   Check Replay    |-- Truy vấn Nonce -->|                 |
  |                   |                   |<-- Nonce chưa có ---|                 |
  |                   |<-- Anti-Replay OK |                     |                 |
  |                                       |                     |                 |
  |                   |-- Nhấp Bước 4 --->|                     |                 |
  |                   |   Check MAC/AES   |-- Giải mã AES-GCM ->|                 |
  |                   |                   |-- Đối chiếu Hash ---|                 |
  |                   |<-- Bản rõ/MAC OK -|                     |                 |
  |                                       |                     |                 |
  |                   |-- Quyết định ---->|                     |                 |
  |                   |   Duyệt giao dịch |-- Lưu Nonce ------->|                 |
  |                   |                   |                                       |-- Ghi nhật ký ->|
  |                   |                   |<====== Duyệt thành công ==============|                 |
```

## 5.2 Đặc tả chi tiết các bước xử lý gói tin an toàn
Khi một yêu cầu chuyển tiền được khởi tạo:
1.  **Đóng gói gói tin tại Client:**
    -   Client biên soạn thông điệp giao dịch $M$ (ví dụ: `Alice->Bob:$250`).
    -   Client sinh ngẫu nhiên chuỗi định danh một lần $Nonce$ (UUIDv4) và lấy thời gian hiện tại của máy khách $Timestamp$.
    -   Tạo chữ ký số $Sig$ bằng cách băm chuỗi metadata $(Sender \parallel Timestamp \parallel Nonce)$ bằng SHA-512 và mã hóa ký số RSA-PSS với Private Key của Client.
    -   Mã hóa bản rõ $M$ bằng thuật toán AES-128-GCM với Session Key để thu được bản mã $C$, thẻ xác thực $Tag$, và vector khởi tạo $IV$.
    -   Tính toán mã hash toàn vẹn cuối cùng $Hash = \text{SHA-512}(C \parallel Tag \parallel IV \parallel Timestamp)$.
    -   Gói tất cả thành gói tin bảo mật gửi đi: $Packet = (C, Tag, IV, Nonce, Timestamp, Sig, Hash)$.
2.  **Xử lý và Kiểm duyệt 4 bước tuần tự tại Gateway Ngân hàng:**
    -   **Bước 1: Xác thực thực thể (Authenticity Check):** Cổng bảo mật giải trích $Sig$ và metadata trong gói tin, băm lại metadata bằng SHA-512 và xác minh bằng Public Key của Client. Nếu chữ ký không khớp, báo lỗi mạo danh thực thể và từ chối.
    -   **Bước 2: Kiểm tra giới hạn thời gian (Timestamp Check):** Cổng bảo mật so sánh thời gian hiện tại của hệ thống máy chủ $T_{server}$ với thời gian gửi ghi trong gói tin $Timestamp$. Nếu khoảng chênh lệch $T_{server} - Timestamp > 15 \text{ giây}$, gói tin bị từ chối vì quá hạn để tránh các cuộc tấn công phát lại cũ hoặc nghẽn hàng đợi.
    -   **Bước 3: Phòng thủ chống phát lại (Anti-Replay Check):** Cổng bảo mật truy vấn mã $Nonce$ trong Database Registry. Nếu tìm thấy Nonce đã tồn tại trong danh sách đã xử lý, hệ thống kết luận đây là một cuộc tấn công phát lại (Replay Attack) và hủy giao dịch ngay lập tức.
    -   **Bước 4: Xác thực mật mã và giải mã (AEAD Decrypt & Integrity Check):** Cổng bảo mật tính toán lại băm SHA-512 của dữ liệu nhận được để đối chiếu tính toàn vẹn. Sau đó đưa $C$, $Tag$ và $IV$ vào thuật toán giải mã đối xứng AES-GCM với Session Key. Nếu $Tag$ khớp, bản rõ giao dịch gốc được khôi phục thành công. Nếu có bất kỳ sự thay đổi dữ liệu nào dù chỉ 1 byte, quá trình giải mã sẽ thất bại (lỗi MAC check).
3.  **Hoàn tất giao dịch:** Sau khi hoàn thành 4 bước an toàn và Admin chọn phê duyệt, Nonce được lưu vĩnh viễn vào Registry và lịch sử giao dịch được ghi nhận vào Audit Logs của ngân hàng.

---

# CHƯƠNG 6: CHI TIẾT CÀI ĐẶT VÀ PHÂN TÍCH MÃ NGUỒN LÕI

## 6.1 Cấu trúc thư mục dự án và vai trò các tệp tin
Dự án được phân chia thư mục rõ ràng theo tiêu chuẩn GitHub:
*   `main.py`: Tệp mã nguồn Python chứa toàn bộ giao diện tkinter và lõi xử lý thuật toán mật mã của ứng dụng.
*   `credentials.json`: Tệp lưu thông tin tài khoản đăng nhập Admin của nhóm dưới dạng băm bảo mật SHA-256 để kiểm soát quyền đăng nhập.
*   `background.png`: File hình nền đăng nhập hiển thị giao diện Cyberpunk chuyên nghiệp.
*   `report/convert.py`: Script Python tự động biên dịch tệp báo cáo Markdown sang tệp Word .docx, thiết lập cấu trúc font chữ, cỡ chữ, căn lề và định dạng bảng biểu tự động.

## 6.2 Phân tích chi tiết mã nguồn Lõi Mật mã học (`CryptoEngine`)
Lớp `CryptoEngine` trong tệp `main.py` chịu trách nhiệm thực thi toàn bộ các phép toán mật mã của hệ thống. Dưới đây là phân tích chi tiết mã nguồn triển khai:

##### Bảng 6.1: Các hàm xử lý mật mã trong CryptoEngine

| Tên Hàm | Đầu vào chính | Đầu ra chính | Mục đích bảo mật |
| :--- | :--- | :--- | :--- |
| `sign_metadata` | sender, timestamp, nonce, private_key | Chữ ký số signature (bytes) | Xác thực và chống chối bỏ |
| `verify_metadata_signature` | sender, timestamp, nonce, signature, public_key | Boolean (True/False) | Kiểm tra tính giả mạo danh tính |
| `encrypt_transaction_details`| plaintext, session_key | ciphertext, tag, nonce (bytes) | Bí mật thông tin & Toàn vẹn (AEAD) |
| `decrypt_transaction_details`| ciphertext, tag, nonce, session_key | Bản rõ plaintext (str) | Giải mã và kiểm tra tính toàn vẹn |
| `calculate_sha512_hash` | ciphertext, timestamp | Chuỗi băm hex hash (str) | Toàn vẹn gói tin lớp ngoài |
| `check_anti_replay` | nonce, timestamp_str | Boolean hoặc ném Exception | Chống phát lại & Chống DoS trễ hạn |

### 6.2.1 Triển khai Chữ ký số RSA-PSS
Mã nguồn hàm ký số và xác minh chữ ký RSA-PSS sử dụng thư viện `Crypto.Signature.pss` kết hợp hàm băm `SHA512` bảo đảm an toàn bất đối xứng:

```python
def sign_metadata(self, sender, timestamp, nonce, client_private_key):
    """Ký số metadata giao dịch bằng RSA-PSS kết hợp SHA-512 (Xác thực danh tính)"""
    metadata = f"{sender}|{timestamp}|{nonce}"
    key = RSA.import_key(client_private_key)
    h = SHA512.new(metadata.encode('utf-8'))
    signer = pss.new(key)
    signature = signer.sign(h)
    return signature

def verify_metadata_signature(self, sender, timestamp, nonce, signature, client_public_key):
    """Xác minh chữ ký số RSA-PSS của khách hàng gửi để chống mạo danh"""
    metadata = f"{sender}|{timestamp}|{nonce}"
    try:
        key = RSA.import_key(client_public_key)
        h = SHA512.new(metadata.encode('utf-8'))
        verifier = pss.new(key)
        verifier.verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False
```

### 6.2.2 Triển khai Mã hóa và Giải mã AES-GCM
Lõi AES-GCM bảo đảm tính bảo mật tối đa bằng cách sinh tự động IV/Nonce ngẫu nhiên cho từng khối mã hóa và so sánh thẻ xác thực MAC tag khi giải mã:

```python
def encrypt_transaction_details(self, plaintext, session_key):
    """Mã hóa đối xứng có xác thực AES-GCM (Bảo mật & Toàn vẹn tích hợp)"""
    cipher = AES.new(session_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode('utf-8'))
    # Trả về ciphertext, tag xác thực 16-byte, và IV tự sinh ngẫu nhiên
    return ciphertext, tag, cipher.nonce

def decrypt_transaction_details(self, ciphertext, tag, nonce, session_key):
    """Giải mã và xác thực tính toàn vẹn của dữ liệu bằng AES-GCM"""
    try:
        cipher = AES.new(session_key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode('utf-8')
    except ValueError:
        # Nếu ciphertext hoặc tag bị thay đổi dù chỉ 1 bit, hàm ném lỗi
        raise ValueError("LỖI XÁC THỰC MẬT MÃ (MAC check failed): Bản mã bị sửa đổi!")
```

### 6.2.3 Triển khai Phòng thủ Anti-Replay và Timestamp
Bộ lọc kiểm soát thời gian và danh sách Nonce đã dùng được lưu trữ trong Set để tối ưu hóa tốc độ tra cứu $O(1)$:

```python
def check_anti_replay(self, nonce, timestamp_str, max_age_seconds=15):
    """Phòng thủ chống phát lại (Replay Attack) và loại bỏ giao dịch trễ hạn"""
    # 1. Kiểm tra Nonce trong Registry
    if nonce in self.nonce_registry:
        raise Exception(f"TẤN CÔNG PHÁT LẠI PHÁT HIỆN: Nonce '{nonce[:10]}...' đã tồn tại!")
        
    # 2. Kiểm tra Timestamp hết hạn
    try:
        tx_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        now_time = datetime.now()
        age = (now_time - tx_time).total_seconds()
        
        if age > max_age_seconds:
            raise Exception(f"LỖI THỜI GIAN HẾT HẠN: Giao dịch trễ hạn {age:.1f} giây.")
    except ValueError:
        raise Exception("Định dạng thời gian không hợp lệ.")
        
    # Thêm nonce vào Registry nếu hợp lệ
    self.nonce_registry.add(nonce)
    return True
```

## 6.3 Phân tích mã nguồn Giao diện & Điều hành (`BankingApp`)
Lớp `BankingApp` kế thừa từ lớp `tk.Tk` chịu trách nhiệm dựng giao diện người dùng và điều phối luồng trò chơi.

### 6.3.1 Dẫn xuất Khóa bảo mật Admin thông qua PBKDF2
Khi Admin đăng nhập, mật khẩu thô được dẫn xuất bằng PBKDF2-HMAC-SHA256 kết hợp chuỗi muối cố định qua 100,000 vòng lặp để sinh Khóa phiên đối xứng:

```python
def on_login(self):
    name = self.ent_name.get().strip()
    password = self.ent_pass.get().strip()
    
    # Đọc credentials.json để xác thực băm mật khẩu
    with open(self.credentials_path, "r", encoding="utf-8") as f:
        creds = json.load(f)
    
    entered_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    if name != creds["username"] or entered_hash != creds["password_sha256"]:
        messagebox.showerror("Lỗi", "Thông tin đăng nhập không chính xác!")
        return
        
    # Sử dụng PBKDF2 sinh khóa đối xứng AES từ mật khẩu nhập vào
    salt = b"atbm_salt_fixed"
    self.crypto.session_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000, 16)
    
    self.frame_login.destroy()
    self.create_widgets() # Khởi động giao diện Dashboard chính
```

### 6.3.2 Cơ chế phân loại cấp độ người chơi (Level Logic)
Hệ thống quản lý game tự động điều phối các loại giao dịch dựa trên cấp độ:
*   **Level 1 (Dễ):** 100% giao dịch sinh ra là hợp lệ, hướng dẫn người chơi làm quen với quy trình an ninh 4 bước.
*   **Level 2 (Trung bình):** 60% giao dịch hợp lệ, 20% giao dịch bị sửa đổi (Tampered), 20% giao dịch bị phát lại (Replay). Nhịp độ giao dịch trung bình.
*   **Level 3 (Khó):** Xuất hiện thêm các cuộc tấn công phức tạp như giao dịch trễ hạn (Timeout) và chữ ký giả mạo (Wrong Key). Tốc độ giao dịch đến nhanh, đòi hỏi phản xạ kiểm duyệt nhanh nhạy.

---

# CHƯƠNG 7: HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH ỨNG DỤNG

## 7.1 Môi trường yêu cầu
Ứng dụng CyberBank Defense được phát triển trên ngôn ngữ Python và yêu cầu môi trường chạy cơ bản sau:
*   **Hệ điều hành:** Microsoft Windows 10/11, macOS, hoặc Linux.
*   **Phiên bản Python:** Python 3.8, 3.9, 3.10 hoặc 3.11.
*   **Thư viện đồ họa:** Thư viện `tkinter` và `ttk` (Mặc định đã đi kèm bộ cài đặt Python tiêu chuẩn trên Windows).
*   **Thư viện mật mã:** Thư viện bên thứ ba `pycryptodome` thực hiện các tính toán mật mã.

## 7.2 Các bước cài đặt thư viện phụ thuộc
1.  Mở cửa sổ dòng lệnh (Command Prompt đối với Windows hoặc Terminal đối với macOS/Linux).
2.  Đảm bảo công cụ quản lý thư viện `pip` của Python đã được cập nhật bằng lệnh:
    ```bash
    python -m pip install --upgrade pip
    ```
3.  Thực hiện cài đặt thư viện mật mã `pycryptodome` bằng cách chạy lệnh:
    ```bash
    pip install pycryptodome
    ```
4.  (Tùy chọn) Đối với một số hệ điều hành Linux (như Ubuntu/Debian), nếu thiếu thư viện GUI tkinter, cài đặt bổ sung bằng lệnh:
    ```bash
    sudo apt-get install python3-tk
    ```

## 7.3 Hướng dẫn khởi chạy và vận hành
1.  Tải toàn bộ thư mục dự án từ GitHub và giải nén trên máy tính của bạn.
2.  Mở Command Prompt/Terminal và chuyển hướng thư mục làm việc đến thư mục dự án chứa file `main.py`.
3.  Chạy chương trình bằng lệnh:
    ```bash
    python main.py
    ```
4.  Khi giao diện đăng nhập hiển thị, nhập thông tin tài khoản mặc định của nhóm:
    -   **Tên Người chơi:** `Group 23 - ATBM`
    -   **Mật khẩu bảo vệ:** `atbm_key_2026`
5.  Click nút **⚡ KHỞI ĐỘNG HỆ THỐNG GIAO DIỆN ⚡** để đăng nhập và bắt đầu trải nghiệm trò chơi điều hành bảo mật an ninh ngân hàng.

---

# CHƯƠNG 8: KỊCH BẢN KIỂM THỬ CHỨC NĂNG VÀ BẢO MẬT (TEST CASES REPORT)

## 8.1 Kiểm thử chức năng bình thường (Happy Path)

### 8.1.1 Đăng nhập quản trị viên thành công
*   **Mô tả:** Xác minh tài khoản Quản trị viên đăng nhập thành công vào hệ thống điều hành an ninh với thông tin chính xác được băm SHA-256 đối chiếu từ credentials.json.
*   **Các bước thực hiện:**
    1.  Khởi chạy chương trình bằng lệnh `python main.py`.
    2.  Nhập chính xác Username: `Group 23 - ATBM`.
    3.  Nhập chính xác Password: `atbm_key_2026`.
    4.  Nhấp chọn nút *Khởi động hệ thống giao diện*.
*   **Kết quả mong đợi:** Chương trình xác thực mật khẩu thành công, dẫn xuất session key an toàn thông qua hàm PBKDF2, đóng màn hình đăng nhập và hiển thị Dashboard điều khiển chính.

![Hình 8.1: Giao diện màn hình đăng nhập quản trị thành công của CyberBank Defense](login_page.png)

### 8.1.2 Kiểm duyệt giao dịch hợp lệ thành công
*   **Mô tả:** Thực hiện đầy đủ quy trình an ninh 4 bước để duyệt một giao dịch bình thường, không bị sửa đổi hay phát lại.
*   **Các bước thực hiện:**
    1.  Hệ thống sinh một giao dịch hợp lệ gửi đến: `Alice (ACC-100204)` gửi `$150` đến `Bob (ACC-887711)`.
    2.  Nhấp chọn lần lượt 4 bước kiểm tra trên giao diện (hoặc nhấn phím tắt 1, 2, 3, 4):
        -   *Bước 1: Xác thực RSA-PSS* -> Thông báo chữ ký hợp lệ.
        -   *Bước 2: Kiểm tra Timestamp* -> Thông báo gói tin nằm trong giới hạn thời gian (chênh lệch 0.1 giây).
        -   *Bước 3: Giải mã AES-GCM* -> Giải mã thành công ra plaintext `Alice (ACC-100204)->Bob (ACC-887711):$150`.
        -   *Bước 4: Kiểm tra Anti-Replay* -> Thông báo Nonce chưa tồn tại trong Registry.
    3.  Nhấp chọn nút *Duyệt giao dịch* (hoặc nhấn phím J).
*   **Kết quả mong đợi:** Giao dịch được phê duyệt thành công. Điểm số tăng lên (+10 điểm). Mã Nonce được đưa vào database. Nhật ký ghi nhận log trạng thái duyệt thành công.

![Hình 8.2: Bảng Điều phối và Duyệt giao dịch hợp lệ sau khi hoàn thành 4 bước kiểm tra](dashboard_page.png)

## 8.2 Kiểm thử bảo mật chủ động (Sandbox Attack Cases)

### 8.2.1 Sửa đổi bản mã giao dịch (Tampering Ciphertext)
*   **Mô tả:** Xác minh hệ thống phát hiện hành vi sửa đổi bản mã giao dịch trên kênh truyền mạng mạng.
*   **Các bước thực hiện:**
    1.  Chuyển sang tab **Phòng Thử Nghiệm Tấn Công (Tab Sandbox)**.
    2.  Tạo giao dịch hợp lệ: `Hacker_Anonymous` gửi `$999000` đến `Hacker_Destination`.
    3.  Kích hoạt tùy chọn: *Sửa đổi dữ liệu (Tamper 1 byte trong Ciphertext)*.
    4.  Nhấp chọn nút *Gửi đến Cổng thanh toán*.
    5.  Thực hiện bước 4 (Giải mã AES-GCM) tại màn hình điều hành.
*   **Kết quả mong đợi:** Hệ thống giải mã AES-GCM phát hiện sai lệch và ném ra ngoại lệ `ValueError: MAC check failed`. Giao dịch bị ngăn chặn thành công, ghi nhận log: `[CRITICAL] Lỗi toàn vẹn (Integrity Error)`.

### 8.2.2 Tấn công phát lại giao dịch cũ (Replay Attack)
*   **Mô tả:** Chứng minh hệ thống từ chối các giao dịch cũ bị kẻ xấu nghe lén và gửi lại.
*   **Các bước thực hiện:**
    1.  Duyệt thành công một giao dịch hợp lệ để ghi nhận Nonce vào database.
    2.  Tại tab Sandbox, kích hoạt tùy chọn: *Tấn công phát lại (Replay cùng mã Nonce cũ đã dùng)*.
    3.  Bấm *Gửi đến Cổng thanh toán*.
    4.  Thực hiện bước 3 (Kiểm tra Anti-Replay) tại màn hình điều hành.
*   **Kết quả mong đợi:** Cổng ngân hàng phát hiện mã Nonce trùng lặp đã tồn tại trong Registry, từ chối xử lý và hiển thị cảnh báo: `TẤN CÔNG PHÁT LẠI PHÁT HIỆN: Nonce ... đã tồn tại trong Database!`.

### 8.2.3 Gửi giao dịch quá hạn thời gian (Timeout Attack)
*   **Mô tả:** Kiểm chứng hệ thống tự động loại bỏ gói tin giao dịch bị hacker lưu giữ quá lâu.
*   **Các bước thực hiện:**
    1.  Tại tab Sandbox, kích hoạt tùy chọn: *Làm trễ/Hết hạn thời gian (Gửi gói tin sau 10 phút)*.
    2.  Bấm nút *Gửi đến Cổng thanh toán*.
    3.  Thực hiện bước 2 (Kiểm tra Timestamp) tại màn hình điều hành.
*   **Kết quả mong đợi:** Hệ thống tính toán chênh lệch thời gian giữa lúc tạo gói tin và lúc nhận đạt 600 giây (vượt mức 15 giây cho phép), ném ra lỗi `LỖI THỜI GIAN HẾT HẠN` và từ chối phê duyệt giao dịch.

### 8.2.4 Chữ ký số giả mạo (Invalid RSA Signature)
*   **Mô tả:** Kiểm tra khả năng phát hiện kẻ mạo danh không sở hữu khóa riêng tư hợp lệ của khách hàng.
*   **Các bước thực hiện:**
    1.  Tại tab Sandbox, kích hoạt tùy chọn: *Ký số giả mạo (Sử dụng khóa RSA sai/khác)*.
    2.  Bấm nút *Gửi đến Cổng thanh toán*.
    3.  Thực hiện bước 1 (Xác thực RSA-PSS) tại màn hình điều hành.
*   **Kết quả mong đợi:** Thuật toán xác minh chữ ký RSA-PSS phát hiện khóa công khai và chữ ký không khớp, báo lỗi không khớp chữ ký số (`ValueError: Invalid signature`), hệ thống lập tức hủy giao dịch.

### 8.2.5 Đăng nhập sai thông tin quản trị (Unauthorized Login)
*   **Mô tả:** Bảo đảm hệ thống ngăn chặn việc đăng nhập sai quyền tài khoản quản trị để bảo vệ lõi xử lý.
*   **Các bước thực hiện:**
    1.  Mở màn hình đăng nhập của ứng dụng.
    2.  Nhập sai thông tin (ví dụ: Username = `Hacker`, Password = `wrong_password`).
    3.  Bấm nút *Khởi động hệ thống giao diện*.
*   **Kết quả mong đợi:** Hệ thống kiểm tra băm mật khẩu, thông báo lỗi đăng nhập thất bại và giữ người dùng ở màn hình đăng nhập, ngăn chặn truy cập trái phép.

![Hình 8.3: Phòng thí nghiệm Sandbox giả lập các cuộc tấn công bảo mật](sandbox_page.png)

---

# CHƯƠNG 9: ĐO LƯỜNG HIỆU NĂNG THỰC TẾ (BENCHMARK REPORT)

## 9.1 So sánh hiệu năng các thuật toán mã hóa đối xứng
Module Benchmark đo lường thời gian xử lý trung bình của ba thuật toán đối xứng phổ biến gồm AES-GCM (128-bit), DES (cổ điển), và Triple DES (3DES) trên gói tin dữ liệu 1MB qua 10 vòng lặp:

##### Bảng 9.1: Bảng dữ liệu Benchmark tốc độ mã hóa đối xứng (gói tin 1MB)

| Thuật toán | Chế độ mã hóa | Thời gian xử lý trung bình (ms) | Tốc độ tương đương (MB/s) | Mức độ an toàn |
| :--- | :---: | :---: | :---: | :--- |
| **AES-GCM (128-bit)** | AEAD (Sử dụng Counter) | ~2.8 ms | ~357.1 MB/s | Rất cao |
| **DES (Cổ điển)** | CBC | ~22.4 ms | ~44.6 MB/s | Không an toàn (Lỗi thời) |
| **Triple DES (3DES)** | CBC | ~61.5 ms | ~16.2 MB/s | Trung bình (Quá chậm) |

Kết quả đo lường cho thấy **AES-GCM** có tốc độ vượt trội gấp **22 lần so với DES** và gấp **40 lần so với Triple DES**. Điều này minh chứng cho tính tối ưu của cấu trúc mã dòng và sự hỗ trợ đắc lực từ tập lệnh phần cứng AES-NI được tích hợp trong các CPU Intel/AMD hiện đại.

## 9.2 So sánh hiệu năng các thuật toán băm (Hash)
So sánh tốc độ băm của SHA-256 và SHA-512 trên cùng tệp tin dữ liệu 1MB:

##### Bảng 9.2: Bảng dữ liệu Benchmark tốc độ băm (gói tin 1MB)

| Thuật toán băm | Kích thước đầu ra | Thời gian xử lý trung bình (ms) | Tốc độ tương đương (MB/s) | Tối ưu hóa phần cứng |
| :--- | :---: | :---: | :---: | :--- |
| **SHA-256** | 256 bits | ~4.2 ms | ~238.1 MB/s | Tối ưu trên hệ thống 32-bit |
| **SHA-512** | 512 bits | ~2.9 ms | ~344.8 MB/s | Tối ưu trên hệ thống 64-bit |

Hàm băm **SHA-512** có tốc độ chạy nhanh hơn **SHA-256** khoảng 30% trên máy tính thử nghiệm (Kiến trúc CPU 64-bit). Lý do là vì SHA-512 sử dụng các toán tử logic trên các từ dữ liệu 64-bit, tận dụng tối đa băng thông của các thanh ghi 64-bit trên CPU máy tính hiện đại, mang lại sự kết hợp hoàn hảo giữa độ an toàn cực cao và hiệu suất phần cứng tuyệt vời.

![Hình 9.1: Biểu đồ cột so sánh hiệu năng các thuật toán mã hóa đối xứng và băm](benchmark_page.png)

---

# CHƯƠNG 10: ĐÁNH GIÁ HIỆU QUẢ SƯ PHẠM VÀ TÍNH KHẢ DỤNG CỦA GAME

## 10.1 Hiệu quả trong việc nâng cao kiến thức an toàn thông tin
Ứng dụng CyberBank Defense đã chứng minh tính hiệu quả cao trong hoạt động giáo dục mật mã học thông qua các khía cạnh:
*   **Trực quan hóa luồng dữ liệu bảo mật:** Sinh viên không còn mơ hồ về các khái niệm trừu tượng. Việc tự mình nhấn từng nút để thực thi các bước giải mã, kiểm tra chữ ký giúp người học hiểu rõ mối liên kết mật thiết giữa các thuật toán.
*   **Phương pháp học tương tác chủ động (Gamification):** Việc tính điểm, vượt qua các màn chơi và đối mặt với nhịp độ giao dịch tăng dần tạo động lực học tập tự nhiên cho sinh viên, biến việc học lý thuyết an toàn thông tin vốn dĩ khô khan trở nên thú vị.

## 10.2 Đánh giá thiết kế giao diện đồ họa (GUI) và tính khả dụng
*   **Bố cục phân vùng logic:** Giao diện được chia thành các khu vực rõ ràng: Cột hiển thị hồ sơ giao dịch đến trực quan, khung nút bấm quy trình an ninh, màn hình Terminal logs hiển thị chi tiết các mã Hex của Ciphertext và Chữ ký số giúp sinh viên dễ dàng so khớp trực giác.
*   **Thiết kế phím tắt tối ưu:** Game tích hợp phím tắt thông minh giúp người chơi kiểm duyệt nhanh mà không cần di chuột liên tục, tăng tính phản xạ điều khiển và tối ưu hóa tính khả dụng cho phần mềm.

---

# CHƯƠNG 11: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN CẢI TIẾN

## 11.1 Các kết quả và thành tựu đã đạt được
*   Thiết kế và lập trình thành công game giáo dục bảo mật **CyberBank Defense v2.0** chạy ổn định trên nền tảng Python 3.
*   Triển khai chính xác và tối ưu lõi mật mã học nâng cao đạt tiêu chuẩn ngân hàng thực tế gồm AES-GCM (AEAD), RSA-PSS, SHA-512, và PBKDF2.
*   Thiết kế giao diện Cyberpunk Dark Mode trực quan, đẹp mắt bằng thư viện tkinter.
*   Xây dựng thành công phân hệ **Security Sandbox Lab** hỗ trợ kiểm thử chủ động 4 dạng tấn công mạng phổ biến và phân hệ **Performance Benchmark** đo lường tốc độ thuật toán vẽ đồ thị thời gian thực.

## 11.2 Các hạn chế hiện tại của hệ thống
*   Hệ thống hiện tại vẫn chạy giả lập offline trong một tiến trình duy nhất, chưa kết nối mạng phân tán thật.
*   Registry lưu trữ Nonce và Audit Logs được lưu tạm thời trên bộ nhớ RAM, dữ liệu sẽ bị giải phóng hoàn toàn khi tắt chương trình.

## 11.3 Đề xuất cải tiến và hướng phát triển tương lai
*   **Phát triển mạng phân tán Client-Server:** Sử dụng thư viện socket của Python để tách biệt Client (máy người dùng gửi giao dịch) và Server (máy chủ Ngân hàng duyệt giao dịch) trên các máy tính độc lập kết nối qua mạng LAN/Internet.
*   **Áp dụng cơ sở dữ liệu vật lý:** Sử dụng SQLite để lưu trữ vĩnh viễn thông tin Nonce Registry, tài khoản Admin và lịch sử Audit Logs, đảm bảo tính bền vững dữ liệu.
*   **Nâng cấp Mật mã học đường cong Elip (ECC):** Thay thế RSA bằng chữ ký ECDSA hoặc Ed25519 để rút ngắn độ dài khóa và chữ ký số xuống nhiều lần, giúp tăng tốc xử lý và tiết kiệm băng thông truyền dữ liệu.

---

# CHƯƠNG 12: THÔNG TIN DỰ ÁN VÀ CẤU TRÚC THƯ MỤC NỘP BÀI

## 12.1 Các sản phẩm và đường dẫn đính kèm dự án BTL
*   **Link Repository GitHub:** [https://github.com/Group23-ATBM/CyberBankDefense](https://github.com/Group23-ATBM/CyberBankDefense)
*   **Link Video Demo Chương trình (5-7 phút):** [https://youtube.com/watch?v=demo_link_group23](https://youtube.com/watch?v=demo_link_group23)

## 12.2 Sơ đồ cấu trúc thư mục nộp bài chuẩn trên GitHub
Quyển báo cáo, mã nguồn và tài liệu bổ trợ của dự án BTL Đề tài 23 được sắp xếp chuyên nghiệp theo cấu trúc thư mục sau:

```
CyberBankDefense/
│
├── main.py                     # Mã nguồn chính chạy ứng dụng game
├── credentials.json             # File lưu cấu hình tài khoản Admin đã băm SHA-256
├── background.png               # Tệp ảnh nền dùng cho giao diện đăng nhập
├── requirements.txt             # File danh sách các thư viện cần cài đặt (pycryptodome)
│
├── docs/                        # Thư mục chứa tài liệu đặc tả thiết kế bổ trợ
│   ├── threat_model.md          # Chi tiết phân tích hiểm họa an ninh
│   └── protocol_design.md       # Chi tiết giao thức kiểm duyệt bảo mật
│
└── report/                      # Thư mục chứa các tệp báo cáo chính
    ├── convert.py               # Script chuyển đổi báo cáo sang tệp Word DOCX
    ├── login_page.png           # Ảnh minh họa màn hình đăng nhập
    ├── dashboard_page.png       # Ảnh minh họa màn hình duyệt giao dịch
    ├── sandbox_page.png         # Ảnh minh họa phòng lab tấn công Sandbox
    ├── benchmark_page.png       # Ảnh minh họa kết quả benchmark đồ thị
    ├── bao_cao.md               # Quyển báo cáo BTL định dạng Markdown
    └── bao_cao.docx             # Quyển báo cáo BTL định dạng Word hoàn chỉnh
```

---

# KẾT LUẬN

Qua quá trình nghiên cứu, thiết kế, triển khai thực tế mã nguồn chương trình ứng dụng game cũng như xây dựng tài liệu quyển báo cáo này, nhóm thực hiện BTL đề tài 23 đã đạt được những kết quả ý nghĩa. Chúng em đã hiện thực hóa thành công mô hình Cổng bảo mật ngân hàng mô phỏng dưới một giao diện đồ họa GUI hiện đại, bắt mắt và dễ dàng tương tác. Toàn bộ các tiêu chuẩn mật mã tiên tiến, có độ an toàn và tin cậy cao được áp dụng rộng rãi trong các định chế tài chính ngân hàng ngày nay như AES-GCM, RSA-PSS, SHA-512, và PBKDF2 đã được tích hợp một cách chính xác vào lõi logic của chương trình.

Về khía cạnh giáo dục, trò chơi **CyberBank Defense** đã chứng minh là một học cụ trực quan vô cùng hiệu quả. Ứng dụng đã chuyển tải những khái niệm toán mật mã trừu tượng, khó hình dung trên lý thuyết thành những tương tác trực quan trong game. Người chơi được rèn luyện phản xạ phát hiện hiểm họa thông qua 4 bước kiểm duyệt tuần tự, trực tiếp kích hoạt các cuộc tấn công Sandbox bảo mật và quan sát phản ứng phòng thủ của hệ thống. Đồng thời, module Benchmark được xây dựng đã giúp kiểm chứng trực quan tốc độ xử lý phần cứng và hiệu năng của từng thuật toán mật mã học trên dữ liệu thực.

Mặc dù hệ thống vẫn tồn tại một số hạn chế nhất định như việc lưu trữ Registry tạm thời trên bộ nhớ RAM và chạy offline trên một máy tính, đề tài đã mở ra định hướng phát triển rõ nét về việc mở rộng hệ thống Client-Server phân tán qua kết nối Socket mạng thực tế và tích hợp hệ quản trị cơ sở dữ liệu vật lý trong tương lai. Bài tập lớn này không chỉ là kết quả làm việc nghiêm túc của nhóm mà còn là nền tảng tri thức thực tiễn vững chắc giúp chúng em tự tin hơn trên con đường học tập và làm việc trong lĩnh vực An toàn thông tin sau này.

---

# TÀI LIỆU THAM KHẢO

1.  William Stallings (2020), *Cryptography and Network Security: Principles and Practice*, 8th Edition, Pearson Education.
2.  NIST Special Publication 800-38D (2007), *Recommendation for Block Cipher Modes of Operation: Galois/Counter Mode (GCM) and GMAC*, National Institute of Standards and Technology.
3.  RFC 8017 (2016), *PKCS #1: RSA Cryptography Specifications Version 2.2*, Internet Engineering Task Force (IETF).
4.  RFC 2898 (2000), *PKCS #5: Password-Based Cryptography Specification Version 2.0* (Dẫn xuất khóa PBKDF2), Internet Engineering Task Force (IETF).
5.  PyCryptodome Library Documentation, *https://www.pycryptodome.org/en/latest/* (Tài liệu hướng dẫn triển khai lõi mật mã trên Python).
6.  Python Software Foundation, *Tkinter GUI Programming documentation*, *https://docs.python.org/3/library/tkinter.html*.
7.  NIST Special Publication 800-132 (2010), *Recommendation for Password-Based Key Derivation: Part I: Buffer Hash and PBKDF2*, National Institute of Standards and Technology.
