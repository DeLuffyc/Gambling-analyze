import os
import json

def load_credentials(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.loads(file.read())
    return data


DB_CREDENTIALS = 'credentials/postgresql.json'

TGRM_BOT_CREDENTIALS = 'credentials/tg.json'

OPENAI_API = 'credentials/cred_llm.json'
DEEPSEEK = 'credentials/cred_llm.json'
PERPLEXITY = 'credentials/cred_llm.json'

TG_LOG = 'credentials/tg_log.json'
