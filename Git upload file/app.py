from flask import Flask, render_template, request, redirect, url_for
from github import Github
import os
import time

app = Flask(__name__)

# Replace with your GitHub credentials
GITHUB_TOKEN = "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"  # Generate a personal access token

# Initialize GitHub API
github = Github(GITHUB_TOKEN)
USERNAME = 'admin'
PASSWORD = 'abc'
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        # Here, you can add actual authentication logic
        if username == USERNAME and password == PASSWORD:
           return redirect(url_for("upload"))
        else:
            return render_template('login.html')
    return render_template('login.html')

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        comment = request.form['comment']
        if file:
            timestamp = str(int(time.time()))  # Unix timestamp as filename
            filename = timestamp + ".sql" #+ file.filename
            file.save(filename)

            # Upload to GitHub
            repo = github.get_repo("MapplesoftAccount/parisMysql")  # Replace with your GitHub username and repository name
            with open(filename, "rb") as f:
                content = f.read()
                commit_message = f"Uploaded at {timestamp}\n\nComment: {comment}"
                repo.create_file(filename, f"Upload {filename}", content)

            os.remove(filename)  # Remove the uploaded file
            return "File uploaded and saved in GitHub repository."
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
