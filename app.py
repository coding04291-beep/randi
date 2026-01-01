import os
import requests
from flask import Flask, render_template, request, jsonify

# 폴더 경로를 명시적으로 지정하여 크래시 방지
template_dir = os.path.abspath('templates')
app = Flask(__name__, template_folder=template_dir)
# 티어 이름 정의
TIER_NAMES = [
    "Unrated", "B5", "B4", "B3", "B2", "B1", 
    "S5", "S4", "S3", "S2", "S1", 
    "G5", "G4", "G3", "G2", "G1", 
    "P5", "P4", "P3", "P2", "P1",
    "D5", "D4", "D3", "D2", "D1",
    "R5", "R4", "R3", "R2", "R1"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-problem')
def get_problem():
    tier = request.args.get('tier', 13)
    handle = request.args.get('handle', '')
    query = f"tier:{tier} !@{handle} lang:ko"
    
    url = f"https://solved.ac/api/v3/search/problem?query={query}&sort=random"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            items = res.json().get('items', [])
            if items:
                return jsonify(items[0])
    except:
        pass
    return jsonify({"error": "문제를 찾을 수 없습니다."}), 404

@app.route('/check-status')
def check_status():
    handle = request.args.get('handle')
    problem_id = request.args.get('problemId')
    
    url = f"https://solved.ac/api/v3/search/problem?query=id:{problem_id} @{handle}"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            count = res.json().get('count', 0)
            return jsonify({"solved": count > 0})
    except:
        pass
    return jsonify({"solved": False})

if __name__ == '__main__':
    # Railway/Render 등 배포 환경에서 할당한 포트를 사용함
    # host='0.0.0.0'은 외부 모든 접속을 허용한다는 설정 (필수)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

