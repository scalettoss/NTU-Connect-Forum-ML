import math
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

def compute_tf(document):
    
    words = document.lower().split()
    word_count = {}
    total_words = len(words)
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    tf = {word: count / total_words for word, count in word_count.items()}
    return tf

def compute_idf(documents):
    
    N = len(documents)
    word_df = {}
    for doc in documents:
        words = set(doc.split())
        for word in words:
            word_df[word] = word_df.get(word, 0) + 1
    idf = {word: math.log((N + 1) / (df + 1)) + 1 for word, df in word_df.items()}
    return idf

def compute_tf_idf(documents, idf_scores=None):
    
    if idf_scores is None:
        idf_scores = compute_idf(documents)
    tf_idf = []
    for doc in documents:
        tf_scores = compute_tf(doc)
        tf_idf_s = {word: tf_scores[word] * idf_scores.get(word, 0) for word in tf_scores}
        tf_idf.append(tf_idf_s)
    return tf_idf

def convert_to_matrix(tf_idf_scores, vocabulary):
    matrix = [[doc_scores.get(word, 0) for word in vocabulary] for doc_scores in tf_idf_scores]
    return matrix

# File paths for saving model and data
MODEL_PATH = 'train/svm_model.pkl'
VOCAB_PATH = 'train/vocabulary.pkl'
IDF_PATH = 'train/idf_scores.pkl'

def  train_model(X_train_list, y_train):
    idf_scores = compute_idf(X_train_list)
    tf_idf_train = compute_tf_idf(X_train_list, idf_scores)
    vocabulary = sorted(set().union(*[doc_scores.keys() for doc_scores in tf_idf_train]))

    tf_idf_train = compute_tf_idf(X_train_list, idf_scores)
    X_train_matrix = convert_to_matrix(tf_idf_train, vocabulary)
    X_train_array = np.array(X_train_matrix)

    # Train SVM model
    svm_model = SVC(kernel='linear', random_state=42)
    svm_model.fit(X_train_array, y_train)

    joblib.dump(svm_model, MODEL_PATH)
    joblib.dump(vocabulary, VOCAB_PATH)
    joblib.dump(idf_scores, IDF_PATH)

    print("Model trained and saved successfully!")
    return svm_model, vocabulary, idf_scores

def predict_with_model(X_test_list):
    if not (os.path.exists(MODEL_PATH) and os.path.exists(VOCAB_PATH) and os.path.exists(IDF_PATH)):
        print("No saved model or data found. Please train the model first!")
        return None

    # Load model, vocabulary, and IDF scores
    svm_model = joblib.load(MODEL_PATH)
    vocabulary = joblib.load(VOCAB_PATH)
    idf_scores = joblib.load(IDF_PATH)

    # Compute TF-IDF for test data
    tf_idf_test = compute_tf_idf(X_test_list, idf_scores)
    X_test_matrix = convert_to_matrix(tf_idf_test, vocabulary)
    X_test_array = np.array(X_test_matrix)

    # Predict
    y_pred = svm_model.predict(X_test_array)
    return y_pred

def predict_text(text):
    
    if not (os.path.exists(MODEL_PATH) and os.path.exists(VOCAB_PATH) and os.path.exists(IDF_PATH)):
        print("No saved model or data found. Please train the model first!")
        return None

   
    svm_model = joblib.load(MODEL_PATH)
    vocabulary = joblib.load(VOCAB_PATH)
    idf_scores = joblib.load(IDF_PATH)

    text_list = [text]  
    tf_idf = compute_tf_idf(text_list, idf_scores)
    text_matrix = convert_to_matrix(tf_idf, vocabulary)
    text_array = np.array(text_matrix)

    # Predict
    prediction = svm_model.predict(text_array)[0]  
    return prediction

data = pd.read_csv('dataset.csv')
X = data['text'].fillna('')  
y = data['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train_list = X_train.tolist()
X_test_list = X_test.tolist()

if not os.path.exists(MODEL_PATH):
    svm_model, vocabulary, idf_scores =  train_model(X_train_list, y_train)
else:
    print("Model already exists, skipping training.")

y_pred = predict_with_model(X_test_list)

if y_pred is not None:
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    example_text = "bán khóa học giá rẻ"
    predicted_label = predict_text(example_text)
    print(f"\nExample prediction:")
    print(f"Text: '{example_text}'")
    print(f"Predicted label: {predicted_label}")