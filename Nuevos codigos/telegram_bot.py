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
    model = YOLO("best2.pt")
    cap = cv2.VideoCapture(2)

    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return

    # Enviar mensaje de bienvenida
    await send_message(CHAT_ID, "Bienvenido al bot de mlops para detección de vacas")

    detected_cattle = False
    last_detection_time = time.time()
    last_multiple_detection_time = time.time()
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se puede leer el video de la cámara.")
            break

        results = model(frame)

        print(results)

        cattle_count = 0

        for result in results:
            boxes = result.boxes.cpu().numpy()
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                conf = box.conf[0]
                cls_idx = box.cls[0]
                label = model.names[int(cls_idx)]
                if label.lower() == "cattle" and conf > 0.8:
                    cattle_count += 1
                    detected_cattle = True
                    current_time = time.time()
                    if current_time - last_detection_time > 10:
                        await send_message(CHAT_ID, "Vaca detectada con confianza {:.2f}".format(conf))
                        last_detection_time = current_time
                    # Dibujar un rectángulo alrededor del objeto detectado
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    # Añadir etiqueta de confianza
                    cv2.putText(frame, f'{label} {conf:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        current_time = time.time()
        if cattle_count > 1 and current_time - last_multiple_detection_time > 10:
            await send_message(CHAT_ID, f"Se detectaron {cattle_count} vacas.")
            last_multiple_detection_time = current_time

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) == 27:  # Esc para salir
            break

        if time.time() - start_time > 20:
            if detected_cattle:
                await send_message(CHAT_ID, "Vaca detectada en los últimos 20 segundos.")
                detected_cattle = False
            start_time = time.time()

    cap.release()
    cv2.destroyAllWindows()

async def main():
    await process_video()

if __name__ == "__main__":
    asyncio.run(main())