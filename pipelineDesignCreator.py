from consts import BASE_PLUGINS_STORAGE
from pipelineDescriptionCreator import get_design
from datetime import datetime

from pipelineXmlCreator import create_pipeline_xml

def CreateDesign(query, scenario_name):
    design = get_design(query)

    now = datetime.now()
    created_date = now.strftime('%Y/%m/%d %H:%M:%S.') + f'{now.microsecond // 1000:03}'

    hops = ''
    transforms = ''

    pipeline_xml = create_pipeline_xml(scenario_name, created_date, hops, transforms)
    filepath = BASE_PLUGINS_STORAGE+'/'+scenario_name+'.hpl'

    with open(filepath, "w") as file:
        file.write(pipeline_xml)



query = "i want to generate 3 rows of string data with values : 'm1', 'n4', 'ji' with data grid plugin then insert rows as csv into local file"
scenario_name = "fileCreator"
CreateDesign(query, scenario_name)