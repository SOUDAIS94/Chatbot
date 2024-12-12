import nltk
nltk.download('punkt')  # Télécharge les ressources nécessaires pour la tokenisation
nltk.download('stopwords')  # Télécharge les stopwords si nécessaire
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
# import des packages pour le pré-traitement
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import streamlit as st
# Charger le fichier FAQ
faq_dict = {}
current_question = None

with open('FAQ.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line.startswith('Q:'):
            current_question = line[2:].strip()
        elif line.startswith('R:') and current_question:
            faq_dict[current_question] = line[2:].strip()

# Prétraitement
def preprocess(sentence):
    words = word_tokenize(sentence)
    words = [word.lower() for word in words if word.lower() not in stopwords.words('english') and word not in string.punctuation]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return words

# Trouver la réponse la plus pertinente
def get_most_relevant_sentence(query):
    query = preprocess(query)
    max_similarity = 0
    most_relevant_question = None

    for question in faq_dict.keys():
        processed_question = preprocess(question)
        similarity = len(set(query).intersection(processed_question)) / float(len(set(query).union(processed_question)))
        if similarity > max_similarity:
            max_similarity = similarity
            most_relevant_question = question

    if most_relevant_question:
        return faq_dict[most_relevant_question]
    else:
        return "Je ne suis pas sûr de comprendre votre question. Pouvez-vous reformuler ?"

# Interface Streamlit
st.title("Chatbot : Travel agency FAQ")
st.write("Bienvenue sur votre assistant IA, conçu par KONE Souleymane pour répondre à vos besoins dans le domaine de l'agence de voyage")
user_input = st.text_input("Posez votre question ici :")

if user_input:
    response = get_most_relevant_sentence(user_input)
    st.write(f"Réponse : {response}")

