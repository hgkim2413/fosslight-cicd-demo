pipeline {
    agent {
        docker {
            image 'python:3.11.3'
            args '-u root:root'
        }
    }

    stages {
        stage('1. 환경 설정 (Setup)') {
            steps {
                script {
                    echo '--- 시스템 패키지 설치 (Binary 분석용) ---'
                    sh 'apt-get update'
                    sh 'apt-get install -y openjdk-17-jre-headless binutils'
                    
                    echo '--- Python 도구 설치 ---'
                    sh 'pip install --upgrade pip'
                    sh 'pip install fosslight_scanner pyinstaller'
                }
            }
        }

        stage('2. 빌드 및 동적 환경 구성 (Build & Install)') {
            steps {
                echo '--- [Dependency] 패키지 실제 설치 ---'
                sh 'pip install -r requirements.txt'

                echo '--- [Binary] 실행 파일(ELF) 빌드 ---'
                // src 폴더 안의 main.py를 빌드하여 dist/optimus_app 생성
                sh 'pyinstaller --onefile --name optimus_app src/main.py'
            }
        }

        stage('3. Fosslight 정밀 스캔') {
            steps {
                echo '--- 통합 스캔 수행 ---'
                // 현재 폴더(.) 전체를 스캔
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