import os
import numpy as np
import hnswlib
from transformers import AutoTokenizer, AutoModel
import torch

# Configuration
DOCUMENTS_DIR = 'documents' #Name of the folder containing your documents
INDEX_FILE = 'hnsw_index.bin' #Name of the index of your files
DIM = 768  # Vectors dimension
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModel.from_pretrained('bert-base-uncased')

#Transform text into vectors
def embed_text(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

# Initializing the HNWS index
index = hnswlib.Index(space='cosine', dim=DIM)

# We create the index if it doesn't already exists
if os.path.exists(INDEX_FILE):
    index.load_index(INDEX_FILE)
else:
    index.init_index(max_elements=10000, ef_construction=2000, M=96)
    index.set_ef(50)

document_vectors = []
document_paths = []

# We transform each file inside the folder into vectors
for file_name in os.listdir(DOCUMENTS_DIR):
    if file_name != "README.txt":
        file_path = os.path.join(DOCUMENTS_DIR, file_name)
        with open(file_path, 'r') as file:
            text = file.read()
            vector = embed_text(text)
            document_vectors.append(vector)
            document_paths.append(file_path)

# Every vector created is then added to the index
if document_vectors:
    index.add_items(np.array(document_vectors), np.arange(len(document_vectors)))

# The index and the path to the documents are saved
index.save_index(INDEX_FILE)
with open('document_paths.txt', 'w') as f:
    for path in document_paths:
        f.write(f"{path}\n")

print("Finished indexing your documents.")

