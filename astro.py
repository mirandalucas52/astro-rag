import torch
import os
import re
import ollama
import json
from openai import OpenAI
import argparse

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

def get_relevant_context(rewritten_input, vault_embeddings, vault_content, top_k=3):
    if vault_embeddings.nelement() == 0:
        return []
    input_embedding = ollama.embeddings(model='mxbai-embed-large', prompt=rewritten_input)["embedding"]
    cos_scores = torch.cosine_similarity(torch.tensor(input_embedding).unsqueeze(0), vault_embeddings)
    top_k = min(top_k, len(cos_scores))
    top_indices = torch.topk(cos_scores, k=top_k)[1].tolist()
    relevant_context = [vault_content[idx].strip() for idx in top_indices]
    return relevant_context

def rewrite_query(user_input_json, conversation_history, ollama_model):
    user_input = json.loads(user_input_json)["Query"]
    context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history[-2:]])
    prompt = f"""Rewrite the query below using the conversation history for context. Ensure the core intent is preserved, clarified, and expanded without deviating from the original topic. Do not answer the query.

    Conversation History:
    {context}

    Original query: {user_input}

    Rewritten query:
    """
    response = client.chat.completions.create(
        model=ollama_model,
        messages=[{"role": "system", "content": prompt}],
        max_tokens=200,
        n=1,
        temperature=0.1,
    )
    rewritten_query = response.choices[0].message.content.strip()
    return json.dumps({"Rewritten Query": rewritten_query})

def ollama_chat(user_input, system_message, vault_embeddings, vault_content, ollama_model, conversation_history):
    conversation_history.append({"role": "user", "content": user_input})
    
    if len(conversation_history) > 1:
        query_json = {
            "Query": user_input,
            "Rewritten Query": ""
        }
        rewritten_query_json = rewrite_query(json.dumps(query_json), conversation_history, ollama_model)
        rewritten_query_data = json.loads(rewritten_query_json)
        rewritten_query = rewritten_query_data["Rewritten Query"]
        print(PINK + "Original Query: " + user_input + RESET_COLOR)
        print(PINK + "Rewritten Query: " + rewritten_query + RESET_COLOR)
    else:
        rewritten_query = user_input
    
    relevant_context = get_relevant_context(rewritten_query, vault_embeddings, vault_content)
    if relevant_context:
        context_str = "\n".join(relevant_context)
        print("Context Pulled from Documents: \n\n" + CYAN + context_str + RESET_COLOR)
    else:
        print(CYAN + "No relevant context found." + RESET_COLOR)
    
    user_input_with_context = user_input
    if relevant_context:
        user_input_with_context = user_input + "\n\nRelevant Context:\n" + context_str
    
    conversation_history[-1]["content"] = user_input_with_context
    
    messages = [
        {"role": "system", "content": system_message},
        *conversation_history
    ]
    
    response = client.chat.completions.create(
        model=ollama_model,
        messages=messages,
        max_tokens=2000,
    )
    
    conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
    
    return response.choices[0].message.content

print(NEON_GREEN + "Parsing command-line arguments..." + RESET_COLOR)
parser = argparse.ArgumentParser(description="Ollama Chat")
parser.add_argument("--model", default="llama3.2:1b", help="Ollama model to use (default: llama3.2)")
args = parser.parse_args()

print(NEON_GREEN + "Initializing Ollama API client..." + RESET_COLOR)
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='llama3.2:1b'
)

print(NEON_GREEN + "Generating embeddings for the vault content..." + RESET_COLOR)

print(NEON_GREEN + "Checking for existing embeddings..." + RESET_COLOR)
vault_embeddings_tensor = load_embeddings(EMBEDDINGS_FILE)
vault_content = []
if os.path.exists("vault.txt"):
    with open("vault.txt", "r", encoding='utf-8') as vault_file:
        vault_content = vault_file.readlines()

if vault_embeddings_tensor is None:
    print(NEON_GREEN + "No embeddings found. Generating embeddings for the vault content..." + RESET_COLOR)
    print(NEON_GREEN + "Loading vault content..." + RESET_COLOR)

    vault_embeddings = []
    for content in vault_content:
        response = ollama.embeddings(model='mxbai-embed-large', prompt=content)
        vault_embeddings.append(response["embedding"])
    print("Converting embeddings to tensor...")
    vault_embeddings_tensor = torch.tensor(vault_embeddings) 
    save_embeddings(vault_embeddings_tensor, EMBEDDINGS_FILE)
    print(NEON_GREEN + "Embeddings saved to file: " + EMBEDDINGS_FILE + RESET_COLOR)
else:
    print(NEON_GREEN + "Loaded embeddings from file: " + EMBEDDINGS_FILE + RESET_COLOR)

conversation_history = []
system_message = "You are a helpful assistant that is an expert in knitting by extracting the most useful tips from the given document."

while True:
    user_input = input(YELLOW + "Pose moi une question sur l'astronomie (ou écris quit pour quitter la conversation): " + RESET_COLOR)
    if user_input.lower() == 'quit':
        break
    
    response = ollama_chat(user_input, system_message, vault_embeddings_tensor, vault_content, args.model, conversation_history)
    print(NEON_GREEN + "Response: \n\n" + response + RESET_COLOR)
