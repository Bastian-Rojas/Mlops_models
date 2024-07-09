import asyncio
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.error import TelegramError
import cv2
import time
from ultralytics import YOLO

TOKEN = "7395836341:AAFyq0FsnEg7GFoOQfrN4vJpymAQVnhdiis"
CHAT_ID = "6180225137"

bot = Bot(token=TOKEN)
cap = None

async def send_message(chat_id, message):
    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except TelegramError as e:
        print(f"Error al enviar mensaje: {e}")

async def take_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global cap

    if cap is not None:
        cap.release()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        await send_message(CHAT_ID, "Error: No se pudo abrir la cámara.")
        return

    ret, frame = cap.read()
    if not ret:
        await send_message(CHAT_ID, "Error: No se pudo tomar la foto.")
        return

    photo_path = 'photo.jpg'
    cv2.imwrite(photo_path, frame)

    try:
        await bot.send_photo(chat_id=CHAT_ID, photo=open(photo_path, 'rb'))
    except TelegramError as e:
        print(f"Error al enviar foto: {e}")

    cap.release()
    cap = cv2.VideoCapture(0)

async def process_video():
    global cap
    model = YOLO("best2.pt")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return

    await send_message(CHAT_ID, "Bienvenido al bot de mlops para detección de vacas, Usa /foto para tomar una foto")

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
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(frame, f'{label} {conf:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        current_time = time.time()
        if cattle_count > 1 and current_time - last_multiple_detection_time > 10:
            await send_message(CHAT_ID, f"Se detectaron {cattle_count} vacas.")
            last_multiple_detection_time = current_time

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) == 27:
            break

        if time.time() - start_time > 20:
            if detected_cattle:
                await send_message(CHAT_ID, "Vaca detectada en los últimos 20 segundos.")
                detected_cattle = False
            start_time = time.time()

    cap.release()
    cv2.destroyAllWindows()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_message(CHAT_ID, "¡Hola! Usa /takephoto para tomar una foto.")

async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("foto", take_photo))

    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await process_video()
    await application.stop()

if __name__ == "__main__":
    asyncio.run(main())