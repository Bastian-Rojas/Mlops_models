pipeline {
    agent any
    
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
                   pip install torch==1.10.0+cu113 torchvision==0.11.1+cu113 torchaudio==0.10.0+cu113 -f https://download.pytorch.org/whl/torch_stable.html
                   pip install numpy  # Asegúrate de incluir otras bibliotecas necesarias
                   pip install python-telegram-bot  # Instalar la biblioteca para Telegram
                '''
            }
        }
        
        stage('Train Model') {
            steps {
                sh '. venv/bin/activate && python train_model.py'
            }
        }
        
        stage('Validate Model') {
            steps {
                sh '. venv/bin/activate && python validate_model.py'
            }
        }
        
        stage('Use Telegram Bot') {
            steps {
                script {
                    def telegramBotPath = "${WORKSPACE}\\Nuevos codigos\\telegram_bot.py"
                    sh ". venv/bin/activate && python ${telegramBotPath}"
                }
            }
        }
    }
    
    post {
        always {
            sh 'deactivate || true'
        }
        success {
            echo 'Pipeline ejecutado con éxito'
        }
        failure {
            echo 'Pipeline fallido'
        }
    }
}
