import json

from pluginDocumentsSearch import search
from documentsProvider import get_plugin_full_docs, get_plugin_xmls, get_plugin_tips
from systemPrompts import pipeline_description_prompt
from requestRunner import run_request

def create_pipeline_description(query):
    plugins = search(query)
    plugin_docs = get_plugin_full_docs(plugins, True)
    plugin_json = {plugin: {"document": doc} for plugin, doc in plugin_docs.items()}
    plugin_json_str = json.dumps(plugin_json, indent=2)
    pipeline_description_prompt_for_query = pipeline_description_prompt.format(plugin_docs=plugin_json_str)

    messages = [
        {"role": "system", "content": pipeline_description_prompt_for_query}, 
        {"role": "user", "content": query}
    ]
    pipeline_design = run_request(messages)
    return pipeline_design

def strip_code_fences(text):
    text = text.strip()
    if text.startswith("```json"):
        text = text[len("```json"):].strip()
    elif text.startswith("```"):
        text = text[len("```"):].strip()
    if text.endswith("```"):
        text = text[:-len("```")].strip()
    return text

def get_design(query):
    design = create_pipeline_description(query)
    print("answer")
    design = strip_code_fences(design)
    data = json.loads(design)
    description = data['description']
    print(description)
    used_plugins = data['used_plugins']
    print(used_plugins)
    print(len(used_plugins))
    
    plugin_documents = get_plugin_full_docs(used_plugins)
    plugin_xmls = get_plugin_xmls(used_plugins)
    plugin_tips = get_plugin_tips(used_plugins)

    return {
        "description": description,
        "used_plugins": used_plugins,
        "plugin_documents": plugin_documents,
        "plugin_xmls": plugin_xmls,
        "plugin_tips" : plugin_tips
    }

def get_design2(description, used_plugins):
    plugin_documents = get_plugin_full_docs(used_plugins)
    plugin_xmls = get_plugin_xmls(used_plugins)
    plugin_tips = get_plugin_tips(used_plugins)

    return {
        "description": description,
        "used_plugins": used_plugins,
        "plugin_documents": plugin_documents,
        "plugin_xmls": plugin_xmls,
        "plugin_tips" : plugin_tips
    }

# query = "i want to read 100 rows of a topic from kafka then insert rows into postgres with url 192.168.10.11"
# query = "i want to generate 5 rows of random data have one text column then insert rows into postgres with url 192.168.10.11"
# query = "i want to generate 5 rows of random data have one text column then insert rows as csv into local file"
# get_design(query)