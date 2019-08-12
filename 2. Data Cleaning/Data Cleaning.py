import re, string
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 
import pandas as pd
import numpy as np
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
lemmatizer = WordNetLemmatizer()
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def cleaning(sentences):
    result = []
    for text in sentences:
        text = str(text)
        text = text.lower()
        text = re.sub(r"\'m", " am", text)
        text = re.sub(r"\'s", " is", text)
        text = re.sub(r"\'ll", " will", text)
        text = re.sub(r"\'ve", " have", text)
        text = re.sub(r"\'re", " are", text)
        text = re.sub(r"won\'t", "will not", text)
        text = re.sub(r"can\'t", "cannot", text)
        text = re.sub(r"n\'t", " not", text)
        text = re.sub(r"\'bout", "about", text)
        text = re.sub(r"\'til", "until", text)
        text = re.sub(r"""[^a-zA-Z0-9-!$%^&@*()+|=`{}\[\]:;"'<>?,.\/\s]"""," ",text)
        text = re.sub(r"\bft\b|\bforeigntalent\b","foreign talent",text)
        text = re.sub(r"\bgovt\b|\bgahment\b|\bgahmen\b|\bgov\b","government",text)
        text = re.sub(r"\bpapies\b|\bpapees\b","pappies",text)
        text = re.sub(r"\bchi bai\b|\bchibai\b|\bchee bye\b|\bcheebye\b","cb",text)
        text = re.sub(r"\bfk\b|\bfck\b","fuck",text)
        text = re.sub(r"\bkanina\b|\bkanena\b","knn",text)
        text = re.sub(r"\blky\b","lee kuan yew",text)
        text = re.sub(r"\blhl\b|\bpm lee\b","lee hsien loong",text)
        if len(text.split()) == 0:
            continue
        then = []
        sw = stopwords.words('english')
        for word in text.split():
            if word not in sw:
              word = lemmatizer.lemmatize(word, get_wordnet_pos(word))
              then.append(word)
        result.append(then)
    result = [" ".join(x) for x in result]
    return result

# Outputs a list. Just assign the list back to your dataframe column if need be.