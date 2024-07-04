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
                   pip install torch==2.3.1+cu121 torchvision==0.18.1+cu121 numpy==1.26.4
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
                    // Definir la ruta completa al archivo telegram_bot.py
                    def telegramBotPath = "${WORKSPACE}\\Nuevos codigos\\telegram_bot.py"
                    // Ejecutar el script usando el entorno virtual
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