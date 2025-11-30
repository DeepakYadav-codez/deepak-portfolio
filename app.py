from flask import Flask, render_template, request, send_from_directory
import os
import requests
import json

app = Flask(__name__)

# Load API Values from Render Environment
BREVO_API_KEY = os.environ.get("BREVO_API_KEY")
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")

# ------------ ROUTES ------------ #

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/projects")
def projects():
    projects_data = [
        {
            "name": "E-Waste Tracker",
            "description": "AI-powered system to detect & classify e-waste from images and videos.",
            "tech": "Flask, Python, MongoDB, AI"
        },
        {
            "name": "VillageConnect",
            "description": "A digital community platform for rural services & forums.",
            "tech": "Flask, SQL, HTML, CSS"
        }
    ]
    return render_template("projects.html", projects=projects_data)

@app.route("/resume")
def resume():
    return render_template("resume.html")

@app.route("/download")
def download_resume():
    return send_from_directory("resume", "Deepak_Resume.pdf", as_attachment=True)

# ------------ CONTACT FORM (Brevo API) ------------ #

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # Brevo API endpoint
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "accept": "application/json",
            "api-key": BREVO_API_KEY,
            "content-type": "application/json"
        }

        # Email sent TO YOU
        email_to_you = {
            "sender": {"email": EMAIL_SENDER, "name": "Portfolio Contact"},
            "to": [{"email": EMAIL_SENDER}],
            "subject": f"New Message from {name}",
            "htmlContent": f"""
                <h3>New Contact Message</h3>
                <p><b>Name:</b> {name}</p>
                <p><b>Email:</b> {email}</p>
                <p><b>Message:</b><br>{message}</p>
            """
        }

        # Auto Reply to USER
        email_to_user = {
            "sender": {"email": EMAIL_SENDER, "name": "Deepak Portfolio"},
            "to": [{"email": email}],
            "subject": "Thank you for contacting Deepak!",
            "htmlContent": f"""
                Hello {name},<br><br>
                Thank you for your message! I will get back to you soon.<br><br>
                <b>Your Message:</b><br>{message}<br><br>
                Best Regards,<br>Deepak Yadav
            """
        }

        try:
            # Send both emails
            requests.post(url, headers=headers, data=json.dumps(email_to_you))
            requests.post(url, headers=headers, data=json.dumps(email_to_user))

            return render_template("contact.html", success=True)

        except Exception as e:
            print("BREVO API ERROR:", e)
            return render_template("contact.html", error=True)

    return render_template("contact.html")

# ------------ MAIN ------------ #
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
