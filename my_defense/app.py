from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# 티어 이름 변환 테이블 (0~30)
TIER_NAMES = [
    "Unrated", 
    "B5", "B4", "B3", "B2", "B1", 
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
    
    # 쿼리: 특정 티어 + 유저가 안 푼 문제
    query = f"tier:{tier} !@{handle} lang:ko"
    url = f"https://solved.ac/api/v3/search/problem?query={query}&sort=random"
    
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            items = res.json().get('items', [])
            if items:
                return jsonify(items[0])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"error": "문제를 찾을 수 없습니다."}), 404

@app.route('/check-status')
def check_status():
    handle = request.args.get('handle')
    problem_id = request.args.get('problemId')
    
    if not handle or not problem_id:
        return jsonify({"solved": False})

    # Solved.ac 검색 쿼리로 해당 유저가 문제를 풀었는지 대조
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
    # 5000번 포트에서 실행
    app.run(port=5000, debug=True)