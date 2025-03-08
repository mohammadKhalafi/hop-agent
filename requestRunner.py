import os
import requests
import time
import logging
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('METIS_API_KEY')

logging.basicConfig(filename="app.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def run_request(messages):
    logging.info(f"Processing messages started.")

    url = "https://api.metisai.ir/api/v1/wrapper/deepseek/chat/completions"

    # Headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"  # Read API key from environment
    }

    data = {
        "model": "deepseek-chat",
        "messages": messages
    }

    logging.debug(f"Processing data: {data}")

    start_time = time.time()
    response = requests.post(url, json=data, headers=headers)
    end_time = time.time()
    response_time = end_time - start_time

    if response.status_code == 200:
        message_content = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        print(message_content[0:10], f'\\ in time :{response_time}')
        logging.info(f"Processed result in {response_time}")
        logging.debug(f"Result : {message_content}")
        return message_content
    else:
        error = f"Error: {response.status_code}, {response.text}"
        logging.error(f"Error : {error}")
        print(error)
        raise Exception(error)