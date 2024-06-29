import cv2

def process_video(video_path, model, slow_factor=2):
    cap = cv2.VideoCapture(video_path)

    # Crear ventana con tamaño fijo
    cv2.namedWindow("Vacas", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Vacas", 1280, 720)

    paused = False
    current_frame = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                break

            # Realizar predicciones en el frame
            results = model.predict(frame, imgsz=640, conf=0.6)

            # Anotar y mostrar el frame
            for result in results:
                annotated_frame = result.plot()
                cv2.imshow("Vacas", annotated_frame)

            current_frame += 1

        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # Esc para salir
            break
        elif key == ord(' '):  # Barra espaciadora para pausar/reanudar
            paused = not paused
        elif key == ord('d'):  # Flecha derecha para adelantar
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame + 30)  # Adelantar 30 frames
            current_frame += 30
        elif key == ord('a'):  # Flecha izquierda para retroceder
            current_frame = max(0, current_frame - 30)  # Retroceder 30 frames
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)

    cap.release()
    cv2.destroyAllWindows()
