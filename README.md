# TaskFlow

API REST para gerenciamento de tarefas pessoais, construída com **Django REST Framework** e autenticação por token.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-%23a30000.svg?style=for-the-badge&logo=django&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)

---

## Sobre

TaskFlow é uma API para criar, listar e acompanhar tarefas, com controle de fluxo de
status e mensagens de erro em português. Cada usuário só enxerga e altera as próprias tarefas.

### Funcionalidades

- 🔐 Autenticação por **Token** (DRF Token Auth)
- ✅ CRUD de tarefas
- 🔄 Transição de status controlada: `PENDENTE` → `EM_PROGRESSO` → `CONCLUIDA` (estado final)
- 🔎 Filtro por status
- 📄 Paginação (`PageNumberPagination`)
- 🇧🇷 Respostas e erros em português (`LANGUAGE_CODE = 'pt-br'`)
- 🚫 Tratamento de acesso negado (HTTP 403) para tarefas de outros usuários

---

## Stack

- **Python** + **Django** + **Django REST Framework**
- **MariaDB**
- Autenticação: DRF Token Authentication

---

## Como rodar

> Ajuste os comandos abaixo ao seu `settings.py` / `requirements.txt` reais.

```bash
# clonar
git clone https://github.com/lipefp/taskflow.git
cd taskflow

# ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows

# dependências
pip install -r requirements.txt

# banco (MariaDB) — configure as credenciais em settings.py / .env antes
python manage.py migrate

# usuário admin (opcional)
python manage.py createsuperuser

# subir o servidor
python manage.py runserver
```

A API fica disponível em `http://127.0.0.1:8000/`.

---

## Autenticação

Obtenha um token e use-o no header das requisições:

```bash
# obter token
curl -X POST http://127.0.0.1:8000/api-token-auth/ \
  -d "username=SEU_USER&password=SUA_SENHA"

# usar o token
curl http://127.0.0.1:8000/api/tasks/ \
  -H "Authorization: Token SEU_TOKEN_AQUI"
```

---

## Endpoints

> Tabela de referência — alinhe com o seu `urls.py`.

| Método | Rota | Descrição |
| --- | --- | --- |
| `POST` | `/api-token-auth/` | Retorna o token de autenticação |
| `GET` | `/api/tasks/` | Lista as tarefas do usuário (paginada) |
| `GET` | `/api/tasks/?status=PENDENTE` | Filtra por status |
| `POST` | `/api/tasks/` | Cria uma tarefa |
| `GET` | `/api/tasks/{id}/` | Detalha uma tarefa |
| `PATCH` | `/api/tasks/{id}/` | Atualiza (inclui transição de status) |
| `DELETE` | `/api/tasks/{id}/` | Remove uma tarefa |

---

## Testes

Coleção testada com **Bruno** (alternativa open-source ao Postman).

---

## Autor

**Felipe Diniz** · [GitHub](https://github.com/lipefp) · [LinkedIn](https://www.linkedin.com/in/felipe-diniz-39237b288)
