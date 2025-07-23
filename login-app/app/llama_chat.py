import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "prompt_sistema.txt")
with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    PROMPT_INICIAL = f.read()

# Cliente OpenAI (nuevo estilo)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generar_respuesta_llama(pregunta_usuario):
    try:
        respuesta = client.chat.completions.create(
            model="gpt-3.5-turbo",  # o "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": PROMPT_INICIAL},
                {"role": "user", "content": pregunta_usuario}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return respuesta.choices[0].message.content
    except Exception as e:
        return f"❌ Error modelo LLaMA entrenado: {str(e)}"
