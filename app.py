from flask import Flask, render_template, request, send_file
import os
import requests
import json

app = Flask(__name__)

# ---------------- ENVIRONMENT VARIABLES ---------------- #

BREVO_API_KEY = os.environ.get("BREVO_API_KEY")
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")

# ---------------- ROUTES ---------------- #

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


# ---------------- RESUME DOWNLOAD ---------------- #

@app.route('/download')
def download_resume():
    file_path = os.path.join(app.root_path, "resume", "Deepak_Yadav_Resume.pdf")

    print("Looking for file at:", file_path)

    if not os.path.exists(file_path):
        return "Resume file not found", 404

    return send_file(
        file_path,
        as_attachment=True,
        download_name="Deepak_Yadav_Resume.pdf",
        mimetype="application/pdf"
    )





# ---------------- CONTACT FORM (BREVO API) ---------------- #

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # Brevo API Endpoint
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "accept": "application/json",
            "api-key": BREVO_API_KEY,
            "content-type": "application/json"
        }

        # Mail to YOU
        email_to_you = {
            "sender": {"email": EMAIL_SENDER, "name": "Portfolio Contact"},
            "to": [{"email": EMAIL_SENDER}],
            "subject": f"New Message from {name}",
            "htmlContent": f"""
                <h3>New Contact Form Submission</h3>
                <p><b>Name:</b> {name}</p>
                <p><b>Email:</b> {email}</p>
                <p><b>Message:</b><br>{message}</p>
            """
        }

        # Auto Reply to USER
        email_to_user = {
            "sender": {"email": EMAIL_SENDER, "name": "Deepak Portfolio"},
            "to": [{"email": email}],
            "subject": "Thanks for contacting Deepak!",
            "htmlContent": f"""
                Hello {name},<br><br>
                Thank you for reaching out! I have received your message and will contact you soon.<br><br>
                
                <b>Your Message:</b><br>{message}<br><br>
                
                Best Regards,<br>
                Deepak Yadav
            """
        }

        try:
            # Send emails
            r1 = requests.post(url, headers=headers, data=json.dumps(email_to_you))
            r2 = requests.post(url, headers=headers, data=json.dumps(email_to_user))

            print("YOUR EMAIL STATUS:", r1.status_code, r1.text)
            print("USER EMAIL STATUS:", r2.status_code, r2.text)

            return render_template("contact.html", success=True)

        except Exception as e:
            print("❌ BREVO API ERROR:", e)
            return render_template("contact.html", error=True)

    return render_template("contact.html")


# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
