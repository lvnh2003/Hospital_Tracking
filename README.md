# Hospital_Tracking

## Giới Thiệu

Ứng dụng này được thiết kế để phát hiện người bị ngã trong bệnh viện thông qua camera giám sát. Khi phát hiện có người bị ngã, hệ thống sẽ:
- Gửi thông báo đến ứng dụng điện thoại.
- Phát ra tiếng báo động tại khu vực camera.
- Quản lý các camera giám sát.

## Các Tính Năng

1. **Phát hiện người bị ngã**: Sử dụng các thuật toán xử lý hình ảnh để phát hiện khi có người bị ngã trong khu vực giám sát.
2. **Gửi thông báo đến ứng dụng điện thoại**: Sử dụng Firebase Cloud Messaging để gửi thông báo đến ứng dụng điện thoại khi có người bị ngã.
3. **Phát ra tiếng báo động**: Phát ra âm thanh cảnh báo tại khu vực camera khi phát hiện có người bị ngã.
4. **Quản lý camera**: Quản lý danh sách các camera giám sát, thêm, xóa và cấu hình các camera.

## Yêu Cầu Hệ Thống

- Python 3.x
- File `serviceAccountKey.json` từ Firebase  ,`registration_token` từ ứng dụng Android https://github.com/ZzlinhzZ/Hospital_Help.git ,`client_id` từ Imgur 
## Cài Đặt

1. **Cài đặt Python và các thư viện cần thiết**

   ```sh
   pip install -r requirement.txt
    ```

2. **Thêm các File và token yêu cầu**
3. **Chạy dự án**
   ```sh
   python main.py
    ```
## Demo 
![Home](/resources/home.png)
![Memu](/resources/menu.png)