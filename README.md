# Offroad Alert API

Este projeto é uma API para alertas de emergência usando FastAPI. Ele permite que os usuários enviem suas localizações e enviem emails de emergência para contatos de emergência.

## Configuração

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)
- Ambiente virtual (recomendado)

### Instalação

1. Clone o repositório:

    ```sh
    git clone https://github.com/seu-usuario/offroad-alert-api.git
    cd offroad-alert-api
    ```

2. Crie e ative um ambiente virtual:

    ```sh
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

3. Instale as dependências:

    ```sh
    pip install -r requirements.txt
    ```

4. Crie um arquivo `.env` na raiz do projeto e adicione suas credenciais de email:

    ```env
    EMAIL_USER=your_email@gmail.com
    EMAIL_PASSWORD=your_app_password
    ```

    - `EMAIL_USER`: Seu endereço de email que será usado para enviar os emails de emergência.
    - `EMAIL_PASSWORD`: A senha do seu email. Se você estiver usando o Gmail e tiver a verificação em duas etapas ativada, use uma senha de app. Para criar uma senha de app, siga as instruções neste [link](https://support.google.com/accounts/answer/185833?hl=pt-BR).

### Executando a Aplicação

Para iniciar a aplicação, execute o seguinte comando:

```sh
uvicorn main:app --reload