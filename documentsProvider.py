from consts import *
import os

def get_plugin_full_docs(plugins, add_all_plugin_names=False):
    docs = {}

    if add_all_plugin_names:
        docs = {
            os.path.splitext(f)[0]: None
            for f in os.listdir(COMPLETE_DOC_DIR) 
            if f.endswith('.txt')
        }
    
    for plugin in plugins:
        file_path = os.path.join(COMPLETE_DOC_DIR, plugin + ".txt")
        with open(file_path, 'r', encoding='utf-8') as f:
            docs[plugin] = f.read()
            
    return docs