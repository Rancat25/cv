import flet as ft
import cv2
import asyncio

def main(page: ft.Page):
    camera = None
    video_feed = ft.Image(width=640, height=480)

    async def open_camera(e):
        nonlocal camera
        if camera is None:
            camera = cv2.VideoCapture(0)  # تأكد من استخدام الكاميرا الصحيحة
            if not camera.isOpened():
                print("Error: Could not open camera.")
                return
        await update_feed()

    def close_camera(e):
        nonlocal camera
        if camera is not None:
            camera.release()
            camera = None
            video_feed.src = None
        page.update()

    async def update_feed():
        while camera is not None and camera.isOpened():
            ret, frame = camera.read()
            if ret:
                _, img_encoded = cv2.imencode('.jpg', frame)
                video_feed.src_base64 = img_encoded.tobytes()
                page.update()
            await asyncio.sleep(0.03)

    # أزرار فتح وإغلاق الكاميرا
    open_button = ft.ElevatedButton(text="Open Camera", on_click=open_camera)
    close_button = ft.ElevatedButton(text="Close Camera", on_click=close_camera)

    # إضافة العناصر إلى الصفحة
    page.add(
        video_feed,
        open_button,
        close_button
    )

# تشغيل التطبيق
ft.app(target=main)
