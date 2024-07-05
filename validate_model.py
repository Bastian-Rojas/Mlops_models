import torch
import torchvision.transforms as transforms
from PIL import Image
import os
from ultralytics import YOLO

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def load_model(model_path):
    model = YOLO(model_path)  # Utiliza la clase YOLO para cargar el modelo correctamente
    model.eval()
    return model

def validate_image(image_path, model):
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)
    
    with torch.no_grad():
        output = model(image)
    
    prediction = output[0].item()  # Ajusta esto según la salida específica de tu modelo
    
    return prediction

if __name__ == "__main__":
    model_path = 'best.pt'
    base_dir = r'D:\Mlops_models\Data_1\valid'
    image_filename = '20_jpg.rf.7b3d4b4e991d768c4a111d4b00db1ced.jpg'
    image_path = os.path.join(base_dir, 'images', image_filename)
    
    model = load_model(model_path)
    confidence = validate_image(image_path, model)
    
    print(f'Confidence: {confidence:.3f}')
