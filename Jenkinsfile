pipeline {
    agent any

    stages {
        stage('Install dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '. venv/bin/activate && pytest -q'
            }
        }

        stage('Build docker image') {
            steps {
                sh 'docker build -t gestion_tareas:latest .'
            }
        }
    }

    post {
        always {
            sh 'rm -rf venv || true'
        }
    }
}
