import cv2
import os


def process_images(directory_path, model):
    # Crear ventana con tamaño fijo
    cv2.namedWindow("Deteccion Ovinos", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Deteccion Ovinos", 1280, 720)

    # Obtener dimensiones de la pantalla
    screen_width = cv2.getWindowImageRect('Deteccion Ovinos')[2]
    screen_height = cv2.getWindowImageRect('Deteccion Ovinos')[3]

    # Calcular la posición para centrar la ventana
    window_width = 1280
    window_height = 720
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Mover la ventana al centro de la pantalla
    cv2.moveWindow("Deteccion Ovinos", x, y)

    # Obtener lista de archivos de imagen en el directorio
    image_files = [f for f in os.listdir(directory_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    image_files.sort()  # Ordenar la lista de archivos
    total_images = len(image_files)

    current_image_index = 0

    while True:
        if 0 <= current_image_index < total_images:
            image_path = os.path.join(directory_path, image_files[current_image_index])
            image = cv2.imread(image_path)

            # Realizar predicciones en la imagen
            results = model.predict(image, imgsz=640, conf=0.7)

            # Anotar y mostrar la imagen
            for result in results:
                annotated_image = result.plot()
                cv2.imshow("Deteccion Ovinos", annotated_image)

        key = cv2.waitKey(0) & 0xFF

        if key == 27:  # Esc para salir
            break
        elif key == ord('d'):  # Siguiente imagen
            current_image_index += 1
            if current_image_index >= total_images:
                current_image_index = 0  # Volver al inicio
        elif key == ord('a'):  # Imagen anterior
            current_image_index -= 1
            if current_image_index < 0:
                current_image_index = total_images - 1  # Ir al final

    cv2.destroyAllWindows()