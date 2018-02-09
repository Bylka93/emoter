from flask import Flask, jsonify, request, render_template, abort, redirect, url_for, current_app, send_from_directory
from werkzeug.utils import secure_filename

import emote

UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

em = emote.Emote()

firstTime = True

@app.route("/api/sentiment/<string:text_input>", methods=['GET'])
def get_sentiment(text_input):
    em.getInput(text_input)  # Polarity score
    sentiment = em.normalizedProbValues
    return jsonify({"result": sentiment})


@app.route("/api/sentiment/sentences/<string:text_input>", methods=['GET'])
def get_sentences_sentiment(text_input):
    em.split_into_sentences(text_input)
    sentencesResults = em.sentencesProbValues
    sentencesText = em.sentences
    sentencesResultsFinal = dict(zip(sentencesText, sentencesResults))
    # sentencesResults = [{"sentence": s, "sentiment": emote_trainer_wrapper.massResults[t]} for s, t in emote_trainer_wrapper.sentences]
    return jsonify({"results": sentencesResultsFinal})


@app.route("/app/sentiment", methods=['POST'])
def sentiment():
    text = get_text(request)
    em.getInput(text)  # Polarity score
    sentiment = em.normalizedProbValues
    return jsonify({"result": sentiment})


@app.route("/app/sentiment/sentences", methods=['POST'])
def sentences_sentiment():
    text = get_text(request)
    em.split_into_sentences(text)
    sentencesResults = em.sentencesProbValues
    sentencesText = em.sentences
    sentencesResultsFinal = dict(zip(sentencesText, sentencesResults))
    # sentencesResults = [{"sentence": s, "sentiment": emote_trainer_wrapper.massResults[t]} for s, t in emote_trainer_wrapper.sentences]
    return jsonify({"results": sentencesResultsFinal})


def get_text(req):
    '''Get the text from the request.'''
    if req.form:
        return req.form['text']
    elif req.headers['Content-Type'] == 'application/json':
        return req.json['text']
    else:
        abort(404)


##### Views #####
@app.route("/")
def home():
    global firstTime
    if firstTime:
        firstTime = False
        # Runs Emote for the first time to load the initial pickled data (first time analysis is always slower)
        em.getInput("")
    else:
        pass
    return current_app.send_static_file('templates/emote-home.html')


# Upload CSV for Emote mass analysis
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return current_app.send_static_file('templates/emote-home.html')
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(filename)
            em.analyzeCSV(filename)
            return redirect(url_for('static',
                                    filename="results.csv"))


@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               "results.csv")


@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)