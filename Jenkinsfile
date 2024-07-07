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
                   pip install torch torchvision torchaudio
                   pip install numpy  
                   pip install pyyaml
                   pip install python-telegram-bot  
                   pip install ultralytics
                '''
            }
        }
        
        stage('Train Model') {
            steps {
                sh ". venv/bin/activate && python train.py"
            }
        }
        
        stage('Validate Model') {
            steps {
                sh ". venv/bin/activate && python validate_model.py"
            }
        }
        
        stage('Use Telegram Bot') {
            steps {
                script {
                    def telegramBotPath = "${WORKSPACE}/Nuevos codigos/telegram_bot.py"
                    sh ". venv/bin/activate && python ${telegramBotPath}"
                }
            }
        }
    }
}