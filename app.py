from flask import Flask, render_template, request, send_from_directory
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

app = Flask(__name__)

# Load Brevo SMTP Credentials from Render Environment Variables
SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = os.environ.get("SMTP_PORT")
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_KEY = os.environ.get("SMTP_KEY")
SMTP_SENDER = os.environ.get("SMTP_SENDER")
SMTP_NAME = os.environ.get("SMTP_NAME")  # Optional - for reply name


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


# DOWNLOAD RESUME
@app.route("/download")
def download_resume():
    return send_from_directory("resume", "Deepak_Resume.pdf", as_attachment=True)


# ------------ CONTACT FORM (Brevo SMTP) ------------ #
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
        New Contact Form Message:

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

        reply_body = f"""
Hello {name},

Thank you for contacting me!
I have received your message and I will get back to you shortly.

Your Message:
{message}

Best Regards,
{SMTP_NAME}
        """

        reply.attach(MIMEText(reply_body, "plain"))

        try:
            # Secure TLS context
            context = ssl.create_default_context()

            # Connect to Brevo SMTP
            with smtplib.SMTP(SMTP_HOST, int(SMTP_PORT)) as server:
                server.starttls(context=context)
                server.login(SMTP_USER, SMTP_KEY)

                # Send emails
                server.sendmail(SMTP_SENDER, SMTP_SENDER, msg.as_string())
                server.sendmail(SMTP_SENDER, email, reply.as_string())

            return render_template("contact.html", success=True)

        except Exception as e:
            print("EMAIL ERROR:", e)
            return render_template("contact.html", error=True)

    return render_template("contact.html")


# ------------ MAIN ------------ #
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
