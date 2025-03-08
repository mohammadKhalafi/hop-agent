from requestRunner import run_request
from systemPrompts import design_pipeline_prompt

user_description_of_pipeline = "i want to create a table with 5 rows and three columns one of them has integer type. fill table with sample data."
messages = [
    {"role": "system", "content": design_pipeline_prompt}, 
    {"role": "user", "content": user_description_of_pipeline}
    ]

pipeline_design = run_request(messages)


