from flask import Flask, render_template, request
import Final_Decision_Probability as fdp
import CorrectorAndRevise as cr
import activity_grader as ag

app = Flask(__name__)

forumInfo = {}

@app.route("/")
def home():
    return render_template("Cartisius_Tech_WebPage.html")


@app.route("/prediction", methods=["POST"])
def admission_rate_prediction():
    """
    Function binded with the tab College Prediction and Advice

    Return: string
    """

    # Retrieving the parameter values. 
    gpa = request.form["gpa_score"] # parameter name = gpa_score
    sat_eng = request.form["sat_english"] # parameter name = sat_english
    sat_math = request.form["sat_math"] # parameter name = sat_math
    sat_essay = request.form["sat_essay"] # parameter name = sat_essay
    activity_score = request.form["activity_score"] # parameter name = activity_score
    person_statement_score = request.form["personal_statement_score"] # parameter name = personal_statement_score
    residency = request.form["residency"] # parameter name = residency
    race = request.form["race"] # parameter name = race
    gender = request.form["gender"] # parameter name = gender

    # Generating the result
    prediction = fdp.make_prediction(gpa, sat_eng, sat_math, sat_essay, activity_score, person_statement_score, residency, race, gender)

    return prediction

@app.route("/forum", methods=["POST"])
def admission_rate_prediction():
    """
    Function binded with the tab college application forum
    
    Returns
    -------
        String: Indicating the content has been saved or not.
    """
    title = request.form["title"] # parameter name = title
    content = request.form["content"] # parameter name = content
    author = request.form["author"] # parameter name = author

    if title in forumInfo.keys(): # not saving duplicate contents.
        return "Topic already existed"
    else:
        forumInfo[title] = (title, content, author)
        return "Topic saved"


@app.route("/personal_statement", methods=["POST"])
def admission_rate_prediction():
    """
    Function binded with the tab Personal Statement Grading
    
    Returns
    -------
    grade           : String
                Overall grade
    correct_context : String
                content after revising the grammar
    final_context   : String
                Final content that has been revised according to the suggestions
    evaluation      : String
                How well is the personal statement
    suggestion      : String
                Advices to the personal statement
    """

    # Retrieving the file path of the pdf file
    filePath = request.form["pdf_file_path_personal_statement"] # parameter name = pdf_file_path_personal_statement

    # Generating suggestions
    grade, correct_context, final_context, evaluation, suggestion = cr.correct_and_revise(filePath)

    return (str(grade), correct_context, final_context, evaluation, suggestion)

@app.route("/activity", methods=["POST"])
def admission_rate_prediction():
    """
    Function binded with the tab Activity Grading
    
    Returns
    -------
    grade        : String
                Overall grade
    suggestion   : String
                Suggestions to the activity content.
    """

    # Retrieving the file path of the pdf file
    filePath = request.form["pdf_file_path_activity"] # parameter name = pdf_file_path_activity

    # Generating suggestions
    grade, suggestion = ag.grade_activity(filePath)

    return (grade, suggestion)


if __name__ == "__main__":
    app.run()
