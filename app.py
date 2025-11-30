from flask import Flask, render_template, request, send_from_directory
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

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


# CONTACT FORM + EMAIL SENDING
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # Email to YOU
        msg_to_you = EmailMessage()
        msg_to_you["Subject"] = "New Contact Message from Portfolio"
        msg_to_you["From"] = EMAIL_USER
        msg_to_you["To"] = EMAIL_USER

        msg_to_you.set_content(f"""
You received a new message from your portfolio website:

Name: {name}
Email: {email}

Message:
{message}
        """)

        # Auto Reply to USER
        msg_to_user = EmailMessage()
        msg_to_user["Subject"] = "Thank you for contacting me!"
        msg_to_user["From"] = EMAIL_USER
        msg_to_user["To"] = email

        msg_to_user.set_content(f"""
Hi {name},

Thank you for reaching out!
I have received your message and I will get back to you shortly.

Your Message:
{message}

Best Regards,
{os.getenv("REPLY_NAME")}
""")

        try:
            # Connect to Gmail SMTP
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_USER, EMAIL_PASS)

                # Send both emails
                smtp.send_message(msg_to_you)
                smtp.send_message(msg_to_user)

            return render_template("contact.html", success=True)

        except Exception as e:
            print("EMAIL ERROR:", e)
            return render_template("contact.html", error=True)

    return render_template("contact.html")



# ------------ MAIN ------------ #
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
