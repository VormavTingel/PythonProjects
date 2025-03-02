# Aplicativo de Backup Automático para Google Drive

Este projeto oferece uma forma simples de **fazer backup** de uma pasta local para o **Google Drive**, mantendo a estrutura de diretórios.  
Ele inclui:

- Uma **tela de Login** (usuário/senha locais do aplicativo).  
- Uma **tela de Backup** (permite selecionar a pasta e fazer o upload recursivo para o Drive).  
- Integração com a **API do Google Drive** via **PyDrive2**.  

---

## Sumário

1. [Recursos](#recursos)  
2. [Pré-requisitos](#pré-requisitos)  
3. [Instalação](#instalação)  
4. [Configuração da API do Google Drive](#configuração-da-api-do-google-drive)  
5. [Uso](#uso)  
6. [Estrutura do Projeto](#estrutura-do-projeto)  
7. [Funcionamento Interno](#funcionamento-interno)  
8. [Contribuindo](#contribuindo)  
9. [Licença](#licença)

---

## Recursos

- **Interface Gráfica** em Python (Tkinter + ttk).  
- **Login local** para controle de acesso ao app.  
- **Autenticação OAuth2** no Google Drive (arquivo `client_secrets.json` e tokens gerenciados pelo PyDrive2).  
- **Upload recursivo** de pastas e subpastas, preservando a estrutura no Drive.  
- **Mensagens de status** via messagebox (informando sucesso ou erro).  

---

## Pré-requisitos

- **Python 3.8+** (o projeto deve funcionar em 3.9, 3.10 etc.).  
- (Opcional) **Tkinter**: geralmente já vem instalado em muitas distribuições de Python. Em alguns sistemas Linux pode ser necessário:
  ```bash
  sudo apt-get install python3-tk
  ```
- **Conta Google** para gerar as credenciais do Drive no [Google Cloud Console](https://console.cloud.google.com/).  

---

## Instalação

1. **Clone** este repositório:

   ```bash
   git clone https://github.com/SEU_USUARIO/backup-drive.git
   cd backup-drive
   ```

2. **Crie e ative um ambiente virtual** (recomendado):

   ```bash
   # Linux/macOS
   python -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuração da API do Google Drive

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/).  
2. Crie um projeto (ou utilize um já existente) e habilite a **API do Google Drive**.  
3. Em **APIs e serviços** > **Credenciais**, crie um **OAuth client ID** (tipo “Desktop”) para liberar o fluxo OAuth.  
4. Baixe o arquivo `client_secrets.json` e coloque na **pasta raiz** do projeto.  
5. (Opcional) Adicione `client_secrets.json` ao **.gitignore** para evitar expor credenciais.  

---

## Uso

1. **Execute o aplicativo:**
   ```bash
   python main.py
   ```

2. **Login:**
   - Insira o **usuário** e **senha** cadastrados no aplicativo.
   - Clique em **Entrar** para acessar a tela de backup.

3. **Fazer o Backup:**
   - Escolha a **pasta** que deseja enviar ao Google Drive.
   - (Opcional) Insira um e-mail de referência (não é obrigatório).
   - Clique em **Fazer Backup**.
   - O navegador abrirá solicitando **autenticação OAuth** no Google Drive.
   - Após a autorização, os arquivos serão **enviados automaticamente**.

---

## Estrutura do Projeto

```bash
.
├── main.py                # Script principal (interface gráfica)
├── backup.py              # Funções de backup e integração com o Drive
├── auth.py                # Gerenciamento de autenticação do Google
├── README.md              # Documentação do projeto
├── requirements.txt       # Dependências do projeto
├── .gitignore             # Ignora arquivos sensíveis
└── client_secrets.json    # Arquivo de credenciais OAuth (não deve ser commitado)
```

---

## Funcionamento Interno

1. **Tela de Login**
   - O usuário digita **usuário e senha**.
   - O sistema valida e libera acesso à **tela de backup**.

2. **Tela de Backup**
   - O usuário seleciona uma pasta local e inicia o backup.
   - O programa autentica no Google Drive via **OAuth2**.
   - Os arquivos são enviados para o Drive **mantendo a estrutura original**.

3. **Autenticação no Google Drive**
   - O **PyDrive2** gerencia a autenticação.
   - O primeiro login gera um `credentials.json` para reutilização futura.
   - Se o token expirar, o sistema solicitará uma nova autenticação.

4. **Upload Recursivo**
   - O script percorre a pasta selecionada e **recria a estrutura** no Drive.
   - Todos os arquivos são enviados automaticamente.

---

## Contribuindo

Contribuições são bem-vindas! Para colaborar:

1. **Fork** este repositório.
2. Crie um **branch** para sua feature:
   ```bash
   git checkout -b minha-nova-feature
   ```
3. **Commit suas mudanças**:
   ```bash
   git commit -m "Adiciona nova funcionalidade X"
   ```
4. **Envie seu código**:
   ```bash
   git push origin minha-nova-feature
   ```
5. Abra um **Pull Request** e aguarde revisão. 🚀

---

