# Automação de Processamento de Candidaturas 

Este projeto automatiza a leitura de e-mails de candidaturas recebidos no Gmail, extrai dados como nome, telefone e vaga, salva anexos e registra tudo em uma planilha Excel.

---

## Demonstração

<video src="video.mp4" controls width="600"></video>

Se o vídeo não rodar no seu navegador, você pode baixar e assistir localmente, ou assistir online no YouTube:  
[Vídeo no YouTube](https://www.youtube.com/watch?v=2FLH48IfD0U)

---

## Fluxograma / Diagrama

Você pode ver o fluxo de funcionamento do sistema em um diagrama interativo no Excalidraw:

[Diagrama no Excalidraw](https://excalidraw.com/#room=04bc62a6d15446692d9e,Wjl8_7ug7jJgNW6ZwkjOvg)

---

## Tecnologias utilizadas

- Python 3.x  
- Google Gmail API  
- openpyxl para leitura/escrita de arquivos Excel  
- dotenv para uso de variáveis de ambiente  
- regex para extração de informações em texto  

---

## Como funciona (fluxo resumido)

1. Autentica no Gmail via OAuth2.  
2. Busca e-mails não lidos (até 50 por execução).  
3. Para cada e-mail:
   - Extrai nome, telefone e vaga do corpo ou do assunto.  
   - Salva anexos, se existirem.  
   - Registra dados na planilha `candidatos.xlsx`.  
   - Marca o e-mail como lido.  

---

## Estrutura do projeto

```
seu_projeto/
├── anexos/               # pasta onde anexos são salvos
├── candidatos.xlsx       # planilha gerada com os dados
├── credentials.json      # credenciais da API Gmail
├── token.json            # token gerado após autenticação
├── .env                  # variáveis de ambiente
├── script.py             # script principal da automação
├── video.mp4             # vídeo de demonstração (para execução local)
└── README.md             # este arquivo
```

---

## Pré‑requisitos

- Conta Google com Gmail API habilitada no Google Cloud Console.  
- Arquivo `credentials.json` com credenciais OAuth2.  
- Instalar dependências Python:

```bash
pip install -r requirements.txt
```

---

## Como executar

1. Configure o `.env` (opcional, mas recomendado):

```env
GOOGLE_CREDENTIALS=credentials.json
GOOGLE_TOKEN=token.json
```

2. Execute:

```bash
python script.py
```

---

## Melhorias futuras

- Uso de banco de dados (SQLite, PostgreSQL).  
- Validação mais rígida de nome, telefone e e-mail.  
- Interface web para revisão manual dos candidatos.  
- Agendamento automático (cron, cloud).  

---
