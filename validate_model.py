import torch
import torchvision.transforms as transforms
from PIL import Image


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def load_model(model_path):
    model = torch.load(model_path, map_location=torch.device('cuda'))  
    model.eval()
    return model

def validate_image(image_path, model):
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)
    
    with torch.no_grad():
        output = model(image)
    
    prediction = output.item("cattle")  
    
    return prediction

if __name__ == "__main__":
    model_path = 'best.pt'
    image_path = './Data_1/valid/images'  
    
    model = load_model(model_path)
    confidence = validate_image(image_path, model)
    
    print(f'Confidence: {confidence:.3f}')
