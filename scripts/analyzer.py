import os
import requests
from google import genai


token = os.getenv("GITHUB_TOKEN")
repo = os.getenv("GITHUB_REPOSITORY")
pr_number = os.getenv("GITHUB_REF").split("/")[-1]
GEMINI_KEY = os.getenv("GEMINI_KEY")
client = genai.Client(api_key=GEMINI_KEY)

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

# Buscar dados do PR
pr_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
pr_response = requests.get(pr_url, headers=headers).json()

title = pr_response["title"]
body = pr_response["body"]

# Buscar arquivos alterados
files_url = pr_url + "/files"
files = requests.get(files_url, headers=headers).json()

diff_summary = ""
for file in files:
    diff_summary += f"\nArquivo: {file['filename']}\nPatch:\n{file.get('patch','')}\n"

prompt = f"""
Você é um engenheiro de QA senior.

Analise o Pull Request abaixo.

Título:
{title}

Descrição:
{body}

Alterações:
{diff_summary}

Tarefas:
1. Reescreva a descrição de forma mais clara e estruturada.
2. Sugira cenários de teste para QA.
3. Aponte possíveis riscos ou regressões.
"""

response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

analysis = response.text
print(analysis)
comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
response = requests.post(
    comment_url,
    headers=headers,
    json={"body": analysis}
)

print(response.status_code)
print(response.text)