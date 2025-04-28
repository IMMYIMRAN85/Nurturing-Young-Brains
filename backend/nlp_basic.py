import json
import re
import datetime
from flask import Flask
from flask_mail import Mail, Message
from transformers import pipeline

# Load sentiment-analysis pipeline (pretrained)
nlp_model = pipeline("sentiment-analysis")

# List of simple bad words
bad_words = ["bad", "stupid", "hate", "violence", "idiot", "kill", "hurt"]

# Paths
COMMENTS_FILE = 'backend/model/comments.json'
DANGEROUS_FILE = 'backend/model/dangerous_comments.json'
SUMMARY_FILE = 'backend/model/summary.txt'
FULL_LOG_FILE = 'backend/model/full_comments_log.json'

# Flask app for sending emails
app = Flask(__name__)

# Email Configuration
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='pandibaaz@gmail.com',  # <-- your Gmail address here
    MAIL_PASSWORD='rdyo xymg zwut yrmv'    # <-- your Gmail password or App Password here
)

mail = Mail(app)

# Function to load comments
def load_comments():
    try:
        with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['comments']
    except Exception as e:
        print("Error loading comments:", e)
        return []

# Function to save full log
def save_full_log(all_comments_log):
    try:
        with open(FULL_LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump({"log": all_comments_log}, f, ensure_ascii=False, indent=4)
        print(f"\n📚 Full comments log saved to '{FULL_LOG_FILE}'.")
    except Exception as e:
        print("Error saving full comments log:", e)

# Function to append the summary
def save_summary(dangerous_count):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(SUMMARY_FILE, 'a', encoding='utf-8') as f:
            f.write("\n--------------------------------------\n")
            f.write(f"Summary (Generated on {now})\n")
            if dangerous_count > 0:
                f.write(f"⚠️ {dangerous_count} dangerous comments detected and saved.\n")
            else:
                f.write("✅ No dangerous comments detected. Nothing to save.\n")
            f.write("--------------------------------------\n")
        print(f"\n📝 Summary appended to '{SUMMARY_FILE}'.")
    except Exception as e:
        print("Error saving summary:", e)

# Function to send email alert
def send_alert_email(comment_text, bad_words):
    try:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with app.app_context():  # <-- This line is very important
            msg = Message(
                subject="🚨 Alert: Dangerous Comment Detected",
                sender=app.config['MAIL_USERNAME'],
                recipients=['imran385@outlook.com'],  # <-- your receiver
                body=f"""
Dear Parent,

A potentially harmful comment has been detected:

Comment: "{comment_text}"
Bad words found: {bad_words}

Detected on: {now}

Please review your child's online activity.

Regards,
Nurturing & Protecting Young Brains Team
"""
            )
            mail.send(msg)
            print("✅ Alert email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to check comments
def check_comments(comments):
    dangerous_comments = []
    all_comments_log = []

    for idx, comment in enumerate(comments, start=1):
        try:
            # Use the BERT model to predict sentiment
            result = nlp_model(comment)[0]
            label = result['label']  # Either 'POSITIVE' or 'NEGATIVE'
            score = result['score']  # Confidence score

            if label == 'NEGATIVE':
                # Dangerous Comment Detected
                print(f"[DANGEROUS] Comment {idx}: {comment}")
                print(f"    🔥 Model Prediction: {label} (Confidence: {score:.2f})")
                dangerous_comments.append({
                    "comment": comment,
                    "model_prediction": label,
                    "confidence": float(score)
                })
                all_comments_log.append({
                    "comment": comment,
                    "status": "DANGEROUS",
                    "model_prediction": label,
                    "confidence": float(score)
                })
                # Send alert email
                send_alert_email(comment, label)
            else:
                # Safe Comment
                print(f"[SAFE] Comment {idx}: {comment}")
                print(f"    ✅ Model Prediction: {label} (Confidence: {score:.2f})")
                all_comments_log.append({
                    "comment": comment,
                    "status": "SAFE",
                    "model_prediction": label,
                    "confidence": float(score)
                })
        except Exception as e:
            print(f"Error analyzing comment {idx}: {e}")

    # Save dangerous comments if any
    if dangerous_comments:
        try:
            with open(DANGEROUS_FILE, 'w', encoding='utf-8') as f:
                json.dump({"dangerous_comments": dangerous_comments}, f, ensure_ascii=False, indent=4)
            print(f"\n⚠️ Saved {len(dangerous_comments)} dangerous comments to '{DANGEROUS_FILE}'.")
        except Exception as e:
            print("Error saving dangerous comments:", e)

    # Save full log and summary
    save_full_log(all_comments_log)
    save_summary(len(dangerous_comments))


# Main execution
if __name__ == "__main__":
    comments = load_comments()
    if comments:
        check_comments(comments)
    else:
        print("No comments found or failed to load!")



