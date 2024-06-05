from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

resposta = client.chat.completions.create(
    messages=[
        {"role":"system","content":"Listar apenas os nomes dos produtos, sem adicionar descrição"},
        {"role":"user","content":"Liste 3 produtos sustentáveis"}
    ],
    model="gpt-4",
    temperature=0,
    max_tokens=200,
    n = 3
)
for contador in range(0,3):
    print(resposta.choices[0].message.content)