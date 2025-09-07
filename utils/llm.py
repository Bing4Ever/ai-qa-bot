from openai import OpenAI
import os
import base64
import json as jsonlib
from dotenv import load_dotenv
from prompts import ROLE_PROMPTS
from entities.invoice import Invoice

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_openai_with_role(messages, system_prompt, model="gpt-4o", temperature=0.7, max_tokens=500):
    full_messages = [{"role": "system", "content": system_prompt}] + messages
    try:
        return "This is a mock response"
    
        response = client.chat.completions.create(
            model=model,
            messages=full_messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"OpenAI 调用失败: {str(e)}"

    
def analyze_invoice_image_bytes(image_bytes) -> dict:
    prompt = ROLE_PROMPTS["Financial Advisor"]
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    image_url = f"data:image/png;base64,{base64_image}"

    test = """
    {
                                "invoice_date": "YYYY-MM-DD",
                                "issuer": "Store Name",
                                "total_amount": 123.45,
                                "items": [
                                {
                                    "description": "Product Name",
                                    "category": "Category Name",
                                    "amount": 12.34
                                },
                                {
                                    "description": "Another Product",
                                    "category": "Another Category",
                                    "amount": 56.78
                                    }
                                ]
                            }
    """
    result_json = jsonlib.loads(test)
    return result_json
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Please analyze this invoice image and return structured JSON data."
                    },
                    {
                        "type" :"image_url",
                        "image_url": 
                        {
                            "url": image_url,
                            "detail": "high"
                        }
                    }
                ]
            }
        ],
        temperature=0.0,
        max_tokens=800,
        response_format={ "type": "json_object" }
    )
    result_text = response.choices[0].message.content

    try:        
        result_json = jsonlib.loads(result_text)
        return result_json
    except jsonlib.JSONDecodeError:
        return {"error": "Failed to parse JSON", "raw_response": result_text}


    