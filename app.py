from flask import Flask, render_template, request, send_from_directory
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Load SMTP Credentials from Render Environment
SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = os.environ.get("SMTP_PORT")
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_KEY = os.environ.get("SMTP_KEY")
SMTP_SENDER = os.environ.get("SMTP_SENDER")

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

# CONTACT FORM USING BREVO SMTP
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # Email to YOU
        msg = MIMEMultipart()
        msg["From"] = SMTP_SENDER
        msg["To"] = SMTP_SENDER
        msg["Subject"] = f"New Contact Form Message from {name}"

        body = f"""
        Name: {name}
        Email: {email}
        Message:
        {message}
        """
        msg.attach(MIMEText(body, "plain"))

        # Auto Reply to USER
        reply = MIMEMultipart()
        reply["From"] = SMTP_SENDER
        reply["To"] = email
        reply["Subject"] = "Thank you for contacting Deepak!"

        reply.attach(MIMEText(
            f"Hello {name},\n\nThank you for your message!\nI have received it and will get back to you soon.\n\nBest Regards,\nDeepak",
            "plain"
        ))

        try:
            with smtplib.SMTP(SMTP_HOST, int(SMTP_PORT)) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_KEY)

                # send both emails
                server.sendmail(SMTP_SENDER, SMTP_SENDER, msg.as_string())
                server.sendmail(SMTP_SENDER, email, reply.as_string())

            return render_template("contact.html", success=True)

        except Exception as e:
            print("EMAIL ERROR:", e)
            return "Internal Server Error", 500

    return render_template("contact.html")


# ------------ MAIN ------------ #
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
