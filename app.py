from flask import Flask, request, jsonify, render_template
import openai
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:
        # 기본 레시피 생성
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """당신은 요리 전문가입니다. 사용자가 입력한 재료를 기반으로 최소 3가지 요리 레시피를 제안하세요. 각 요리는 사용자가 제공한 재료만을 활용해야 합니다. 사용자가 제공하지 않은 소금과 같은 기본 조미료들은 추가하지 마세요.
                        각 요리 레시피는 아래 형식을 따르세요:

                        1.요리 이름 (한글 이름, 영문 이름) 
                        - 재료: 필요한 재료를 간단히 나열하세요.  
                        - 조리법:  
                            -  요리를 시작하는 첫 단계 설명  
                            -  다음 단계 설명  
                            -  필요한 모든 단계를 포함  
                            -  완성 단계 설명  

                    응답은 항상 한국어로 작성하고, 간결하며 읽기 쉽게 표현해야 합니다.  
                    추가적인 설명이나 불필요한 HTML 태그, 스타일은 포함하지 마세요."""
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            max_tokens=1000,
            temperature=0.8
        )

        reply = response['choices'][0]['message']['content']
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate-image", methods=["POST"])
def generate_image():
    description = request.json.get("description", "")

    if not description:
        return jsonify({"error": "No description provided"}), 400

    try:
        # DALL·E 이미지 생성
        image_response = openai.Image.create(
            prompt=description,
            n=1,
            size="512x512"
        )
        image_url = image_response['data'][0]['url']
        return jsonify({"image_url": image_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
