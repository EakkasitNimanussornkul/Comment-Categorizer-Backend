import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('wordnet')

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def tokenize_data(text):
    sentences = nltk.tokenize.sent_tokenize(text, language='english')
    tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]

    return sentences, tokenized_sentences

def preprocess_tokens(tokens):
    tokens = [w.lower() for w in tokens]
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if w not in stop_words]

    return tokens

def remove_emoji(string):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


lemmatizer = WordNetLemmatizer()

def preprocess(text):
    # 1. Lowercase
    text = str(text).lower()
    # 2. Remove emojis
    text = remove_emoji(text)
    # 2. Remove special characters (keep only letters and spaces)
    text = clean_text(text)
    # 3. Tokenize (split into words)
    _, tokenized_data = tokenize_data(text)
    # 4. Lemmatize
    lemmatized_tokens = [lemmatizer.lemmatize(word) for sentence in tokenized_data for word in sentence]
    # Join back into a string
    return ' '.join(lemmatized_tokens)

