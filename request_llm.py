import requests
from openai import OpenAI
from scriptss.config import load_credentials, OPENAI_API, DEEPSEEK

creds = load_credentials(OPENAI_API)
open_ai_key = creds['open_ai']
client = OpenAI(api_key=open_ai_key)


def openai_context_json(system_prompt, user_promt):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": str(system_prompt)},
                {"role": "user", "content": str(user_promt)}
            ],
            response_format={ "type": "json_object" }
        )
        return completion.choices[0].message.content
    except requests.exceptions.RequestException as e:
        return f"Ошибка при выполнении запроса: {e}"


def openai_context_string(system_prompt, user_promt):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": str(system_prompt)},
                {"role": "user", "content": str(user_promt)}
            ]
        )
        return completion.choices[0].message.content
    except requests.exceptions.RequestException as e:
        return f"Ошибка при выполнении запроса: {e}"


creds = load_credentials(DEEPSEEK)
deepseek_key = creds['deepseek']

def deekpeek_context_string(system_prompt, user_prompt):
    try:
        client = OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com")

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
        ],
            temperature=0.7,
            stream=False
        )

        return response.choices[0].message.content
    except requests.exceptions.RequestException as e:
        return f"Ошибка при выполнении запроса: {e}"