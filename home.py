from flask import Flask, render_template, request
import threading

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        character = request.form.get("character")
        artifact_set = request.form.get("artifact_set")
        weapon = request.form.get("weapon")
        if request.form.get("update"):
            # Code to generate the Character object and run 'MakeScoreFunction()' and 'MakeArtifactSetRanking()'
            pass
        elif request.form.get("run_simulation"):
            # Code to run the simulation with multithreading
            pass

    return render_template("home.html")

if __name__ == "__main__":
    app.run()