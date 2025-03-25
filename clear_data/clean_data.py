import pandas as pd
import re
from pyvi import ViTokenizer
# Đọc danh sách stopwords từ file
with open("./clear_data/vietnamese-stopwords.txt", "r", encoding="utf-8") as f:
    stopwords = set(f.read().splitlines())

def xoa_stopwords(text):
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stopwords]
    return ' '.join(filtered_words)

def chuan_hoa_text(text):
    text_lower = text.lower()
    text_remove_special = re.sub(r'[^\w\s]', '', text_lower)
    text_remove_space = text_remove_special.strip()
    text_to_unicode = normalize_to_unicode(text_remove_space)
    tokenized_text = ViTokenizer.tokenize(text_to_unicode)
    text_remove_stopword = remove_stopwords(tokenized_text)
    return text_remove_stopword

def preprocess_text(text):
    text = xoa_stopwords(text)
    text = chuan_hoa_text(text)
    return text

df = pd.read_csv('./raw_data/data/sort_label.csv') 
texts = df['text'].tolist()
labels = df['label'].tolist()

processed_texts = [preprocess_text(text) for text in texts]
print(processed_texts)

processed_df = pd.DataFrame({'text': processed_texts, 'label': labels})

processed_df.to_csv('./clear_data/data/clean_data.csv', index=False, encoding='utf-8')
