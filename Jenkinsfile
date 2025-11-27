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
                sh '. venv/bin/activate && pytest --junitxml=test-results.xml'
                junit 'test-results.xml'
            }
        }

        stage('SonarQube analysis') {
            environment {
                SONAR_HOST_URL = 'http://sonarqube:9000'
            }
            steps {
                withCredentials([string(credentialsId: 'sonar-token-gestion', variable: 'SONAR_TOKEN')]) {
                    sh '''
                        docker run --rm \
                          --network bridge \
                          -e SONAR_HOST_URL=$SONAR_HOST_URL \
                          -e SONAR_LOGIN=$SONAR_TOKEN \
                          -v "$PWD":/usr/src \
                          sonarsource/sonar-scanner-cli \
                          -Dsonar.projectKey=gestion_tareas \
                          -Dsonar.sources=. \
                          -Dsonar.tests=tests \
                          -Dsonar.python.version=3.13
                    '''
                }
            }
        }

        stage('Build docker image') {
            steps {
                sh 'docker build -t gestion_tareas:latest .'
            }
        }

        stage('Package artifacts') {
            steps {
                sh '''
                    cat > build_info.txt <<EOF
Build: ${BUILD_NUMBER}
Git commit: ${GIT_COMMIT:-unknown}
Branch: ${GIT_BRANCH:-unknown}
Built image: gestion_tareas:latest
EOF
                '''
                archiveArtifacts artifacts: 'test-results.xml, build_info.txt', fingerprint: true
            }
        }
    }

    post {
        always {
            sh 'rm -rf venv || true'
        }
    }
}
