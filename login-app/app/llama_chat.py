# llama_chat.py
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "prompt_sistema.txt")
with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    PROMPT_INICIAL = f.read()

# Simulando estructura Hugging Face
class FakeTokenizer:
    def __init__(self):
        pass
    def encode(self, text, return_tensors=None):
        return text
    def decode(self, tokens):
        return tokens

class FakeModel:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    def generate(self, prompt, max_new_tokens=500, temperature=0.7):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": PROMPT_INICIAL},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_new_tokens
        )
        return response.choices[0].message.content

# Instancias como si fueran de transformers
tokenizer = FakeTokenizer()
model = FakeModel(api_key=os.getenv("OPENAI_API_KEY"))

# Método de entrada desde app.py
def generar_respuesta_llama(pregunta_usuario):
    return model.generate(pregunta_usuario)
