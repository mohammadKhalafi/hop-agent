import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def search_plugins(query, top_k=3):
    # Load FAISS index
    index = faiss.read_index("C:/Users/mohammad/Desktop/hop/index/plugins_faiss.index")
    file_names = np.load("C:/Users/mohammad/Desktop/hop/index/plugin_filenames.npy")

    # Embed the query
    query_embedding = model.encode([query], convert_to_numpy=True)

    # Search FAISS
    distances, indices = index.search(query_embedding, top_k)

    # Retrieve results
    results = [(file_names[i], distances[0][j]) for j, i in enumerate(indices[0])]
    
    return results


# Example query
query = "i want to read 100 rows of a topic from kafka and store it in postgressql with url 192.168.10.11"
results = search_plugins(query, 3)

for file, score in results:
    print(f"Match: {file} (Score: {score})")
