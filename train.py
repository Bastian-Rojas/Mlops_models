import yaml
import os

# Cargar hiperparámetros desde config.yaml
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Construir el comando de entrenamiento con los parámetros cargados
command = (
    f"yolo task=detect mode=train "
    f"epochs={config['epochs']} "
    f"data=data.yaml "
    f"model=yolov8l.pt "
    f"imgsz={config['imgsz']} "
    f"batch={config['batch']} "
    f"lr0={config['lr0']} "
    f"weight_decay={config['weight_decay']} "
    f"momentum={config['momentum']} "
    f"patience={config['patience']} "   # Early stopping
    f"cos_lr={config['cos_lr']} "       # Cosine Annealing LR
    f"augment=True "                    # Aumentación de datos
)

print("Ejecutando comando:", command)

os.system(command)