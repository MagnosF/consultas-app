## 🩺 Consultas Médicas — Sistema de Agendamento e Gerenciamento

- Este projeto consiste no desenvolvimento de um aplicativo mobile para agendamento e gerenciamento de consultas médicas, com backend em FastAPI e frontend em React Native (Expo).
O sistema permite o cadastro e autenticação de usuários com perfis diferenciados (paciente, médico e administrador), além de oferecer funcionalidades de agendamento, cancelamento, histórico e notificações.

## ✨ Funcionalidades Principais

### 👤 Gestão de Usuários
- **Cadastro e autenticação** com perfis diferenciados (paciente, médico, administrador)
- **Controle de acesso** baseado em tipos de usuário
- **Sessão segura** com tokens JWT

### 📅 Agendamento
- **Agendar consultas** com médicos disponíveis
- **Cancelar** agendamentos
- **Visualizar histórico** de atendimentos
- **Notificações** e lembretes automáticos


## 🛠 Stack Tecnológica

### 💻 Backend (API)
- **Python 3.10+** • **FastAPI** • **Uvicorn**
- **MySQL** • **SQLAlchemy ORM**
- **Passlib** (hash de senhas) • **Python-JOSE** (JWT)

### 📱 Frontend (Mobile)
- **React Native** • **Expo Go** • **Axios**
- **React Navigation** • **Async Storage**

## 📁 Estrutura de Pastas
consultas-medicas/
├── 📱 consultas-app/ # Frontend (React Native + Expo)
│ ├── src/
│ │ ├── Screens/ # Telas (Login, Cadastro, Agenda)
│ │ ├── components/ # Componentes reutilizáveis
│ │ ├── routes/ # Configuração de navegação
│ │ ├── services/ # API (Axios)
│ │ ├── context/ # Contextos globais
│ │ ├── styles/ # Estilos
│ │ └── utils/ # Funções auxiliares
│ ├── App.js
│ └── package.json
│
└── 🖥️ consultas-api/ # Backend (FastAPI)
├── app/
│ ├── database/ # Conexão com banco
│ ├── models/ # Modelos ORM
│ ├── schemas/ # Validação (Pydantic)
│ ├── routes/ # Endpoints da API
│ ├── core/ # Configurações principais
│ └── services/ # Lógica de negócio
├── main.py # Ponto de entrada
├── requirements.txt # Dependências
└── .env # Variáveis de ambiente

## 🚀 Configuração e Instalação

### Pré-requisitos
- **Node.js** (versão LTS)
- **Python 3.10+**
- **MySQL**
- **Expo Go** no celular

## 🖥️ Backend (FastAPI)
### 🔹 1. Crie o ambiente virtual
- cd consultas-api
- python -m venv venv
- venv\Scripts\activate   # (Windows)
# ou
- source venv/bin/activate  # (Linux/Mac)

### 🔹 2. Instale as dependências
- pip install -r requirements.txt

### 🔹 3. Configure o banco de dados MySQL

- Crie um banco no MySQL:

- CREATE DATABASE consultasdb;

- Crie o arquivo .env dentro de consultas-api/:

- DB_USER=root
- DB_PASSWORD=sua_senha
- DB_HOST=localhost
- DB_NAME=consultasdb
- SECRET_KEY=chave_super_secreta
- ALGORITHM=HS256
- ACCESS_TOKEN_EXPIRE_MINUTES=60

### 🔹 4. Execute o servidor
- uvicorn main:app --reload


- 📍 Acesse: http://127.0.0.1:8000/docs

## 📱 Frontend (React Native + Expo)
### 🔹 1. Crie e entre no projeto
- cd consultas-app
- npx expo start

### 🔹 2. Instale as dependências
- npm install axios @react-navigation/native @react-navigation/stack
- npx expo install react-native-screens react-native-safe-area-context
- npm install @react-native-async-storage/async-storage

### 🔹 3. Configure o Axios

- Edite o arquivo src/services/api.js:

- import axios from "axios";

const api = axios.create({
  baseURL: "http://10.0.2.2:8000", // emulador Android
  // ou use o IP local: "http://192.168.x.x:8000"
});

export default api;

### 🔹 4. Execute o app
- npx expo start


- Escaneie o QR Code com o app Expo Go no celular 📱

### 🔐 Funcionalidades Principais
## Módulo	Descrição
- 👤 Cadastro de Usuário	Registro de pacientes, médicos e administradores
- 🔑 Login / Autenticação	JWT Tokens e controle de sessão
- 📅 Agendamento	Criar, listar e cancelar consultas
- 🧾 Histórico	Visualizar atendimentos anteriores
- 🔔 Notificações	Lembretes e avisos automáticos
- ⚙️ Perfis de Acesso	Controle de permissões por tipo de usuário


### 🧰 Comandos Úteis
## Limpar cache do Expo:

- npx expo start -c


## Rodar backend com reload automático:

- uvicorn main:app --reload


## Atualizar dependências:

- pip install --upgrade -r requirements.txt

## 🧑‍💻 Desenvolvido por
Magno Ferreira Santos

- 📘 Projeto acadêmico: Cadastro e Gerenciamento de Usuários (Consultas Médicas)
- 🎓 Curso: Análise e Desenvolvimento de Sistemas
- 🏫 Instituição: Projeção — 2025