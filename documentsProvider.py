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

def get_plugin_xmls(plugins, add_all_plugin_xmls=False):
    xmls = {}

    if add_all_plugin_xmls:
        xmls = {
            os.path.splitext(f)[0]: None
            for f in os.listdir(PLUGIN_XML_DIR) 
            if f.endswith('.xml')
        }
    
    for plugin in plugins:
        file_path = os.path.join(PLUGIN_XML_DIR, plugin + ".xml")
        with open(file_path, 'r', encoding='utf-8') as f:
            xmls[plugin] = f.read()

    return xmls


def get_plugin_tips(plugins):
    tips = {}

    for plugin in plugins:
        file_path = os.path.join(PLUGIN_XML_DIR, plugin + ".txt")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tips[plugin] = f.read()
            print('tips:'+plugin)
        except:
            tips[plugin] = ''

    return tips