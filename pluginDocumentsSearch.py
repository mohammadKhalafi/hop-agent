import os
import faiss
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from consts import *
from requestRunner import run_request
from systemPrompts import query_expand_prompt


def minilm_search(query, top_k):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    index = faiss.read_index(MINILM_INDEX_DIR + "/plugins_faiss.index")
    file_names = np.load(MINILM_INDEX_DIR + "/plugin_filenames.npy")

    # Embed the query
    query_embedding = model.encode([query], convert_to_numpy=True)

    # Search FAISS
    distances, indices = index.search(query_embedding, top_k)

    # Retrieve results
    results = [(file_names[i], distances[0][j]) for j, i in enumerate(indices[0])]
    
    return results



def mpnet_search(query, top_k=5):
    model = SentenceTransformer("all-mpnet-base-v2")  
    index = faiss.read_index(os.path.join(MPNET_INDEX_DIR, "plugins_faiss.index"))
    file_names = np.load(os.path.join(MPNET_INDEX_DIR, "plugin_filenames.npy"), allow_pickle=True)
    chunks = np.load(os.path.join(MPNET_INDEX_DIR, "plugin_chunks.npy"), allow_pickle=True)
    
    # FAISS search
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)

    results = [(file_names[i], distances[0][j]) for j, i in enumerate(indices[0])]

    return results


def enrich_query(query):
    # hohos = " relational database are like postgres, oracledb, sqlserver, ..."
    request = query_expand_prompt.replace("{{Query}}", query)
    messages = [
        {"role": "user", "content": request}
        ]
    response = run_request(messages)
    return response

def search(query):
    print(query)
    final_query = enrich_query(query) 
    print(final_query)
    results = minilm_search(final_query, 20)
    for file, score in results:
        print(f"Match: {file} (Score: {score})")
    return [file for file, score in results]



query = "i want to read 100 rows of a topic from kafka then insert rows into postgres with url 192.168.10.11"
plugins = search(query)