pipeline {
    agent {
        docker {
            image 'python:3.11.3'
            args '-u root:root'
        }
    }
    stages {
        stage('1. 환경 준비') {
            steps {
                script {
                    sh 'apt-get update && apt-get install -y openjdk-17-jre-headless binutils'
                    sh 'pip install --upgrade pip'
                    sh 'pip install fosslight_scanner pyinstaller'
                }
            }
        }
        stage('2. 빌드 및 설치') {
            steps {
                // Dependency: 실제 설치 (동적 분석)
                sh 'pip install -r requirements.txt'
                // Binary: 실제 빌드 (표준 ELF 포맷)
                sh 'pyinstaller --onefile --name real_app src/main.py'
            }
        }
        stage('3. Fosslight 검증') {
            steps {
                sh 'fosslight_scanner -p . -o fosslight_report'
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'fosslight_report/**/*', allowEmptyArchive: true
        }
    }
}