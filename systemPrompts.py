with open("./prompts/query-expand-prompt", "r", encoding="utf-8") as file:
    content = file.read()

query_expand_prompt = content


with open("./prompts/pipeline-description", "r", encoding="utf-8") as file:
    content = file.read()

pipeline_description_prompt = content


with open("./prompts/xml-creation-system-prompt", "r", encoding="utf-8") as file:
    content = file.read()

xml_creation_system_prompt = content


with open("./prompts/xml-creation-user-prompt", "r", encoding="utf-8") as file:
    content = file.read()

xml_creation_user_prompt = content