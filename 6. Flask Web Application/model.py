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

# Training Data
train = pd.read_csv("C:/Users/TKW/Desktop/train.csv")

# Word Classification
def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

# Stopwords
def clean_text(sentences):
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

# Document Cleaning
clean_train = clean_text(train["Comments"])
clean_join = pd.Series(clean_train)
train["Comments"] = clean_join
train = train.dropna()
train["Comments"][:5]

# Attribute Columns
label_cols = ['Insulting', 'Anti Government', 'Xenophobic', 'Racist', 'Sexual']

n = train.shape[0]
vec = TfidfVectorizer(ngram_range=(1,2), 
               min_df=3, max_df=0.9, strip_accents='unicode')
trn_term_doc = vec.fit_transform(train["Comments"])

def pr(y_i, y):
    p = x[y==y_i].sum(0)
    return (p+1) / ((y==y_i).sum()+ 1)
  
x = trn_term_doc

scores = []
sd = []

def get_mdl(y):
    y = y.values
    r = np.log(pr(1,y) / pr(0,y))
    m = LogisticRegression(solver = "liblinear", max_iter = 1000)
    x_nb = x.multiply(r)
    cv_score = np.mean(cross_val_score(
        m, x_nb, y, cv=5, scoring='roc_auc'))
    cv_sd = np.std(cross_val_score(
        m, x_nb, y, cv=5, scoring='roc_auc'))
    scores.append(cv_score)
    sd.append(cv_sd)
    return m.fit(x_nb, y)
  
for i, j in enumerate(label_cols):
    get_mdl(train[j])

def test_mdl(y):
    y = y.values
    r = np.log(pr(1,y) / pr(0,y))
    m = LogisticRegression(C=4, dual=True, solver = "liblinear", max_iter = 1000)
    x_nb = x.multiply(r)
    return m.fit(x_nb, y), r

# Censorship
def censor(comment):
    attributes = []
    test_str = clean_text([comment])
    test_com = pd.Series(test_str)
    test_vec = vec.transform(pd.Series(test_com))
    test_pred = np.zeros((len(test_com), len(label_cols)))
    for i, j in enumerate(label_cols):
        m,r = test_mdl(train[j])
        test_pred[:,i] = m.predict_proba(test_vec.multiply(r))[:,1]
        if test_pred[:,i] >= 0.5:
            attributes.append(j)
    if len(attributes) != 0:
        attributes.insert(0, "Sorry, your comment will be banned as it contains the following material:")
        return(list(attributes))
    else:
        attributes.append('CLEAN')
        attributes.insert(0, 'Your comment is')
        return(list(attributes))