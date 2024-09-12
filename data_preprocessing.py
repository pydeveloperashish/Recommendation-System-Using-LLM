import pandas as pd
import re

# Load and preprocess function
def load_and_preprocess_csv(file_path):
    df = pd.read_csv(file_path)
    
    def clean_text(text):
        text = re.sub(r'\s+', ' ', str(text).strip().lower())
        text = re.sub(r'[^a-z0-9\s,]', '', text)
        return text

    def combine_fields(row):
        return f"{row['Product Name']} {row['Description']} {row['Product Tags']} {row['Platform']}"

    df['combined_text'] = df.apply(combine_fields, axis=1)
    df['combined_text'] = df['combined_text'].apply(clean_text)
    
    return df


df = load_and_preprocess_csv('dataset.csv')
df.to_csv('processed_final_data.csv')