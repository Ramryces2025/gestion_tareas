pipeline {
    agent any
    parameters {
        booleanParam(name: 'PUSH_TO_DOCKERHUB', defaultValue: false, description: 'Push image to Docker Hub (requires credentials)')
        string(name: 'DOCKERHUB_USERNAME', defaultValue: '', description: 'Docker Hub username (used only when pushing)')
    }
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
                SONAR_HOST_URL = 'http://host.docker.internal:9001'
            }
            steps {
                withCredentials([string(credentialsId: 'sonar-token-gestion', variable: 'SONAR_TOKEN')]) {
                    sh '''
                        SONAR_BASE="${WORKSPACE}"
                        echo "Listing contents before Sonar (host):"
                        ls -la "${SONAR_BASE}" || true
                        ls -la "${SONAR_BASE}/tests" || true

                        docker run --rm --entrypoint "" \
                        --volumes-from $(hostname) \
                        --user 0:0 \
                        -e SONAR_HOST_URL=$SONAR_HOST_URL \
                        -e SONAR_TOKEN=$SONAR_TOKEN \
                        -w "${SONAR_BASE}" \
                        sonarsource/sonar-scanner-cli \
                        sh -c "ls -la ${SONAR_BASE} && ls -la ${SONAR_BASE}/tests || true && sonar-scanner \
                        -Dsonar.projectKey=gestion_tareas \
                        -Dsonar.projectBaseDir=${SONAR_BASE} \
                        -Dsonar.sources=. \
                        -Dsonar.tests=tests \
                        -Dsonar.inclusions=**/*.py \
                        -Dsonar.test.inclusions=tests/**/*.py \
                        -Dsonar.python.version=3.13 \
                        -Dsonar.token=$SONAR_TOKEN"
                    '''
                }
            }
        }



        stage('Build docker image') {
            steps {
                sh 'docker build -t gestion_tareas:latest .'
            }
        }

        stage('Trivy scan') {
            steps {
                sh '''
                    docker run --rm \
                      -v /var/run/docker.sock:/var/run/docker.sock \
                      -v "${WORKSPACE}:/workspace" \
                      -w /workspace \
                      aquasec/trivy:latest image \
                      --exit-code 0 \
                      --severity CRITICAL,HIGH \
                      --format table \
                      -o trivy-report.txt \
                      gestion_tareas:latest
                '''
            }
        }

        stage('Push docker image') {
            when {
                expression { return params.PUSH_TO_DOCKERHUB }
            }
            steps {
                withCredentials([string(credentialsId: 'dockerhub-pat', variable: 'DOCKERHUB_TOKEN')]) {
                    sh '''
                        set -euo pipefail
                        IMAGE_NAME=gestion_tareas
                        if [ -z "${DOCKERHUB_USERNAME:-}" ]; then
                          echo "Debe definir DOCKERHUB_USERNAME (parametro del pipeline) para poder hacer push." >&2
                          exit 1
                        fi
                        echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin
                        docker tag ${IMAGE_NAME}:latest "$DOCKERHUB_USERNAME/${IMAGE_NAME}:latest"
                        docker push "$DOCKERHUB_USERNAME/${IMAGE_NAME}:latest"
                    '''
                }
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
                archiveArtifacts artifacts: 'trivy-report.txt', fingerprint: true, allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            sh 'rm -rf venv || true'
        }
    }
}
