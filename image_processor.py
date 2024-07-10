import cv2
import os
import sys
import torch
import torchvision.transforms as transforms
from PIL import Image
from ultralytics import YOLO

# Definir las transformaciones de la imagen
transform = transforms.Compose([
    transforms.Resize((640, 640)),  # Cambiado a 640x640 para coincidir con el tamaño esperado por YOLO
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def load_model(model_path):
    model = YOLO(model_path)
    model.eval()
    return model

def process_image(image_path, model):
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)
    
    with torch.no_grad():
        results = model(image)
    
    # Convertir la imagen original a formato OpenCV
    original_image = cv2.imread(image_path)
    
    # Anotar la imagen con los resultados
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy()
        class_ids = result.boxes.cls.cpu().numpy()
        
        for box, confidence, class_id in zip(boxes, confidences, class_ids):
            x1, y1, x2, y2 = map(int, box)
            label = f'{model.names[int(class_id)]}: {confidence:.2f}'
            cv2.rectangle(original_image, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(original_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
    
    # Guardar la imagen anotada
    output_path = os.path.splitext(image_path)[0] + "_annotated.jpg"
    cv2.imwrite(output_path, original_image)
    print(f"Imagen anotada guardada en {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python image_processor.py <ruta_de_la_imagen>")
        sys.exit(1)

    image_path = sys.argv[1]
    
    # Cargar el modelo
    model_path = 'best.pt'  # Sustituye esto con la ruta real a tu modelo
    model = load_model(model_path)

    process_image(image_path, model)