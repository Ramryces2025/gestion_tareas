pipeline {
    agent any
    environment {
        PYTHONPATH = "${WORKSPACE}"
    }

    stages {
        stage('Install dependencies') {
            steps {
                sh '''
                    PYTHON=$(command -v python3 || command -v python)
                    if [ -z "$PYTHON" ]; then
                      echo "Python is required on the Jenkins agent." >&2
                      exit 1
                    fi
                    $PYTHON -m venv venv
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
