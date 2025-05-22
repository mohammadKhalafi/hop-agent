import json

from consts import BASE_PLUGINS_STORAGE
from pipelineDescriptionCreator import get_design
from datetime import datetime
from systemPrompts import xml_creation_system_prompt, xml_creation_user_prompt
from pipelineXmlCreator import create_pipeline_xml
from requestRunner import run_request

orders_sample = """
  <order>
    <hop>
      <from>p1</from>
      <to>p2</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>p2</from>
      <to>p3</to>
      <enabled>Y</enabled>
    </hop>
  </order>
"""

def CreateDesign(query, scenario_name):
    design = get_design(query)

    now = datetime.now()
    created_date = now.strftime('%Y/%m/%d %H:%M:%S.') + f'{now.microsecond // 1000:03}'

    transforms = CreateTransforms(design, query)
    hops = ''

    pipeline_xml = create_pipeline_xml(scenario_name, created_date, hops, transforms)
    filepath = BASE_PLUGINS_STORAGE+'/'+scenario_name+'.hpl'

    with open(filepath, "w") as file:
        # file.write(pipeline_xml)
        file.write(transforms)

def CreateTransforms(design, query):
    description = design["description"]
    used_plugins = design["used_plugins"]
    plugin_documents = design["plugin_documents"]
    plugin_xmls = design["plugin_xmls"]

    plugin_infos = list(zip(used_plugins, plugin_documents, plugin_xmls))
    plugin_infos = [
        {
            "plugin": plugin,
            "document": document,
            "xml": xml
        }
        for plugin, document, xml in plugin_infos
    ]
    plugin_infos = json.dumps(plugin_infos, indent=4)

    system_prompt = xml_creation_system_prompt.format(plugin_infos=plugin_infos, orders_sample=orders_sample)
    user_prompt =  xml_creation_user_prompt.format(query=query, description=description)
    
    messages = [
        {"role": "system", "content": system_prompt}, 
        {"role": "user", "content": user_prompt}
    ]
    created_transforms = run_request(messages)
    return created_transforms



query = "i want to generate 3 rows of string data with values : 'm1', 'n4', 'ji'. just use data grid plugin. nothing more"
scenario_name = "data_grid_test"
CreateDesign(query, scenario_name)