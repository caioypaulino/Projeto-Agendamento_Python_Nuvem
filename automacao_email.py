import os
import smtplib
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

import requests # pip install requests
from dotenv import load_dotenv # pip install python-dotenv
from todoist_api_python.api import TodoistAPI # pip install todoist-api-python

# Carrega variáveis de ambiente do arquivo .env
def load_environment_variables():
    try:
        # Tenta o get do diretório onde o script está.
        # Vai funcionar quando o script for executado como arquivo.
        script_dir = Path(__file__).resolve().parent
    except NameError:
        # Se __file__ não estiver definada, get cwd.
        script_dir = Path(os.getcwd())

    env_file_path = script_dir / ".env"
    load_dotenv(env_file_path)

# Retorna os artigos de notícias mais recentes contendo a palavra-chave 'tech' através da api do site mediastack.
def get_news(news_api_key):
    try:
        params = {
            "access_key": news_api_key,
            "keywords": "tecnologia",
            "languages": "pt",
            "sort": "published_desc",
            # "date"
            "limit": 3,
        }

        response = requests.get("https://api.mediastack.com/v1/news", params=params)
        response.raise_for_status()
        news_items = response.json()["data"]

        news_text = "\n\n".join(
            f"Titulo: {item.get('title', 'No title provided')}\n"
            f"Descrição: {item.get('description', 'No description provided')}\n"
            f"URL: {item.get('url', 'No URL provided')}"
            for item in news_items
        )

        return news_text
    except requests.RequestException as ex:
        return f"As informações de notícias estão indisponíveis no momento. Error: {ex}"

# Retorna o clima atual para uma determinada cidade e país através da api do site weatherbit.
def get_weather(api_key, city_name, country_code):
    try:
        api_url = f"https://api.weatherbit.io/v2.0/current?city={city_name}&country={country_code}&key={api_key}"
        response = requests.get(api_url)
        response.raise_for_status()

        weather_data = response.json()["data"][0]
        weather_report = (
            f"Atualmente, o clima em {weather_data['city_name']}, {weather_data['country_code']} "
            f"é {weather_data['temp']}°C com {weather_data['weather']['description']}."
        )
        return weather_report
    except requests.RequestException:
        return f"As informações meteorológicas estão indisponíveis no momento."

# Recupera tarefas abertas do Todoist.
def get_tasks(todoist_api_key):
    try:
        api = TodoistAPI(todoist_api_key)
        tasks = api.get_tasks()
        tasks_content = [task.content for task in tasks]
        return f"Aqui estão suas tarefas abertas: {', '.join(tasks_content)}"
    except Exception:
        return "Não foi possível recuperar tarefas."

# Envia um e-mail usando o servidor SMTP especificado e credenciais de login
def send_email(sender, recipient, subject, message_body, smtp_server, smtp_port, password):
    try:
        email = EmailMessage()
        email["From"] = sender
        email["To"] = recipient
        email["Subject"] = subject
        email.set_content(message_body)

        with smtplib.SMTP(smtp_server, port=smtp_port) as smtp:
            smtp.starttls()
            smtp.login(sender, password)
            smtp.send_message(email)

        return "Email enviado com sucesso!"
    except Exception as ex:
        return f"Falha ao enviar e-mail. Erro: {ex}"

def main():
    load_environment_variables()

    # Recupera dados sensíveis
    news_api_key = os.getenv("NEWS_API_KEY")
    # todoist_api_key = os.getenv("TODOIST_API_KEY")
    weather_api_key = os.getenv("WEATHER_API_KEY")
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")

    # Email config
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

    news = get_news(news_api_key)
    weather = get_weather(weather_api_key, "Rio de Janeiro", "BR")
    ##tasks = get_tasks(todoist_api_key)

    # Create the email body with separated sections
    message_body = (
        "Bom dia! Aqui está sua atualização:\n\n"
        "---- NOTÍCIAS ----\n\n"
        f"{news}\n\n"
        "---- CLIMA ----\n\n"
        f"{weather}\n\n"
        #"---- TO-DO LIST ----\n\n"
        #f"{tasks}\n"

    )

    # Envia o e-mail ao remetente
    email_status = send_email(
        sender=sender,
        recipient=sender,  # me enviando
        subject="Sua atualização matinal 🚀",
        message_body=message_body,
        smtp_server=SMTP_SERVER,
        smtp_port=SMTP_PORT,
        password=password,
    )
    print(email_status)


if __name__ == "__main__":
    main()

