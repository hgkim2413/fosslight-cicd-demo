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
                echo '--- [Dependency] 동적 분석을 위한 패키지 설치 ---'
                sh 'pip install -r requirements.txt'

                echo '--- [Binary] 실행 파일 빌드 ---'
                // 앱 이름: mysystem_monitor
                sh 'pyinstaller --onefile --name mysystem_monitor src/main.py'
            }
        }
        stage('3. Fosslight 검증') {
            steps {
                echo '--- 통합 스캔 수행 ---'
                sh 'fosslight_scanner -p . -o fosslight_report'
            }
        }
    }
    post {
        always {
            // 리포트와 실행 파일 모두 보관
            archiveArtifacts artifacts: 'fosslight_report/**/*, dist/mysystem_monitor', allowEmptyArchive: true
        }
    }
}