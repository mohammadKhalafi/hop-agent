import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Directory where plugin files are stored
PLUGIN_DIR = "C:/Users/mohammad/Desktop/hop/hop_plugins"

# Load and embed plugin files
docs = []
file_names = []

for file in os.listdir(PLUGIN_DIR):
    file_path = os.path.join(PLUGIN_DIR, file)
    if file.endswith(".txt"):  # Ensure only text files are processed
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            docs.append(content)
            file_names.append(file)

# Convert documents to embeddings
embeddings = model.encode(docs, convert_to_numpy=True)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)  # L2 distance (Euclidean)
index.add(embeddings)

# Save the index for future use
faiss.write_index(index, "C:/Users/mohammad/Desktop/hop/index/plugins_faiss.index")
np.save("C:/Users/mohammad/Desktop/hop/index/plugin_filenames.npy", np.array(file_names))

print("FAISS index saved successfully!")
