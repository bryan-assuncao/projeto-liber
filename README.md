# Projeto Automação RH - Gmail API

## 🚀 O que faz
- Lê e-mails do Gmail com assunto `Candidatura - ...`
- Extrai Nome, Telefone e Vaga do corpo do e-mail
- Baixa anexos e salva na pasta `anexos/`
- Registra informações em `candidatos.xlsx`

## 📂 Estrutura
```
projeto_gmail/
│── main.py
│── credentials.json   # Baixe do Google Cloud Console
│── token.json         # Gerado automaticamente após login
│── anexos/
│── candidatos.xlsx
```

## 🔑 Configuração Google Cloud
1. Crie um projeto em [Google Cloud Console](https://console.cloud.google.com/)
2. Ative a **Gmail API**
3. Vá em **APIs & Services > OAuth consent screen** → configure como **External** e adicione seu e-mail em Test Users
4. Vá em **APIs & Services > Credentials > Create Credentials > OAuth Client ID**
5. Tipo de app: **Desktop app**
6. Baixe o JSON e salve como `credentials.json` na pasta do projeto

## ▶️ Como rodar
```bash
pip install -r requirements.txt
python main.py
```

Na primeira execução, o navegador vai abrir pedindo login e permissão.
Depois disso, será gerado um `token.json` que será usado nas próximas execuções.
