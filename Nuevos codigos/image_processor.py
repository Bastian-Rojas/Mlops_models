import cv2
import os


def process_images(directory_path, model):
    
    cv2.namedWindow("Deteccion Bovinos", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Deteccion Bovinos", 1280, 720)

    screen_width = cv2.getWindowImageRect('Deteccion Bovinos')[2]
    screen_height = cv2.getWindowImageRect('Deteccion Bovinos')[3]

    window_width = 1280
    window_height = 720
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    cv2.moveWindow("Deteccion Bovinos", x, y)

    image_files = [f for f in os.listdir(directory_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    image_files.sort()
    total_images = len(image_files)

    current_image_index = 0

    while True:
        if 0 <= current_image_index < total_images:
            image_path = os.path.join(directory_path, image_files[current_image_index])
            image = cv2.imread(image_path)

            results = model.predict(image, imgsz=640, conf=0.7)

            for result in results:
                annotated_image = result.plot()
                cv2.imshow("Deteccion Bovinos", annotated_image)

        key = cv2.waitKey(0) & 0xFF

        if key == 27:
            break
        elif key == ord('d'):
            current_image_index += 1
            if current_image_index >= total_images:
                current_image_index = 0
        elif key == ord('a'):
            current_image_index -= 1
            if current_image_index < 0:
                current_image_index = total_images - 1

    cv2.destroyAllWindows()