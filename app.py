import streamlit as st
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Sample training data
data = {
    'text': ["I love data science", "Python is amazing", "Win money now", "Free offer click now"],
    'spam': [0, 0, 1, 1]
}
df = pd.DataFrame(data)

# Preprocessing setup
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    words = text.lower().split()
    words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
    return " ".join(words)

df['clean_text'] = df['text'].apply(preprocess)

# Model pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('model', LogisticRegression())
])

pipeline.fit(df['clean_text'], df['spam'])

# Streamlit UI
st.title("Spam Detection App ")

user_input = st.text_area("Enter your message:")

if st.button("Predict"):
    clean = preprocess(user_input)
    prediction = pipeline.predict([clean])[0]

    if prediction == 1:
        st.error("Spam Message")
    else:
        st.success("Not Spam")