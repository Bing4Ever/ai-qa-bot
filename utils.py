from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_openai(prompt, model="gpt-4.1", temperature=0.7, max_tokens=500):
    """
    Function to ask OpenAI's API a question and return the response.
    
    Args:
        prompt (str): The question to ask.
        model (str): The model to use for the request.
        
    Returns:
        str: The response from OpenAI's API.
    """
    try:
        message = [{
            "role": "user", 
            "content": prompt,
            }]
        response = client.chat.completions.create(
            model=model,
            messages=message,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"