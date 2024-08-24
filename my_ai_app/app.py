import os
from flask import Flask, request, render_template, redirect, url_for
import google.generativeai as genai
from PIL import Image

# Flask 앱 초기화
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# 구글 API 키 설정
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# 메인 페이지 라우팅
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            img = Image.open(file_path)
            
            # 이미지에 대한 설명 생성 요청
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            response = model.generate_content(["What is in this photo?", img])
            
            # 결과 페이지로 리다이렉트
            return render_template("result.html", description=response.text)
    
    return render_template("index.html")

# 결과 페이지 라우팅
@app.route("/result")
def result():
    description = request.args.get("description", "")
    return render_template("result.html", description=description)

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
