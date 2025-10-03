import os
import base64
import re
from openpyxl import Workbook, load_workbook
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do .env

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

ANEXOS_DIR = "anexos"
PLANILHA = "candidatos.xlsx"
os.makedirs(ANEXOS_DIR, exist_ok=True)

CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS", "credentials.json")
TOKEN_FILE = os.getenv("GOOGLE_TOKEN", "token.json")

def autenticar_gmail():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return creds

def extrair_dados(corpo):
    nome = re.search(r"(Nome[:]?|Nome completo[:]?)(.*)", corpo)
    telefone = re.search(r"Telefone[:]? (.*)", corpo)
    vaga = re.search(r"Vaga[:]? (.*)", corpo)

    return {
        "nome": nome.group(2).strip() if nome else "Não encontrado",
        "telefone": telefone.group(1).strip() if telefone else "Não encontrado",
        "vaga": vaga.group(1).strip() if vaga else "Não encontrada"
    }

def registrar_planilha(dados, anexo):
    if os.path.exists(PLANILHA):
        wb = load_workbook(PLANILHA)
        ws = wb.active
    else:
        wb = Workbook()
        ws = wb.active
        ws.append(["Nome", "Telefone", "Vaga", "Anexo"])

    ws.append([dados["nome"], dados["telefone"], dados["vaga"], anexo or "SEM ANEXO"])
    wb.save(PLANILHA)

def salvar_anexo(service, msg_id, part):
    if 'body' in part and 'attachmentId' in part['body']:
        att_id = part['body']['attachmentId']
        att = service.users().messages().attachments().get(userId="me", messageId=msg_id, id=att_id).execute()
        data = base64.urlsafe_b64decode(att['data'].encode('UTF-8'))
        filename = part['filename'] or "anexo.pdf"
        filepath = os.path.join(ANEXOS_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(data)
        return filepath
    return None

def processar_emails(service):
    results = service.users().messages().list(userId="me", q="subject:Candidatura").execute()
    mensagens = results.get("messages", [])

    for msg in mensagens:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        payload = msg_data["payload"]
        headers = payload["headers"]
        assunto = next(h["value"] for h in headers if h["name"] == "Subject")
        print(f"\n📧 Processando: {assunto}")

        partes = payload.get("parts", [])
        corpo = ""
        for part in partes:
            if part.get("mimeType") == "text/plain":
                corpo = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
        
        dados = extrair_dados(corpo)
        print(f"-> Dados extraídos: {dados}")

        anexo_salvo = None
        for part in partes:
            if "filename" in part and part["filename"]:
                anexo_salvo = salvar_anexo(service, msg["id"], part)
                print(f"-> Anexo salvo em: {anexo_salvo}")

        registrar_planilha(dados, anexo_salvo)
        print("✅ Registro adicionado na planilha.")

if __name__ == "__main__":
    try:
        creds = autenticar_gmail()
        service = build("gmail", "v1", credentials=creds)
        processar_emails(service)
        print("\n🎉 Processamento concluído! Verifique candidatos.xlsx")
    except HttpError as error:
        print(f"❌ Ocorreu um erro: {error}")
