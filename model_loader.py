from ultralytics import YOLO

def load_model(model_path="best.pt"):
    return YOLO(model_path)