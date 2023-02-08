from flask import Flask, render_template, request
import threading

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        character = request.form.get("character")
        artifact_set = request.form.get("artifact_set")
        weapon = request.form.get("weapon")
        if request.form.get("update"):
            return 1
        elif request.form.get("run_simulation"):
            return 2
        return render_template("index.html", character=character, artifact_set=artifact_set, weapon=weapon)
    else:
        return 1

if __name__ == "__main__":
    app.run()