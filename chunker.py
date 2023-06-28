import re
from spacy.lang.en import English

nlp = English()  # Just the language with no model
nlp.add_pipe("sentencizer")  # Adding a sentencizer pipeline component


def split_sentences(text):
    doc = nlp(text)
    return [sent.text for sent in doc.sents]


def split_into_chunks(text, max_len=800):
    sentences = split_sentences(text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_len:
            current_chunk += sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    return chunks


def clean_and_split_text(text):
    # Remove extra newline characters and join the text
    text = " ".join(text.strip().split("\n"))
    # Remove page numbers
    text = re.sub(r"\d+\n", "", text)
    # Remove citations
    # text = re.sub(r"(?:\*\s*[A-Za-z\d*]+\s*vide[^“]*?(?:\n|$))", "", text)
    # Identify rule titles and add a separator before them
    text = re.sub(r"(\d+(\.|\')\.?\s[^—]+[,—])", r"@@@\1", text)
    # Split the text based on the separator
    segments = text.split("@@@")
    # Create a list to store the cleaned segments
    cleaned_segments = []
    for segment in segments:
        # Only remove extra spaces and newline characters
        segment = re.sub(r"\s+", " ", segment).strip()

        if len(segment) > 800:
            split_chunks = split_into_chunks(segment)
            cleaned_segments.extend(split_chunks)
        else:
            cleaned_segments.append(segment)
    cleaned_segments = [segment for segment in cleaned_segments if segment.strip()]
    return cleaned_segments
