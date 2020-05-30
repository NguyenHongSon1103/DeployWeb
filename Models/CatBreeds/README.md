# DeployWeb
Folder to add Cat Breeds

Các kĩ thuật sử dụng: 
* Chuẩn bị dữ liệu: 
    - Dữ liệu thô là các ảnh chứa trong các thư mục ứng với từng giống,
     cùng với đó là một file csv gồm các trường: tên ảnh - giống - giới tính - độ tuổi
     - Đọc các thông tin từ file csv. Lúc này data là các tên file còn nhãn 
     được đưa về dạng one-hot.
     - Vì lượng dữ liệu lớn không thể đưa vào bộ nhớ trong cùng một thời điểm nên cần
     thực hiện đưa dữ liệu vào theo batch => Viết một class đảm nhận vai trò data generator
     cho bài toán.
* Xây dựng mô hình: Thực hiện finetuning với các mô hình gồm 2 phần
    - Một mạng backbone có nhiệm vụ trích xuất các đặc trưng của dữ liệu
        - Sử dụng API có sẵn của keras với việc bỏ đi lớp phân loại cuối
    - Các lớp FC đảm nhận vai trò của một bộ phân lớp
        - Tinh chỉnh các tham số dựa trên kết quả quan sát được của bài toán
* Vấn đề gặp phải : overfit
    - Các mô hình đã xây dựng hầu hết đều gặp tình trạng overfit
    .Do thời gian huấn luyện một mô hình là khá lâu (5-7 tiếng/lần) nên nhóm cũng gặp phải
    các hạn chế khi áp dụng các phương pháp để hạn chế tình trạng overfiting.
    - Một số phương pháp đã sử dụng:
        - Thay đổi các mạng backbone: Một số mạng đã được nhóm sử dụng như: Mobilenet (v1/v2), InceptionV3,
        InceptionResnet50, VGG16, Xception -> Hầu như kết quả không thay đổi.
        - Giảm số lượng lớp FC và số hidden unit ở mỗi lớp trong bộ phân lớp.
        - Thêm vào các lớp BatchNormalization + ReLU, Dropout ở mỗi lớp FC giúp mô hình hội tụ tốt hơn một chút
        - Thay đổi các thuật toán tối ưu: Adam, SGD, RMSProp
        - Train trên các ảnh nguyên hình con mèo được cắt từ ảnh gốc-> hạn chế tác động của nền tới mô hình, 
        điều này giúp tăng kết quả thêm một chút.
* Kết quả:
    - Các mô hình gặp phải vấn đề overfit với train's lost và validation's lost khoảng 0.44 - 4.56