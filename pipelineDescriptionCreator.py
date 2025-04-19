import json

from pluginDocumentsSearch import search
from documentsProvider import get_plugin_full_docs
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


query = "i want to read 100 rows of a topic from kafka then insert rows into postgres with url 192.168.10.11"
design = create_pipeline_description(query)
print(design)