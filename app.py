# app.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def fetch_github_data(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "repos": data["public_repos"],
            "followers": data["followers"],
            "following": data["following"]
        }
    return None

def fetch_codeforces_data(username):
    url = f"https://codeforces.com/api/user.info?handles={username}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["result"][0]
        return {
            "rating": data["rating"],
            "max_rating": data["maxRating"],
            "rank": data["rank"]
        }
    return None

@app.route('/')
def home():
    return "Backend is running!"

@app.route('/analyze', methods=['POST'])
def analyze_profile():
    data = request.get_json()
    github_username = data.get('github')
    codeforces_handle = data.get('codeforces')

    github_data = fetch_github_data(github_username)
    codeforces_data = fetch_codeforces_data(codeforces_handle)

    if not github_data or not codeforces_data:
        return jsonify({"error": "Invalid username or handle"}), 400

    profile_score = min(github_data["repos"] * 2, 100) + min(codeforces_data["rating"] // 20, 100)
    profile_score = min(profile_score // 2, 100)
    readiness_score = profile_score + 10 if profile_score > 50 else profile_score

    insights = []
    if github_data["repos"] < 5:
        insights.append("Increase GitHub contributions by creating more repositories.")
    if codeforces_data["rating"] < 1200:
        insights.append("Solve more Codeforces problems to boost your rating.")

    return jsonify({
        "profileScore": profile_score,
        "readinessScore": readiness_score,
        "insights": insights
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)