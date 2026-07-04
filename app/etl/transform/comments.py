import pandas as pd

from app.etl.comment_utils.helpers import *
from app.ml.inference.inference import predict

def run_pipeline(comments: pd.DataFrame):
    df = comments.copy()

    #1 lower case the test
    df['text_processed'] = df['text'].str.lower()

    #2 remove whitespace from text
    df['text_processed'] = df['text_processed'].str.replace(r'\s+', ' ', regex=True).str.strip()

    #3 Remove HTML tags, remove <a> links, decode HTML entities and links(general like www.google.com)
    df['text_processed'] = df['text_processed'].apply(clean_html_and_entities)

    #4 Trim text which are too long (spams/copy pasta)
    # df['text_processed'] = df['text_processed'].apply(trim_text)

    #5 Expand English contractions
    df['text_processed'] = df['text_processed'].apply(expand_contractions)

    #6 Slang mapping
    df['text_processed'] = df['text_processed'].apply(correct_slang)

    #7 Check if contains latin characters/emoji
    df = df[df['text_processed'].apply(is_valid_text)]

    #8 collapse emojis that are more than 2 consecutive emojis into just 2 emojis max
    df['text_processed'] = df['text_processed'].apply(collapse)

    #9 removes non latin characters from text (like chinese, japanese, arabic, korean and more)
    df['text_processed'] = df['text_processed'].apply(keep_latin_and_emoji)

    #10 removes rows which are empty for text (since some step can make the text empty/NaN)
    df = df[df['text_processed'].str.strip() != ""]
    df = df.dropna(subset=['text_processed'])

    #11 removes possible new duplicates 
    df = df.drop_duplicates(subset=['text_processed'], keep='first')

    df['text_no_stopwords'] = df['text_processed'].apply(remove_stopwords)

    return df

def predict_labels(comments:pd.DataFrame):
    df = comments.copy()
    df = df[['video_id', 'text', 'text_processed', 'text_no_stopwords']]

    predictions = predict(df["text_processed"])

    df['label'] = predictions

    return df