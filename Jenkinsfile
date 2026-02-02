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
                    sh 'pip install fosslight_scanner pyinstaller pandas openpyxl'
                }
            }
        }
        stage('2. 빌드 및 설치') {
            steps {
                echo '--- [Dependency] 진짜 환경에 패키지 설치 ---'
                sh 'pip install -r requirements.txt'

                echo '--- [Debug] 설치된 패키지 확인 ---'
                sh 'pip list'

                echo '--- [Binary] 실행 파일 빌드 ---'
                sh 'pyinstaller --onefile --hidden-import=psutil --hidden-import=requests --hidden-import=colorama --name mysystem_monitor src/main.py'
            }
        }
        stage('3. Fosslight 검증') {
            steps {
                echo '--- 통합 스캔 수행 ---'
                sh 'fosslight_scanner -p . -o fosslight_report'
            }
        }
        stage('4. Quality Gate (정책 검사)') {
            steps {
                echo '--- [Policy] 라이선스 위반 여부 정밀 검사 ---'
                script {
                    // Python 스크립트 생성 (시트 이름 수정됨: SRC -> SRC_FL_Source)
                    def pythonScript = """
import os
import sys
import pandas as pd

# 1. 리포트 파일 찾기
report_dir = 'fosslight_report'
files = [f for f in os.listdir(report_dir) if f.endswith('.xlsx') and not f.startswith('~')]
if not files:
    print("[Error] 리포트 파일이 없습니다!")
    sys.exit(1)

report_path = os.path.join(report_dir, files[0])
print(f"[Info] 검사할 리포트: {report_path}")

try:
    # 2. 엑셀의 'SRC_FL_Source' 시트 읽기 (사용자가 알려준 정확한 시트명 사용)
    # 필요하다면 'BIN_FL_Source', 'DEP_FL_Dependency'도 읽을 수 있음
    df = pd.read_excel(report_path, sheet_name='SRC_FL_Source')
    
    # 3. 'License' 컬럼에서 'GPL' 글자가 들어간 것 찾기 (대소문자 무시)
    gpl_violation = df[df['License'].astype(str).str.contains('GPL', case=False, na=False)]

    if not gpl_violation.empty:
        print("=" * 60)
        print("🚨 [비상] GPL 라이선스가 감지되었습니다! 배포를 중단합니다. 🚨")
        print("=" * 60)
        # 위반된 파일 목록 출력
        print(gpl_violation[['Source Path', 'License']])
        print("=" * 60)
        sys.exit(1) # 젠킨스에게 '실패' 신호를 보냄
    else:
        print("✅ [통과] GPL 라이선스가 발견되지 않았습니다. 안전합니다.")

except ValueError as ve:
    print(f"[Error] 시트를 찾을 수 없습니다: {ve}")
    print("엑셀 파일에 'SRC_FL_Source' 시트가 있는지 확인해주세요.")
    sys.exit(1)
except Exception as e:
    print(f"[Error] 검사 중 예상치 못한 오류 발생: {e}")
    sys.exit(1)
"""
                    writeFile file: 'quality_check.py', text: pythonScript
                    
                    // 파이썬 스크립트 실행
                    sh 'python quality_check.py'
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'fosslight_report/**/*, dist/mysystem_monitor', allowEmptyArchive: true
        }
    }
}