from flask import Flask, render_template, request
import Final_Decision_Probability as fdp

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("Cartisius_Tech_WebPage.html")

@app.route("/", methods=["POST"])
def process():
    action = request.form.get("action")

    if action == "prediction":
        sat_gpa = request.form["sat-gpa"].split()
        sat_english, sat_math = int(sat_gpa[0]) // 2, int(sat_gpa[0]) // 2
        gpa = int(sat_gpa[1])
        activity = int(request.form['extracurricular-activities'])
        personal_statement = int(request.form['personal-statement'])
        print(fdp.make_prediction(gpa, sat_english, sat_math, activity, personal_statement))
        return fdp.make_prediction(gpa, sat_english, sat_math, activity, personal_statement)
    elif action == "advice":
        print(2)
    elif action == "forum":
        print(3)
    elif action == "grading":
        print(4)


if __name__ == "__main__":
    app.run()
