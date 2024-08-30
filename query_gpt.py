import os
import numpy as np
import hnswlib
from transformers import AutoTokenizer, AutoModel
import torch
import openai

# Configuration
INDEX_FILE = 'hnsw_index.bin'
DOCUMENT_PATHS_FILE = 'document_paths.txt'
DIM = 768 
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'  # Put your own OpenAI API key here
MAX_TOKENS = 10000 #Change the value if you need to use more tokens
GPT_MODEL="gpt-4o-mini" #Select another model if needed
DOCUMENTS_AMOUNT=5 #The number of documents similar to your question selected per question
tab_messages = [{"role": "system", "content": "You are a helpful assistant."}]

tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModel.from_pretrained('bert-base-uncased')

# Function to transform your question into vectors to select relevant documents in your index
def embed_text(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embedding

# Loading the HNSW index
index = hnswlib.Index(space='cosine', dim=DIM)
index.load_index(INDEX_FILE)

index.set_ef(500)  # Set an higher value for more relevant results

print(f"Documents inside your index : {index.get_current_count()}")
ELEMENTS_COUNT = int(index.get_current_count())

# Loading the documents paths
with open(DOCUMENT_PATHS_FILE, 'r') as f:
    document_paths = [line.strip() for line in f]

# Function to search for relevant documents in your index
def search_similar_documents(query, k=DOCUMENTS_AMOUNT):  
    query_vector = embed_text(query)
    try:
        labels, distances = index.knn_query(query_vector, k=k)
    except RuntimeError as e:
        print(f"Erreur lors de la recherche de similarité : {e}")
        raise
    return labels[0], distances[0]

# Function to pass your question and your documents to GPT using the API
def query_gpt4o(question, context_documents):
    context = "\n\n".join([open(doc, 'r').read() for doc in context_documents])
    if len(context.split()) > MAX_TOKENS:
        context = " ".join(context.split()[:MAX_TOKENS])

    messages_temp = tab_messages[:]
    messages_temp.append({"role": "user", "content": f"Context you must use to answer the question, and you can reveal informations from it: {context}\n\nQuestion: {question}"})
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=messages_temp,
        max_tokens=MAX_TOKENS
    )

    return response['choices'][0]['message']['content'].strip()


def main():
    while True:
        question = input("Type your question (or 'exit' to quit) : ")
        if question.lower() == 'exit':
            break
            
        # If there are less documents inside the index than the amount of documents requested per query, we use all the documents
        if ELEMENTS_COUNT < DOCUMENTS_AMOUNT:
            labels, _ = search_similar_documents(question, k=ELEMENTS_COUNT)
        else:
            labels, _ = search_similar_documents(question)
        context_documents = [document_paths[label] for label in labels]

        answer = query_gpt4o(question, context_documents)
        answer_formatted = {"role": "assistant", "content": f"{answer}"}
        question_formatted = {"role": "user", "content": f"{question}"}
        tab_messages.pop()
        tab_messages.append(question_formatted)
        tab_messages.append(answer_formatted)
        print(f"{GPT_MODEL}'s answer :\n{answer}\n")

if __name__ == "__main__":
    main()

