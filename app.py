import os
import numpy as np
import cv2
import sqlite3
from flask import Flask, render_template, request, redirect
from tensorflow.keras.models import load_model

# Initialize Flask App
app = Flask(__name__)

# Define Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
DB_PATH = os.path.join(BASE_DIR, "database.db")
MODEL_PATH = os.path.join(BASE_DIR, "ai_model", "model.h5")  # Relative path to AI model

# Initialize Database
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image BLOB,
                status TEXT
            )
        ''')
        conn.commit()

# Call Database Initialization
init_db()

# Load AI Model
try:
    model = load_model(MODEL_PATH)
    print("✅ AI Model Loaded Successfully!")
except Exception as e:
    print(f"❌ Error Loading Model: {e}")

# Function to Verify Image
def verify_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (64, 64))
    img = img / 255.0
    prediction = model.predict(np.expand_dims(img, axis=0))
    return "Valid Complaint" if prediction[0][0] > 0.5 else "Spam"

# Route for Complaint Submission
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        image = request.files["image"]
        image_path = os.path.join(BASE_DIR, "static", image.filename)  # Store image in /static folder
        image.save(image_path)

        status = verify_image(image_path)

        # Save to Database
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO complaints (image, status) VALUES (?, ?)", (image.read(), status))
                conn.commit()
                print("✅ Complaint Saved Successfully!")
        except Exception as e:
            print(f"❌ Database Error: {e}")

        return redirect("/")

    return render_template("index.html")

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
