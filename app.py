import os
import requests
from flask import Flask, render_template, request, jsonify

# 경로 에러 방지를 위한 절대 경로 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')
app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-problem')
def get_problem():
    tier = request.args.get('tier', 13)
    handle = request.args.get('handle', '')
    # 난이도별 랜덤 문제 검색 (한국어 문제, 내가 안 푼 문제)
    query = f"tier:{tier} !@{handle} lang:ko"
    url = f"https://solved.ac/api/v3/search/problem?query={query}&sort=random"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            items = res.json().get('items', [])
            if items: return jsonify(items[0])
    except: pass
    return jsonify({"error": "문제를 찾을 수 없습니다."}), 404

@app.route('/check-status')
def check_status():
    handle = request.args.get('handle')
    problem_id = request.args.get('problemId')
    # 특정 유저가 해당 문제를 풀었는지 확인
    url = f"https://solved.ac/api/v3/search/problem?query=id:{problem_id} @{handle}"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            count = res.json().get('count', 0)
            return jsonify({"solved": count > 0})
    except: pass
    return jsonify({"solved": False})

if __name__ == '__main__':
    # Railway 등 외부 배포를 위한 포트 바인딩
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
