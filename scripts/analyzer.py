import os
import requests
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

repo = os.getenv("GITHUB_REPOSITORY")
token = os.getenv("GITHUB_TOKEN")
pr_number = os.getenv("GITHUB_REF").split("/")[-1]

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

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
)

analysis = response.choices[0].message.content

# Comentar no PR
comment_url = pr_url + "/comments"
requests.post(
    comment_url,
    headers=headers,
    json={"body": f"## 🤖 AI PR Analysis\n\n{analysis}"}
)