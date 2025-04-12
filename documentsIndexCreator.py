import os
import faiss
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from consts import *

def create_minilm_from_descriptions():
    
    # Load embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

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
    faiss.write_index(index, f"{MINILM_INDEX_DIR}/plugins_faiss.index")
    np.save(f"{MINILM_INDEX_DIR}/plugin_filenames.npy", np.array(file_names))

    print("FAISS index saved successfully!")

def create_all_mpnet_base_from_descriptions():

    # Load embedding model
    model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

    # Load and embed plugin files
    docs = []
    file_names = []

    for file in os.listdir(PLUGIN_DIR):
        file_path = os.path.join(PLUGIN_DIR, file)
        if file.endswith(".txt"):  # Ensure only text files are processed
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

                # Chunk text for better retrieval
                splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=128)
                chunks = splitter.split_text(content)

                docs.extend(chunks)
                file_names.extend([file] * len(chunks))  # Keep track of chunk origins

    # Convert documents to embeddings
    embeddings = model.encode(docs, convert_to_numpy=True)

    # Create FAISS index (HNSW for better performance)
    dimension = embeddings.shape[1]
    index = faiss.IndexHNSWFlat(dimension, 32)  # HNSW for better nearest neighbor search
    index.add(embeddings)

    # Save the FAISS index and filenames
    faiss.write_index(index, f"{MPNET_INDEX_DIR}/plugins_faiss.index")
    np.save(f"{MPNET_INDEX_DIR}/plugin_filenames.npy", np.array(file_names))
    np.save(f"{MPNET_INDEX_DIR}/plugin_chunks.npy", np.array(docs))

    print("FAISS index saved successfully!")


# create_minilm_from_descriptions()
create_all_mpnet_base_from_descriptions()