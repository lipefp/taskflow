# TaskFlow API

API REST para gerenciamento de tarefas pessoais, desenvolvida com Django e Django REST Framework.

Cada usuário acessa apenas suas próprias tarefas. A autenticação é feita via token e o status das tarefas segue um fluxo controlado.

---

## Stack

| Tecnologia | Função |
|---|---|
| Python + Django 6.0.5 | Framework principal |
| Django REST Framework | Camada de API |
| MariaDB | Banco de dados |
| Token Authentication | Autenticação |
| python-decouple | Variáveis de ambiente |

---

## Instalação

Pré-requisitos: Python 3.x e MariaDB rodando localmente.

```bash
git clone https://github.com/lipefp/taskflow
cd taskflow
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Configure o `.env` com suas credenciais antes de rodar:

```env
DEBUG=True
SECRET_KEY=sua-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
DB_NAME=taskflow
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=3306
```

---

## Endpoints

### Autenticação

| Método | Endpoint | Descrição |
|---|---|---|
| `POST` | `/api/accounts/register/` | Cadastrar usuário |
| `POST` | `/api/accounts/login/` | Login — retorna o token |

### Tarefas

Todos exigem o header `Authorization: Token <seu_token>`.

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/tasks/` | Listar tarefas |
| `POST` | `/api/tasks/` | Criar tarefa |
| `GET` | `/api/tasks/{id}/` | Detalhar tarefa |
| `PUT` | `/api/tasks/{id}/` | Atualizar tarefa completa |
| `PATCH` | `/api/tasks/{id}/` | Atualizar parcialmente |
| `DELETE` | `/api/tasks/{id}/` | Excluir tarefa |

Tentar acessar a tarefa de outro usuário retorna `403 Forbidden`.

---

## Filtros e Paginação

```
GET /api/tasks/?status=pending
GET /api/tasks/?status=in_progress
GET /api/tasks/?status=done
GET /api/tasks/?page=2
```

---

## Regras de Status

```
pending ──► in_progress ──► done
   │                          ▲
   └──────────────────────────┘
        (pulo direto permitido)
```

| De / Para | pending | in_progress | done |
|---|---|---|---|
| pending | — | ✅ | ✅ |
| in_progress | ❌ | — | ✅ |
| done | ❌ | ❌ | — |

Transições inválidas retornam `400 Bad Request`.

---

## Tratamento de Erros

`400 Bad Request` — campo obrigatório ausente:
```json
{
  "title": ["Este campo não pode ser vazio."]
}
```

`403 Forbidden` — acesso à tarefa de outro usuário:
```json
{
  "detail": "Você não tem permissão para realizar esta ação."
}
```