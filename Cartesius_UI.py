from flask import Flask, render_template, request, jsonify
import Final_Decision_Probability as fdp
import CorrectorAndRevise as cr
import activity_grader as ag

app = Flask(__name__)

forumInfo = {}

gender_dict = {"Male": 2.0, 
               "Female": 0.0, 
               "Transgender": 1.0}

race_dict = {"Hispanic": 4.0, 
             "Asian": 2.0, 
             "White": 7.0, 
             "International": 5.0,
             "Domestic Unknown": 3.0, 
             "African American": 0.0, 
             "Pacific Islander": 6.0, 
             "American Indian": 1.0
             }

residency_dict = {"CA resident": 0.0, 
                  "Internation": 1.0, 
                  "Non-resident domestic": 2.0, 
                  "unknown": 3.0}

@app.route("/")
def home():
    return render_template("Cartisius_Tech_WebPage.html")


@app.route("/prediction", methods=["POST"])
def admission_rate_prediction():
    """
    Function binded with the tab College Prediction and Advice

    Return: string
    """
    data = request.get_json()
    # Retrieving the parameter values. 
    gpa = float(data["gpa_score"]) # parameter name = gpa_score
    sat_eng = int(data["sat_english"]) # parameter name = sat_english
    sat_math = int(data["sat_math"]) # parameter name = sat_math
    sat_essay = int(data["sat_essay"]) # parameter name = sat_essay
    activity_score = int(data["activity_score"]) # parameter name = activity_score
    personal_statement_score = int(data["personal_statement_score"]) # parameter name = personal_statement_score
    residency = data["residency"] # parameter name = residency
    race = data["race"] # parameter name = race
    gender = data["gender"] # parameter name = gender

    # Generating the result
    print((gpa, sat_eng, sat_math, sat_essay, activity_score, personal_statement_score, residency_dict[residency], race_dict[race], gender_dict[gender]))
    prediction = fdp.make_prediction(gpa, sat_eng, sat_math, sat_essay, activity_score, personal_statement_score, residency_dict[residency], race_dict[race], gender_dict[gender])

    return prediction

@app.route("/forum", methods=["POST"])
def college_application_forum():
    """
    Function binded with the tab college application forum
    
    Returns
    -------
        String: Indicating the content has been saved or not.
    """

    data = request.get_json()
    title = data["title"]
    content = data["content"]
    author = data["author"]

    if title in forumInfo.keys(): # not saving duplicate contents.
        return "Topic already existed"
    else:
        forumInfo[title] = (title, content, author)
        return "Topic saved"


@app.route("/personal_statement", methods=["POST"])
def personal_statement_grading():
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

    # # Retrieving the file path of the pdf file
    data = request.get_json()
    filePath = data["pdf_file_path_personal_statement"] # parameter name = pdf_file_path_personal_statement

    # Generating suggestions
    grade, correct_context, final_context, evaluation, suggestion = cr.correct_and_revise(filePath)

    result = {"grade": str(grade), 
              "correct_context": correct_context, 
              "final_context": final_context, 
              "evaluation": evaluation, 
              "suggestion": suggestion}
    
    return jsonify(result)

@app.route("/activity", methods=["POST"])
def activity_grading():
    """
    Function binded with the tab Activity Grading
    
    Returns
    -------
    grade        : String
                Overall grade
    suggestion   : String
                Suggestions to the activity content.
    """

    # # Retrieving the file path of the pdf file
    data = request.get_json()
    filePath = data["pdf_file_path_activity"] # parameter name = pdf_file_path_activity

    # Generating suggestions
    grade, suggestion = ag.grade_activity(filePath)

    result = {"grade": str(grade), 
              "suggestion": suggestion}

    return jsonify(result)


if __name__ == "__main__":
    app.run(port=9090)
