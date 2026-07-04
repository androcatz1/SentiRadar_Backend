import re, regex
import html
import emoji

from app.config.text_config import CONTRACTION_MAPPING, ENGLISH_STOPWORDS_FULL, MALAY_STOPWORDS_FULL, SLANG_MAPPING

latin_pattern = re.compile(r"[A-Za-z]")

#------------------------------------------------------------------------------
def clean_html_and_entities(text):
    # Remove <a href="...">...</a> completely
    text = re.sub(r'<a\s+href="[^"]*">.*?</a>', '', text)

    # Remove all other HTML tags but keep inner text
    text = re.sub(r'<[^>]+>', '', text)

    # Remove URLs (http, https, www, and domain-like patterns)
    text = re.sub(r'(https?://\S+|www\.\S+)', '', text)

    # Remove standalone domain-like strings (e.g. example.com, site.co, etc.)
    text = re.sub(r'\b[\w.-]+\.(com|co|net|org|io|gov|edu)\b', '', text, flags=re.IGNORECASE)

    # Decode HTML entities like &amp; -> &, &#39; -> '
    text = html.unescape(text)

    # Clean extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text

#------------------------------------------------------------------------------
def expand_contractions(text):
    # Simple word-by-word replacement
    words = text.split()
    expanded_words = [CONTRACTION_MAPPING.get(w.lower(), w) for w in words]
    return " ".join(expanded_words)

#------------------------------------------------------------------------------
def correct_slang(text):
    words = text.split()
    corrected_words = [SLANG_MAPPING.get(w.lower(), w) for w in words]
    return " ".join(corrected_words)

#------------------------------------------------------------------------------
def is_emoji_only(text: str) -> bool:
    text = text.strip()

    # remove all emojis from text
    stripped = emoji.replace_emoji(text, replace="")

    # if nothing left after removing emojis → emoji-only
    return len(stripped.strip()) == 0 and len(text) > 0


def is_valid_text(text: str) -> bool:
    text = text.strip()

    has_latin = bool(latin_pattern.search(text))
    emoji_only = is_emoji_only(text)

    return has_latin or emoji_only

#------------------------------------------------------------------------------
def trim_text(text, front=700, back=100):
    words = text.split()

    # If the total word count is small, return the original text
    if len(words) <= front + back:
        return " ".join(words)

    # Grab the front words and back words safely
    front_part = " ".join(words[:front])
    back_part = " ".join(words[-back:])

    return front_part + " ... " + back_part

#------------------------------------------------------------------------------
def collapse(text):
    for e in set(emoji.distinct_emoji_list(text)):
        text = re.sub(f"({re.escape(e)}){{3,}}", r"\1\1", text)
    return text

#------------------------------------------------------------------------------
def keep_latin_and_emoji(text):
    if not isinstance(text, str):
        return text

    result = []

    for char in text:
        if (
            regex.match(r'[\p{Latin}\p{N}\p{P}\p{Z}]', char)
            or emoji.is_emoji(char)
        ):
            result.append(char)

    return ''.join(result)

#------------------------------------------------------------------------------
all_stopwords = ENGLISH_STOPWORDS_FULL.union(MALAY_STOPWORDS_FULL)

def remove_stopwords(text):
    # 1. Convert to lowercase and remove all punctuation/emojis
    clean_text = re.sub(r'[^\w\s]', '', str(text).lower())
    
    # 2. Split into clean words
    words = clean_text.split()
    
    # 3. Filter out stopwords (strip is no longer needed)
    filtered = [w for w in words if w not in all_stopwords]
    
    return " ".join(filtered)