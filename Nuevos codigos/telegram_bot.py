import asyncio
from telegram import Bot
from telegram.error import TelegramError
import cv2
import time
from ultralytics import YOLO

TOKEN = "7395836341:AAFyq0FsnEg7GFoOQfrN4vJpymAQVnhdiis"
CHAT_ID = "6180225137"
bot = Bot(token=TOKEN)

async def send_message(chat_id, message):
    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except TelegramError as e:
        print(f"Error al enviar mensaje: {e}")

async def process_video():
    model = YOLO("best.pt")  # Asumiendo que este es el path correcto del modelo
    cap = cv2.VideoCapture(0)  # Asumiendo que se utiliza la cámara web por defecto

    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return

    # Enviar mensaje de bienvenida
    await send_message(CHAT_ID, "Bienvenido al bot de mlops para detección de vacas")

    detected_cattle = False
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se puede leer el video de la cámara.")
            break

        # Procesamiento de la imagen con el modelo YOLO
        results = model.predict(frame, imgsz=640, conf=0.8)

        # Revisar los resultados para encontrar 'cattle'
        for result in results:
            for detection in result:
                if len(detection) < 6:
                    continue  # Skip if the detection does not contain enough values

                x1, y1, x2, y2, conf, cls_idx = detection[:6]
                label = model.names[int(cls_idx)]
                if label.lower() == "cattle" and conf > 0.8:
                    detected_cattle = True
                    await send_message(CHAT_ID, "Cattle detectado con confianza {:.2f}".format(conf))

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) == 27:  # Esc para salir
            break

        # Verificar si ha pasado suficiente tiempo y enviar un mensaje
        if time.time() - start_time > 15:  # cada 15 segundos
            if detected_cattle:
                await send_message(CHAT_ID, "Cattle detectado en los últimos 15 segundos.")
                detected_cattle = False  # Restablece la detección
            start_time = time.time()  # Reinicia el contador

    cap.release()
    cv2.destroyAllWindows()

async def main():
    await process_video()

if __name__ == "__main__":
    asyncio.run(main())