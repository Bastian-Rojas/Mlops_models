import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image

# Definir transformaciones para las imágenes
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def load_model(model_path):
    model = models.resnet18(pretrained=False)
    num_ftrs = model.fc.in_features
    model.fc = torch.nn.Linear(num_ftrs, 1)  # Capa final para clasificación binaria
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

def validate_image(image_path, model):
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)
    
    with torch.no_grad():
        output = model(image)
    
    prediction = torch.sigmoid(output).item()  # Aplicar sigmoid para obtener una probabilidad entre 0 y 1
    
    return prediction

if __name__ == "__main__":
    model_path = 'best.pt'
    image_path = 'D:\Mlops_models\Data_1\valid\images'
    
    model = load_model(model_path)
    confidence = validate_image(image_path, model)
    
    print(f'Confidence: {confidence:.3f}')