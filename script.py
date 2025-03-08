from requestRunner import run_request

messages = [
    {"role": "system", "content": "You are a helpful assistant."}, 
    {"role": "user", "content": "What is deepseek?"}
    ]

run_request(messages)

