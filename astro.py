import torch
import os
import re

PINK = '\033[95m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

EMBEDDINGS_FILE = "vault_embeddings.pt"

def save_embeddings(embeddings, filepath):
    torch.save(embeddings, filepath)

def load_embeddings(filepath):
    if os.path.exists(filepath):
        return torch.load(filepath)
    return None

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def clean_and_split_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    sentences = re.split(r'(?<=[.!?]) +', text)
    return sentences
