import os
from pathlib import Path
from dotenv import load_dotenv  # pip install python-dotenv

# Determina o diretório script ou diretório de trabalho atual
script_dir = Path.cwd()
env_file_path = script_dir / ".env"
gitignore_file_path = script_dir / ".gitignore"

# Cria um arquivo . env com o conteúdo especificado
def create_env_file(env_file_path):
    env_content = """TEST_KEY=MyPassword123
                    NEWS_API_KEY=<INPUT_YOUR_KEY_HERE>
                    TODOIST_API_KEY=<INPUT_YOUR_KEY_HERE>
                    WEATHER_API_KEY=<INPUT_YOUR_KEY_HERE>
                    EMAIL_SENDER=<YOUR_EMAIL>
                    EMAIL_PASSWORD=<YOUR_EMAIL_PASSWORD>
                    """
    with env_file_path.open(mode="w") as file:
        file.write(env_content)

# Cria um arquivo .gitignore e ignora o arquivo .env
def create_gitignore_file(gitignore_file_path):
    gitignore_content = """.env
                        # Python cache files
                        __pycache__/
                        *.pyc

                        # OS generated files
                        .DS_Store
                        Thumbs.db

                        # Jupyter notebook checkpoint directories
                        .ipynb_checkpoints/
                        """
    with gitignore_file_path.open(mode="w") as file:
        file.write(gitignore_content)

# Cria o arquivo .env se não existe
if not env_file_path.exists():
    create_env_file(env_file_path)

# Cria o arquivo .gitignore se não existe
if not gitignore_file_path.exists():
    create_gitignore_file(gitignore_file_path)

# Carrega variáveis de ambiente do arquivo .env
load_dotenv(env_file_path)

# os.getenv para ler as variáveis de ambiente
TEST_KEY = os.getenv('TEST_KEY')
TEST_KEY