# Genzie
# A social network powered 

#!/usr/bin/env python
from flask import Flask, jsonify, request, render_template, abort, redirect, url_for, current_app
import emoter
from flask import send_from_directory

app = Flask(__name__)

emt = emoter.Emoter(brain_path="fitness_coach")

firstTime = True

@app.route("/chat", methods=['GET', 'POST'])
def giveResponse():
    text_input = request.form['text_input']
    res = emt.getMsg(text_input)
    print("\n\t", res)
    return jsonify(res=res)


@app.route("/")
def home():
    # global firstTime
    # if firstTime:
        # firstTime = False
        # Runs Emote to load the initial pickled data (first time analysis is always slower), before loading the page
        # emt.getMsg("")
    # return render_template("templates/emoter-home.html")
    return current_app.send_static_file('templates/emoter-home.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')