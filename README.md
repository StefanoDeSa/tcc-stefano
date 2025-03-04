# 🔐 SSO Authentication - 2FA (Google Authenticator)

Este projeto faz parte do **TCC** e tem como objetivo a **implementação de um Servidor SSO (Single Sign-On)** com autenticação em **2 etapas (Email e OTP)** utilizando **Google Authenticator**.

## 🚀 Tecnologias Utilizadas

- **Python 3.x**
- **Django**
- **PyOTP** (para geração e verificação do código OTP)
- **Pillow** (para manipulação de imagens)
- **QRCode** (para gerar QR Codes do OTP)
- **Bootstrap 5** (para estilização das telas)

---

## 🛠️ **Instalação e Configuração**

Siga os passos abaixo para clonar e rodar o projeto localmente.

### 🔹 1. Clone o Repositório

```bash
git clone https://github.com/StefanoDeSa/tcc-stefano.git
cd tcc-stefano
```

### 🔹 2. Crie e Ative o Ambiente Virtual

```bash
py -m venv venv
```

Ative a virtualenv:

- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **Linux/Mac**:
  ```bash
  source venv/bin/activate
  ```

### 🔹 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 🔹 4. Aplique as Migrações do Banco de Dados

```bash
py manage.py migrate
```

### 🔹 5. Inicie o Servidor Django

```bash
py manage.py runserver
```

Agora, acesse [**127.0.0.1:8000**](http://127.0.0.1:8000/) no navegador. 🚀

---

## 🏆 **Funcionalidades**

✅ Autenticação de usuários com **E-mail e Senha**\
✅ Implementação do **2FA (Autenticação de Dois Fatores) com Google Authenticator**\

---

## 📝 **Sobre o Projeto**

Este projeto foi desenvolvido como parte do **Trabalho de Conclusão de Curso (TCC)** e tem como objetivo explorar a implementação de **SSO (Single Sign-On) com 2FA** em aplicações web modernas.

---

## 📜 **Licença**

Este projeto está licenciado sob a **MIT License**. Veja o arquivo [`LICENSE`](LICENSE) para mais detalhes.

---

