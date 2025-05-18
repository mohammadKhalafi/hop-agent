with open("./documents/pipeline-template", "r", encoding="utf-8") as file:
    content = file.read()

pipeline_template = content

def create_pipeline_xml(SCENARIO_NAME, CREATED_DATE, HOPS, TRANSFORMS):
    return pipeline_template.format(SCENARIO_NAME=SCENARIO_NAME,
        CREATED_DATE=CREATED_DATE,
        MODIFIED_DATE=CREATED_DATE,
        HOPS=HOPS, 
        TRANSFORMS=TRANSFORMS)
