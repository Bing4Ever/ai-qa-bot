from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_openai(message, model="gpt-3.5-turbo", system_prompt="", temperature=0.7, max_tokens=500):
    """
    Function to ask OpenAI's API a question and return the response.
    
    Args:
        prompt (str): The question to ask.
        model (str): The model to use for the request.
        
    Returns:
        str: The response from OpenAI's API.
    """
    full_message = [{"role": "system", "content": system_prompt}] + message

    #return "This is a mock response"


    try:
        response = client.chat.completions.create(
            model=model,
            messages=full_message,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"
     

def load_user_log(data_file):
    """
    Load user log from the JSON file.
    
    Returns:
        list: List of user messages.
    """
    if data_file.exists():
        with open(data_file, 'r', encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_user_log(data_file, user_log):
    with open(data_file, 'w', encoding="utf-8") as f:
        json.dump(user_log, f, indent=2, ensure_ascii=False)

def get_today_key():
    """
    Get today's date in YYYY-MM-DD format.
    
    Returns:
        str: Today's date.
    """
    return datetime.now().strftime("%Y-%m-%d")

def can_ask_today(user_id, user_log, MAX_QUESTIONS_PER_DAY = 5):
    """
    Check if the user can ask questions today based on the user log.
    
    Args:
        user_id (str): The ID of the user.
        user_log (dict): The user log containing question counts.
        
    Returns:
        bool: True if the user can ask questions today, False otherwise.
    """
    today = get_today_key()
    count = user_log.get(user_id, {}).get(today, 0)
    return count < MAX_QUESTIONS_PER_DAY

def increment_user_count(user_id, user_log):
    """ 
    Increment the count of questions asked by the user today.
    """
    today = get_today_key()
    if user_id not in user_log:
        user_log[user_id] = {}
    user_log[user_id][today] = user_log[user_id].get(today, 0) + 1

