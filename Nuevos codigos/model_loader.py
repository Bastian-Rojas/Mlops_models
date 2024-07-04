from ultralytics import YOLO

def load_model(model_path="best2.pt"):
    return YOLO(model_path)