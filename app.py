from flask import Flask, request, jsonify, send_file
import requests

app = Flask(__name__)

# ---------- YOUR FULL RESUME (exactly from the document) ----------
RESUME_CONTEXT = """
Hafiza Rida Fatima

AI / ML Engineer · NLP & Generative AI

hafizaridafatima3@gmail.com | https://www.linkedin.com/in/hafiza-rida-fatima-1bba53234 | https://github.com/HafizaRidaFatima | Lahore, Pakistan

PROFESSIONAL SUMMARY
Motivated and detail-oriented AI/ML Engineer currently pursuing a degree in Software Engineering, with a strong focus on Natural Language Processing and Generative AI. Proficient in Python and core ML frameworks, with hands-on experience building intelligent text-driven applications. Passionate about leveraging large language models and transformer architectures to solve real-world problems. Eager to contribute to a forward-thinking AI team through a focused engineering internship.

TECHNICAL SKILLS
Languages: Python
ML / AI: Scikit-learn, TensorFlow, Hugging Face, Transformers
NLP & GenAI: LLMs, Prompt Engineering, RAG
Data & Tools: NumPy, Pandas, Matplotlib, Seaborn, Jupyter Notebook, Google Colab
Dev Tools: Git, GitHub, VS Code
Mathematics: Linear Algebra, Probability & Statistics, Calculus
Soft Skills: Strong Communication, Teamwork, Problem-Solving, Analytical Thinking

EXPERIENCE
Associate Software Engineer Intern (June 2025 -- August 2025) – COD Crafters
- Completed a 3-month internship developing practical software solutions using Python, strengthening core technical skills.
- Awarded Certificate of Achievement for outstanding dedication and performance throughout the internship.

Project Evaluation Volunteer (April 2025) – Expo Lahore
- Volunteered at a university-level project evaluation event, supporting evaluation workflows and coordinating with organizing teams to ensure seamless operations.

PROJECTS
- Sentiment Analysis & Text Classifier (2026)
  Python · Scikit-learn · Pandas · NLTK · Matplotlib
  ▸ Developed a sentiment analysis model to classify text as positive or negative using a custom dataset of 1000+ samples.
  ▸ Applied NLP techniques including text preprocessing, stop word removal, and TF-IDF vectorization with n-grams for feature extraction.
  ▸ Implemented and compared multiple machine learning models such as Logistic Regression, Random Forest, Gradient Boosting, and Naive Bayes to evaluate performance.
  ▸ Optimized model performance using evaluation metrics like accuracy, confusion matrix, and classification report, achieving reliable prediction results.

- Car-Price-Prediction-Linear-Regression-Model (2026)
  Python · Scikit-learn · Pandas · NumPy · Matplotlib
  ▸ Built a Linear Regression model to predict car prices based on key features such as mileage, year, and engine size.
  ▸ Performed data preprocessing, feature engineering, and exploratory data analysis to improve model performance.
  ▸ Evaluated the model using MAE, MSE, and R² score to ensure accurate and reliable predictions.

EDUCATION
Bachelor of Science in Software Engineering (2026 -- Present) – Lahore College For Women University (LCWU), Lahore, Pakistan
- Relevant Coursework: Machine Learning, Data Structures & Algorithms, Database Systems, Statistics & Probability, Linear Algebra.

CERTIFICATIONS & LEARNING
- HCIA-AI Certification – Huawei / HCIA (Valid Through Dec 2028)
- AI: Machine Learning & Deep Learning – NAVTTC / Prime Minister's Hunarmand Pakistan Program (In Progress)
- Hugging Face NLP Course – Hugging Face (Self-Study)
"""

OPENROUTER_API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = f"""You are an AI assistant named "Rida's Resume Assistant". Your only knowledge source is the resume of Hafiza Rida Fatima provided below. Answer all user questions exclusively using the information from that resume. If the question cannot be answered from the resume, politely say that the information is not available in the resume and suggest asking about her skills, projects, experience, education, or certifications. Be helpful, concise, and friendly.

RESUME CONTENT:
{RESUME_CONTEXT}"""

@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/api/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return "", 200
    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "Resume Chatbot"
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.3,
        "max_tokens": 500
    }
    try:
        resp = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        if resp.status_code != 200:
            return jsonify({"error": f"AI service error: {resp.status_code}"}), 502
        result = resp.json()
        reply = result["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
