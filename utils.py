from openai import OpenAI
import os
import base64
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_openai_with_role(messages, system_prompt, model="gpt-3.5-turbo", temperature=0.7, max_tokens=500):
    full_messages = [{"role": "system", "content": system_prompt}] + messages
    try:
        #return "This is a mock response"
    
        response = client.chat.completions.create(
            model=model,
            messages=full_messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"OpenAI 调用失败: {str(e)}"

def ask_openai_with_image(message, system_prompt, image_file, model="gpt-4o", temperature=0.7, max_tokens=500):

    try:
        # Convert image to base64
        image_bytes = image_file.getvalue()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        image_url = f"data:image/png;base64,{base64_image}"

        full_message = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": message},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ]

        #return "This is a mock response"+image_file.name

        response = client.chat.completions.create(
            model=model,
            messages=full_message,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"