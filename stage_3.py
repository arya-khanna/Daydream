import spacy
import nltk.corpus
from nltk.corpus import nps_chat
from nltk.tokenize import TweetTokenizer
from textblob import TextBlob
import time
import os

# downloading everything from header, mainly file_limit
from header import*

q_words = ['what', 'where', 'when','how','why','did','do','does','have','has','am','is','are','can','could','may','would','will','should', "didn't","doesn't","haven't","isn't","aren't","can't","couldn't","wouldn't","won't","shouldn't",'?', "ain't"]

def custom_boundary(docx):
    for token in docx[:-1]:
        if token.text.lower() in q_words:
            docx[token.i].is_sent_start = True
    return docx

class QuestionDetector():
    #Class Initialier:
    #- Creates naive bayes classifier using nltk nps_chat corpus.
    #- Initializes Tweet tokenizer
    #- Initializes question words set to be used
    def __init__(self):
        posts = nltk.corpus.nps_chat.xml_posts()
        featuresets = [(self.__dialogue_act_features(post.text), post.get('class')) for post in posts]
        size = int(len(featuresets) * 0.1)
        train_set, test_set = featuresets[size:], featuresets[:size]
        self.classifier = nltk.NaiveBayesClassifier.train(train_set)
        question_words = ['what', 'where', 'when','how','why','did','do','does','have','has','am','is','are','can','could','may','would','will','should', "didn't","doesn't","haven't","isn't","aren't","can't","couldn't","wouldn't","won't","shouldn't",'?', "ain't"]
        self.Question_Words_Set = set(question_words)
        self.tknzr = TweetTokenizer()

    #Private method, Gets the word vector from sentence
    def __dialogue_act_features(self,sentence):
         features = {}
         for word in nltk.word_tokenize(sentence):
             features['contains({})'.format(word.lower())] = True
         return features

    #Public Method, Returns 'True' if sentence is predicted to be a question, returns 'False' otherwise
    def isQuestion(self,sentence):
        if "?" in sentence:
            return True
        tokens = self.tknzr.tokenize(sentence.lower())
        if self.Question_Words_Set.intersection(tokens) == False:
            return False
        predicted = self.classifier.classify(self.__dialogue_act_features(sentence))
        if predicted == 'whQuestion' or predicted == 'ynQuestion':
            return True
        return False


nlp = spacy.load("en_core_web_sm")
nlp.add_pipe(custom_boundary, before = "parser")

def initialise(filename):
    print("check init")
    try:
        document = open(filename).read()
        document_nlp = nlp(document)
        start_time = time.time()
        d = QuestionDetector()
        sentence_list = []
        for sentence in document_nlp.sents:
            sentence_list.append(str(sentence))
        question_list = []
        for i in sentence_list:
            question_list.append(d.isQuestion(i))
        print("--- %s seconds ---" % (time.time() - start_time))
        nouns = [i for (i, x) in TextBlob(document).pos_tags if x[0] == 'N']
        print("split sentences", sentence_list)
        print("question or not?", question_list)
        print("nouns", nouns)

        # deleting file after it has been used
        os.remove("txt" + str(num) + ".txt")
        print("removed")
    except:
        print("no file atm")


i = 1;
# @param file_limit can be found in header.py
while True:
    if i >= file_limit:
        i = 1
    try:
        initialise("txt" +   str(i) + ".txt")
        i += 1
    except:
        continue



#TO DO:
#SEND LOGS TO FRONT END
#SEND NOUNS TO FRONT END
#SEND QUESTIONS TO FRONT END AS A POPUP/NOTIF
