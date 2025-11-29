from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

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
            "tech": "Flask, Python, MongoDB, AI",
            "link": "#"
        },
        {
            "name": "VillageConnect",
            "description": "A digital community platform for rural services & forums.",
            "tech": "Flask, SQL, HTML, CSS",
            "link": "#"
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


# CONTACT FORM
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        print("\n--- NEW CONTACT MESSAGE ---")
        print("Name:", name)
        print("Email:", email)
        print("Message:", message)
        print("--------------------------------\n")

        return render_template("contact.html", success=True)

    return render_template("contact.html")


# ------------ MAIN ------------ #
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
