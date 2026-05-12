# TaskFlow API

API REST de gerenciamento de tarefas pessoais desenvolvida como avaliação de onboarding backend.

Cada usuário gerencia apenas suas próprias tarefas, com autenticação via token e regras de negócio para controle de status.

---

## Stack

| Tecnologia | Função |
|---|---|
| Python + Django 6.0.5 | Framework principal |
| Django REST Framework | Camada de API |
| MariaDB | Banco de dados |
| Token Authentication | Autenticação stateless |
| python-decouple | Gerenciamento de variáveis de ambiente |

---

## Instalação

**Pré-requisitos:** Python 3.x e MariaDB rodando localmente.

```bash
git clone https://github.com/lipefp/taskflow
cd taskflow

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# edite o .env com suas credenciais do banco

python manage.py migrate
python manage.py runserver
```

### Variáveis de ambiente (.env)

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
| `POST` | `/api/accounts/register/` | Cadastrar novo usuário |
| `POST` | `/api/accounts/login/` | Login — retorna o token de acesso |

### Tarefas

Todos os endpoints abaixo exigem o header:
```
Authorization: Token <seu_token>
```

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/tasks/` | Listar tarefas do usuário autenticado |
| `POST` | `/api/tasks/` | Criar nova tarefa |
| `GET` | `/api/tasks/{id}/` | Detalhar uma tarefa |
| `PUT` | `/api/tasks/{id}/` | Atualizar tarefa completa |
| `PATCH` | `/api/tasks/{id}/` | Atualizar tarefa parcialmente |
| `DELETE` | `/api/tasks/{id}/` | Excluir tarefa |

> Tarefas de outros usuários retornam `404` — não `403` — para não vazar informação de existência do recurso.

---

## Filtros e Paginação

```bash
# Filtrar por status
GET /api/tasks/?status=pending
GET /api/tasks/?status=in_progress
GET /api/tasks/?status=done

# Navegar entre páginas
GET /api/tasks/?page=2
```

A resposta paginada tem o formato:
```json
{
    "count": 10,
    "next": "http://127.0.0.1:8000/api/tasks/?page=2",
    "previous": null,
    "results": [...]
}
```

---

## Regras de Transição de Status

Uma tarefa nasce com status `pending` e só pode avançar — nunca voltar.

```
pending ──► in_progress ──► done
   │                          ▲
   └──────────────────────────┘
        (pulo direto permitido)
```

| De / Para | `pending` | `in_progress` | `done` |
|---|---|---|---|
| `pending` | — | ✅ | ✅ |
| `in_progress` | ❌ | — | ✅ |
| `done` | ❌ | ❌ | — |

Transições inválidas retornam `400 Bad Request` com mensagem descritiva:
```json
{
    "status": ["Transição inválida de done para pending."]
}
```

---

## Exemplos de uso

**Registrar usuário**
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "felipe", "password": "senha123"}'
```

**Login**
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "felipe", "password": "senha123"}'
# → {"token": "abc123..."}
```

**Criar tarefa**
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Authorization: Token abc123..." \
  -H "Content-Type: application/json" \
  -d '{"title": "Estudar DRF", "due_date": "2026-05-30"}'
```

**Atualizar status**
```bash
curl -X PATCH http://127.0.0.1:8000/api/tasks/1/ \
  -H "Authorization: Token abc123..." \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'
```