import requests
import firebase_admin
from firebase_admin import credentials, messaging

# Khởi tạo Firebase Admin SDK, tải file serviceAccountKey.json từ firebase
cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)
# Registration token
registration_token = 'YOUR_REGISTRATION_ID'

def uploadImageToImgur(image_path):
    """
    Tải ảnh lên Imgur và trả về URL của ảnh đã tải lên.

    Args:
        image_path (str): Đường dẫn tới tệp ảnh cần tải lên.

    Returns:
        str: URL của ảnh đã tải lên.
    """
    # Register an application để lấy client_id
    client_id = 'YOUR_CLIENT_ID'
    headers = {"Authorization": f"Client-ID {client_id}"}
    with open(image_path, "rb") as image_file:
        image_data = {"image": image_file.read()}
    response = requests.post("https://api.imgur.com/3/upload", headers=headers, files=image_data)

    if response.status_code == 200:
        return response.json()['data']['link']
    else:
        raise Exception("Failed to upload image to Imgur")


def sendMessage(content, image_url):
    if image_url:
        message = messaging.Message(
            notification=messaging.Notification(
                title="Detect Falling",
                body=f"Detect person is falling in room {content}",
                image=image_url
            ),
            token=registration_token
        )
        # Gửi thông báo
        messaging.send(message)
