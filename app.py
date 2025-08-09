
from flask import Flask, request, render_template
from utils import extract_discount_code, calculate_penalty
from datetime import datetime
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    discount_code = None
    if request.method == "POST":
        start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d")
        plan = request.form["plan"]

        pdf_file = request.files["pdf"]
        if pdf_file:
            filepath = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
            pdf_file.save(filepath)
            discount_code = extract_discount_code(filepath)

        used_days = (end_date - start_date).days
        penalty = calculate_penalty(plan, used_days)
        result = {
            "used_days": used_days,
            "penalty": penalty,
            "plan": plan,
            "code": discount_code
        }
    return render_template("index.html", result=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


