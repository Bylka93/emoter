# Emoter / Emote

Last updated on May 20, 2017

Here's a link to the Medium post about the development of Emoter throughout my undergrad senior year:

"How to Make a Digital Personality of Yourself Using Chatbots, Facebook, and Empathy"

https://medium.com/@johnnyfived/how-to-make-a-digital-personality-of-yourself-using-chatbots-facebook-and-empathy-8b0c53afa9bd

This repository contains the full source code for a sentiment analyzer library called Emote, and its companion program Emoter, a chatbot library intergrated with Emote that allows it to empathize with the users talking to it. Emote is based off TextBlob's (NLTK's) naive Bayes probability system, and is able to detect reasonably accurate values for 3-6 different emotional tones, from 26 (36 eventually) classifications. Emoter chatbot agents use Emote to analyze user messages, then choose an emotionally appropriate response from interchangable "conversations", based around designed personalities / personas. Emoter includes a      (mostly) automated way of parsing downloaded Facebook messages to build a text corpus off an individual person's Facebook profile. This project developed for my undergraduate thesis at Parsons School of Design.


## Note

Emote / Emoter are open-sourced under the MIT License.

### Screenshots

Emoter bot built with my own personality by using my Facebook messages for its corpus.
<img src="/screenshots/emoter-fb-johnny-demo-web.gif?raw=true" width="680px" />

<img src="/screenshots/emote-demo-1.png?raw=true" width="350px" />

<img src="/screenshots/emote-demo-4.png?raw=true" width="600px" />

<img src="/screenshots/emoter_demo_5.png?raw=true" width="600px" />

### Prerequisites

* Windows / Mac (Untested on Linux)
* Python 3.5 or higher
* Pip / virtual environments (Pip not required if installing via setup.py)


## Introduction

Emote uses the TextBlob / NLTK, NumPy, SciPy, pandas, and scikit-learn libraries to build a probabilistic sentiment analyzer for 26 different classifications. These classifications have been divided into 13 pairs of opposites, and are designed to be grouped together to create tone clusters that can then encompass more values as well as decrease false positives. Based off these tone clusters, a further 10 additional tone classifications are derived.

Emoter is a basic but functional chatbot library intergrated with Emote, in order to give chatbot agents the ability to empathize with users and give back emotionally appropriate responses. Emoter agents thus can operate on a "higher level of thinking", by first categorizing messages and then choosing specific, interchangable "conversations" (lists of text responses) to respond from based on certain emotional tones. Within these conversations, Emoter looks for matching text in its database and compares it with the user input on a sliding threshold, outputting the corresponding response if the threshold is met. 

Both Emote and Emoter can be run offline. While Emoter's responses are completely pre-written as of now, plans for developing an "improvisation" feature through using Markov chains and / or a neural network is in the works.


### Full List of Emotional Tone Classifications

```
Positive, negative; love, hate; joy, anger; certainty, confusion; amusement, boredom; intensity, regret; challenging, agreeable; desire, calm; sarcastic, emphatic; instructive, accusative; admiration, inquisitive; modest, pride; ambivalence, vulgarity
```

```
10 additional tones can be derived from the 26 base tones through combining associations: obedience, assertiveness; attraction, disgust; informative, malevolent; anxiety, excitement; hopeful, horror.
```


### Installing

Once you create your virtual environment, run the setup file or install the dependencies via pip. 

All packages should install fine, but on Windows and Mac (and possibly Linux? ha), for NumPy and SciPy, you will need to manually download the packages with mkl, here:

[http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy](http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy)

[http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy](http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy)

In command line or Terminal, cd to the directory where the whl files are, and run this command and install both packages:
```
pip install package_name.whl
```

Then, download the necessary corpus to use TextBlob:
```
python -m textblob.download_corpora
```
Because GitHub has a file upload limitation, and to save space, I've uploaded a pickled version of the probability classifier, so that it doesn't have to rebuild every time Emote is reloaded. 

Now download the pickled classifier file (so the data doesn't have to be re-trained every time).

[http://www.mediafire.com/file/c18ll802ynb7s3c/base_corpus.pickle](http://www.mediafire.com/file/c18ll802ynb7s3c/base_corpus.pickle)

<!-- http://www.mediafire.com/file/c18ll802ynb7s3c/base_corpus.pickle -->

Put the pickle file in the /data directory of Emoter / Emote, or build the pickled file yourself with your own custom database automatically by running emote.py.

Now you can use both Emote and Emoter libraries.

## Using Emote (Sentiment Analysis)

Emote can be run as a script with a CLI, or imported as a module / library. Run_emote.py starts Emote's web app interface, where you can demo the sentiment analysis and mass analyze CSV files. Emoter_trainer_wrapper.py offers a more advanced CLI for Emote, and is meant to be used to train and test Emote's database, but is not functional yet. When you're running Emote for the first time, it'll automatically analyze an empty message, so that the initial loading of the classifier is done (the initial loading takes longer to load).

Start by importing emote.
```
import emote as emote
```
Send text message to be analyzed.
```
em = emote.Emote()
message = "Duct tape. I need it for... taping something."
result = em.runAnalysis(message)
```
You will get a list of tuples of all the emotional tone values in descending order as a result:
```
[('desire', 100.0), ('emphatic', 14.7), ('certainty', 9.6), ('challenging', 5.0), ('agreeable', 3.1), ('instructive', 2.4), ('intensity', 2.3), ('accusative', 2.0), ('anger', 1.4000000000000001), ('inquisitive', 0.7000000000000001), ('confusion', 0.4), ('hate', 0.1), ('negative', 0.0), ('calm', -0.0), ('regret', -0.0), ('modest', -0.1), ('vulgarity', -0.1), ('pride', -0.1), ('love', -0.1), ('positive', -0.1), ('amusement', -0.1), ('joy', -0.1), ('admiration', -0.1), ('sarcastic', -0.1), ('boredom', -0.1), ('ambivalence', -0.1)]
```
You can get values from the result like this:
```
result[0][0]
```
returns the strongest tone classification-value pair:
```
('desire', 100.0)
```
and
```
result[0][0][0]
```
returns the strongest tone classification:
```
'desire'
```
while
```
result[0][0][1]
```
returns the strongest tone value:
```
100.0
```
And so
```
result[0][1]
```
returns the 2nd strongest tone classification-value pair:
```
('emphatic', 14.7)
```
and so on for all 26 base tones, in descending order of value. Eventually, the API will be expanded to return more data like a descriptive psychological analysis, hence why the result is returned as a list.

To use Emote's web interface and mass analyzer feature (for CSV data input / output), start run_emoter.py, and go to localhost:5000 in your browser:

<img src="/screenshots/emote-web-demo-1.png?raw=true" width="600px" />

<img src="/screenshots/emote-web-demo-2.png?raw=true" width="600px" />

## Using Emoter (Chatbot)

Emoter can be run as a script with a CLI, or used as a module / library in Python. By default, Emoter's corpus consists of example texts for a virtual fitness coach / trainer. To customize or make your own chatbot, you can add a new 'brain' in the /data folder, using the 'fitness_coach' files as a template. Emoter brains currently consist of a folder of text files comprised of tuples (eventually, the brains will use SQL).

Start by importing emoter.
```
import emoter as emt
```
Send a message for the bot to analyze and respond to..
```
emtBot = emt.Emoter()
message = "Hey there, how are you?"
result = emtBot.getMsg(message)
```
You will get a string returned with Emoter's matching response statement to your message.
```
print(result)
Hello! Yes, I'm here! How can I help you?
```

This is what the dir structure for an Emoter bot corpus looks like (example corpus, 'fitness_coach', which loads by default):

<img src="/screenshots/emoter-corpus-template-structure.png?raw=true" width="600px" />

Fitness_coach brain working in action.

<img src="/screenshots/emoter_demo_3.png?raw=true" width="600px" />

You can follow the tone of the fitness_coach brain files to determine how to appropriately divide up your dialog to work best with Emoter's 'empathy.' Soon, there will be an automatic texts parser / trainer (emoter_corpus_fb_parser.py) that creates the new files and templates required for a full conversation corpus through a command line interface, from Facebook message archives. This will effectively create a brain, or persona, of an actual person through their Facebook messages.

To load a different, stored corpus in the same Emoter instance, you must have all the necessary text files to build the corpus, in a folder within /data. Pass the exact name of the folder name as the single parameter for Emoter(brain_path).

```
import emoter as emt
emtBot = emt.Emoter(brain_path="custom_bot_name")
emtBot.getMsg("hello emoter")
```
To train an existing Emoter with a new brain (must be located within /data:

```
new_brain_path = different_virtual_assistant
emtBot.trainDatabase(new_brain_path)

```

To call Emote's functions through Emoter..

```
import emoter
emt = emoter.Emoter()
message = "Enter your own message here to be analyzed."
emt.em.runAnalysis(message)
[('instructive', 100.0), ('desire', 77.10000000000001), ('agreeable', 16.6), ('calm', 5.4), ('certainty', 5.2), ('challenging', 4.2), ('emphatic', 3.5000000000000004), ('intensity', 1.3), ('inquisitive', 0.8), ('accusative', 0.8), ('anger', 0.6), ('confusion', 0.4), ('vulgarity', -0.0), ('amusement', -0.0), ('admiration', -0.0), ('regret', -0.0), ('positive', -0.0), ('love', -0.0), ('sarcastic', -0.0), ('pride', -0.0), ('hate', 0.0), ('modest', -0.0), ('boredom', -0.0), ('negative', -0.0), ('joy', -0.0), ('ambivalence', -0.0)]
```

To use Emoter's web interface (which was built for an art exhibit to be displayed on a CRT monitor, hence the aesthetics), start run_emoter.py, and go to localhost:5000 in your browser:

<img src="/screenshots/emoter-web-demo-1.png?raw=true" width="600px" />

<img src="/screenshots/emoter-web-demo-2.png?raw=true" width="600px" />


## Generating an Emoter corpus from Facebook messages


First of all, this system does not work especially well, and is pretty hacked together. Follow at your own caution.

Go here to download your Facebook archive:
[https://www.facebook.com/help/131112897028467](https://www.facebook.com/help/131112897028467).

Then, use the Facebook Chart Archive Parser tool, which can be downloaded here:
[https://github.com/ownaginatious/fbchat-archive-parser](https://github.com/ownaginatious/fbchat-archive-parser).


Running fbchat-archive-parser will give you a CSV file with data formatted into these columns: ['thread'], ['sender'], ['date'], and ['message']. Save or rename this CSV file as "msg_csv.csv", and store it into the root folder of Emoter.

Running 'emoter_corpus_fb_parser.py' allows you to enter in the full name of the Facebook user to automatically parse and generate a usable Emoter corpus, after the initial parsing with fbchat-archive-parser. To create a corpus off a single individual profile, only responses said by the specified user directly after an 'other' user message are counted.

The end result will give you a text file with the generated Facebook corpus, output as "final_msgs.txt", which is currently NOT a usable file. I was unable to parse the lines from the text file without getting Unicode decoding errors. To circumvent this and obtain an actually working corpus, you have to open the final SQL database generated, "new_msgs_db.db", into the program DB Browser for SQLite ([http://sqlitebrowser.org](http://sqlitebrowser.org)). Once you have the final table with all the information open in DB Browser, select all the message-pair responses in the database, and copy and paste it into a text file. Every line should contain the message, in quotes, followed by a single tab ("\t"), and the response, also in quotes. 

See the below image for to see all the new files generated you should have in your directory now. 
<img src="/screenshots/facebook_corpus_files.png?raw=true" width="600px" />

Opening "new_msgs_db.db" should give you a data set with two columns: 'other' and 'profile'.
<img src="/screenshots/facebook_corpus_db_final.png?raw=true" width="300px" />

Select the entirety of the database in DB Browser, and copy and paste the contents into the texts_all.txt file in Emoter's corpus (make sure to put it in a separate brain folder, and specify the path name of the brain).

See the below image for an example of the format of the final corpus you should have, in texts_all.txt.
<img src="/screenshots/facebook_corpus_parsed.png?raw=true" width="600px" />

Right now, there is no automated classification of the the Facebook corpus to be used in Emoter's empathy. You currently can only do that manually.

### Training / Adding Your Own Emote Corpus

Follow this quick visual guide to understand how the base corpus has been trained.

<img src="/docs/emote-training-database-description.png?raw=true" width="600px" />

Also, see the file 'alice_classification_training_sample.txt' to see passages from Alice in Wonderland classified through with Emote's tones.

Right now, you have to copy and paste all the training data (structured as tuples) into the list varible 'self.train' in emote.py, if you are building your own corpus or expanding the base knowledge. Taking in the tuples from a text file was giving me unicode errors; must fix this later. 

### Current Limitations

* System for deriving 10 additional tones from base 26 has not yet been implemented
* Database is too young (<8000 classifications) to be consistently accurate
* Emoter agents are only deployable in Python
* Emoter agents have no ability to remember or learn new things
* Emoter agents only search for one matching database, not multiple. If the threshold fails, then Emoter will just search the entire database.
* Conversations / texts are just lists of tuples, which is too limiting of a data structure
* No automated way of training Facebook database for Emoter's empathetic functionality

### Future Plans

* Functionality to automatically load interchangable databases / corpuses (Pickled files) to narrow down contexts in Emote
* Add an "improvisation" feature for Emoter agents to build new dialog through Markov chains and / or neural networks
* Incorporate machine learning and accuracy testing into Emote's database
* Develop automated way of training databases (described in architecture flowchart in /docs)
* Build out a full RESTful API for Emote, and offer plans for developers / businesses for API calls via Emoter website
* Develop a GUI web interface to create / customize Emoter chatbot agents
* Fix database matching to multiple (going in descending order) instead of just one
* Rework conversations / texts data structure into SQL, with added frequency / weight values for more complexity
* Implement short-term memory functionality for Emoter agents
* Improve sequence matching by incorporating automatic addition of synonyms for words and phrases
* Build a Unity SDK for Emote / Emoter
* Incorporation with speech recognition and speech synthesis
* Incorporation with computer vision

## Deployment

Eventually, an RESTful API will be developed through Flask for both Emote and Emoter.


<!-- ## Contributing -->

<!-- Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us. -->
<!-- ## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).  -->


## Authors

* **Johnny Dunn** - *Initial work* - [jddunn](https://github.com/jddunn)
* **Shubhank Sahay** - *Personas Development for Emoter - Fitness Coach; Corpus training contributions*

Other thanks:

Kyle Li — Sven Travis — Brad McDonald — Ernesto Klarr
Han Shen Chen — Wei Wei — Benjamin Norskov
Gentry Demchak — John Delguidice — Nicholas Elia
Andrew Benson — Kate Wallace — Danny Dang — Alex Addington-White 
Jasmine Martinez — Rafael Alam — Shiqi Shen — Yumeng Wang
Yi Tang — Adam McBride — Elizabeth Peralta — Enayet Kabir
Keiji Kimura — Kim Carl Daniel Koehler — Orien Longo — Willie Quiroz
Nicole Shin Tong Shi — Marco Weibel— Aidain Kaye — Daniel Kaye
John Sharpe — Nicholas Fortugno — Michael Wolf — Ayo Okunseinde
Anthony Marefat — Lucy Matchett — Alexandra Tosti


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


## References

[https://cloud.google.com/prediction/docs/sentiment_analysis](https://cloud.google.com/prediction/docs/sentiment_analysis)

[http://venturebeat.com/2016/08/21/how-higher-emotional-intelligence-will-help-chatbots/](http://venturebeat.com/2016/08/21/how-higher-emotional-intelligence-will-help-chatbots/)

[https://www.theguardian.com/technology/2016/oct/26/black-mirror-episode-playtest-predicted-future-video-games-augmented-reality/](https://www.theguardian.com/technology/2016/oct/26/black-mirror-episode-playtest-predicted-future-video-games-augmented-reality/)

[https://www.theguardian.com/technology/2016/oct/12/video-game-characters-emotional-ai-developers/](https://www.theguardian.com/technology/2016/oct/12/video-game-characters-emotional-ai-developers/)

[https://www.researchgate.net/publication/306091953_A_Meta-Framework_for_Modeling_the_Human_Reading_Process_in_Sentiment_Analysis/](https://www.researchgate.net/publication/306091953_A_Meta-Framework_for_Modeling_the_Human_Reading_Process_in_Sentiment_Analysis/)

[https://www.researchgate.net/publication/308401450_A_Novel_Approach_to_Big_Data_Veracity_using_Crowdsourcing_Techniques_and_Bayesian_Predictors/](https://www.researchgate.net/publication/308401450_A_Novel_Approach_to_Big_Data_Veracity_using_Crowdsourcing_Techniques_and_Bayesian_Predictors/)

[https://www.researchgate.net/publication/308017468_Domain-specific_sentiment_classification_via_fusing_sentiment_knowledge_from_multiple_sources/](https://www.researchgate.net/publication/308017468_Domain-specific_sentiment_classification_via_fusing_sentiment_knowledge_from_multiple_sources/)

[http://www.julianjaynes.org/evidence_summary.php/](http://www.julianjaynes.org/evidence_summary.php/)

## Credits

* TextBlob
* NLTK
* NumPy / SciPy
* scikit-learn
* Flask
* MetroUI (for HTML / CSS template)
