pipeline {
    agent any
    
    environment {
        MODEL_PATH = 'best.pt' // Define la ruta del modelo entrenado
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                sh '''
                   python3 -m venv venv
                   . venv/bin/activate
                   pip install --upgrade pip
                   pip install torch torchvision torchaudio
                   pip install numpy  
                   pip install pyyaml
                   pip install ultralytics
                '''
            }
        }
        
        stage('Train Model') {
            steps {
                sh ". venv/bin/activate && python train.py"
                // Mueve el modelo entrenado a la ubicación esperada
                sh "mv runs/train/exp/weights/best.pt ${MODEL_PATH}"
            }
        }
        
        stage('Validate Model') {
            steps {
                sh ". venv/bin/activate && python validate_model.py"
            }
        }
        
        stage('Process Image') {
            steps {
                script {
                    def imageProcessorPath = "${WORKSPACE}/image_processor.py"
                    def imagePath = "${WORKSPACE}/images/frisona.jpg"  // Ruta a la imagen frisona.jpg
                    sh ". venv/bin/activate && python ${imageProcessorPath} ${imagePath}"
                }
            }
        }
    }
}