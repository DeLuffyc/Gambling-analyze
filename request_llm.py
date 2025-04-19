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

def prompt_with_web_search(user_prompt, system_prompt=None):
    try:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})

        response = client.responses.create(
            model="gpt-4o-mini",  # или "gpt-4o-search-preview"
            tools=[{"type": "web_search_preview"}],
            input=messages
        )
        def extract_answer(response):
            for item in response.output:
                if getattr(item, 'type', None) == 'message' and getattr(item, 'role', None) == 'assistant':
                    if item.content and len(item.content) > 0:
                        return item.content[0].text
            return None

        answer = extract_answer(response)
        return answer

    except Exception as e:
        return f"Ошибка при выполнении запроса: {type(e).__name__}: {e}"


