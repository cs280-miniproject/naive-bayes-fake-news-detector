import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.model_selection import StratifiedKFold
from parser.fake_news_net_parser import FakeNewsNetParser
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer,\
    TfidfVectorizer


def main():
    X, y = FakeNewsNetParser().parse(['PolitiFact'])

    text_clf = Pipeline([
        ('tfidf_vect', TfidfVectorizer(ngram_range=(1, 2))),
        ('clf', ComplementNB(alpha=0.01)),
    ])

    skf = StratifiedKFold(n_splits=5)
    for train_index, test_index in skf.split(X, y):
        print('--------------------------------------------------------------')
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        text_clf = text_clf.fit(X_train, y_train)

        cv = CountVectorizer(ngram_range=(1, 2))
        cv.fit_transform(X_train)
        print(len(cv.vocabulary_))

        y_pred = text_clf.predict(X_test)
        print('ACCURACY: {}'.format(np.mean(y_pred == y_test)))
        print(confusion_matrix(y_test, y_pred))
        print(classification_report(y_test, y_pred))

if __name__ == '__main__':
    main()
