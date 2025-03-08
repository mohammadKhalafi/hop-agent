with open("./prompts/design-pipeline-prompt", "r", encoding="utf-8") as file:
    content = file.read()

plugins = ""
with open("./documents/RowGenerator/description", "r", encoding="utf-8") as file:
    plugins += '{"plugin-type":"RowGenerator","description":"'
    plugins += file.read()
    plugins += '"},'

plugins += "]"

content = content.replace("//plugins//", plugins)

design_pipeline_prompt = content
