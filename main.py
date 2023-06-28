import os
import chunker


def get_extracted_text_path(pdf_path):
    return f"./extracted_texts/{os.path.splitext(os.path.basename(pdf_path))[0]}.txt"


def read_extracted_text(txt_file_path):
    with open(txt_file_path, "r", encoding="utf-8") as file:
        return file.read()


def get_chunks(file_path):
    doc = read_extracted_text(file_path)
    chunks = chunker.clean_and_split_text(doc)
    return chunks


chunks = get_chunks("extracted_texts/temp1687594873613.txt")
print(chunks)
