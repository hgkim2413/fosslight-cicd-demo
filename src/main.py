# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Optimus Developer v1

import sys
from flask import Flask

# [Binary Scanner 최적화] PyInstaller 빌드 시 리소스 경로 문제 방지 코드
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Fosslight CI/CD Real World Test: 한글 인코딩 및 라이선스 헤더 확인 중"

if __name__ == "__main__":
    print("앱이 실행되었습니다.")
    # 실제 서버 실행 (테스트용)
    # app.run(host='0.0.0.0', port=5000)