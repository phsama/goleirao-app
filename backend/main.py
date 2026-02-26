from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI(title="Goleirão App API")

# Setup CORS para permitir acesso do nosso frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "https://goleirao-app.vercel.app",
        "https://goleirao.com.br",
        "https://www.goleirao.com.br"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str

class NewsletterForm(BaseModel):
    email: EmailStr

# IMPORTANTE: Configure estas variáveis posteriormente no deploy
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "seuemail@gmail.com"  # Altere para o seu Gmail
SENDER_PASSWORD = "sua_senha_de_app" # Senha de app gerada na conta Google

def send_email_sync(subject: str, body: str, to_emails: list):
    """Função bloqueante para enviar o e-mail via SMTP."""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    try:
        # Quando for rodar valendo com as credenciais preenchidas, descomente o login e envio!
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        # server.login(SENDER_EMAIL, SENDER_PASSWORD)
        # server.send_message(msg)
        server.quit()
        print(f"E-mail simulado com sucesso! Assunto: {subject}")
    except Exception as e:
        print(f"Falha ao enviar e-mail: {e}")

@app.post("/api/newsletter")
async def signup_newsletter(form: NewsletterForm, background_tasks: BackgroundTasks):
    
    subject = "Você está na lista de espera do Goleirão!"
    body = f"""
    <html>
        <body>
            <h2>E aí, artilheiro!</h2>
            <p>Seu e-mail <strong>{form.email}</strong> foi cadastrado na nossa lista de espera.</p>
            <p>Avisaremos você assim que o App estiver no ar para nunca mais a sua pelada sofrer sem goleiro.</p>
            <br>
            <p>Abraços,<br>Equipe Goleirão 🧤</p>
        </body>
    </html>
    """
    # Envia o e-mail de confirmação sem travar a requisição do usuário
    background_tasks.add_task(send_email_sync, subject, body, [form.email])
    return {"message": "Inscrito com sucesso!"}


@app.post("/api/contact")
async def contact_us(form: ContactForm, background_tasks: BackgroundTasks):
    
    subject = f"Novo Contato - Goleirão App | De: {form.name}"
    body = f"""
    <html>
        <body>
            <h2>E-mail Recebido do Formulário do Goleirão</h2>
            <p><strong>Nome:</strong> {form.name}</p>
            <p><strong>E-mail:</strong> {form.email}</p>
            <p><strong>Mensagem:</strong><br>{form.message}</p>
        </body>
    </html>
    """
    # Envia email alertando o administrador (SENDER_EMAIL)
    background_tasks.add_task(send_email_sync, subject, body, [SENDER_EMAIL])
    return {"message": "Contato enviado com sucesso!"}
