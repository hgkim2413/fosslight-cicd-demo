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
                echo '--- [Debug] 설치된 패키지 확인 ---'
                // pip list를 찍어서 로그에 psutil이 진짜 깔렸는지 확인용
                sh 'pip list' 

                echo '--- [Binary] 실행 파일 빌드 (강제 포함 옵션 추가) ---'
                // --hidden-import 옵션으로 누락 방지
                sh 'pyinstaller --onefile --hidden-import=psutil --hidden-import=requests --hidden-import=colorama --name mysystem_monitor src/main.py'
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