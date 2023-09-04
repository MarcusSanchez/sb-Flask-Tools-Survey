from flask import Flask, render_template, flash, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "OhSoSecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []


@app.route("/")
def home():
    return render_template("start.html", survey=survey)


@app.route("/answer", methods=["POST"])
def route_answer():
    choice = request.form['answer']
    responses.append(choice)
    if len(responses) == len(survey.questions):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:qid>")
def route_question(qid):
    if responses is None:
        return redirect("/")
    if len(responses) == len(survey.questions):
        return redirect("/complete")
    if len(responses) != qid:
        flash("Redirected to question " + str(len(responses) + 1))
        return render_template("question.html",
                               question_num=len(responses),
                               question=survey.questions[len(responses)],
                               tomfoolery=True
                               )

    if qid > len(survey.questions):
        return redirect("/complete")

    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)


@app.route("/complete")
def route_complete():
    return render_template("thanks.html")


if __name__ == "__main__":
    app.run()
