# BoleirApp — Backend

Backend completo em **Python + FastAPI** para o site Acha Racha.

## Estrutura de arquivos

```
boleiro/
│
├── main.py                   ← Ponto de entrada. Roda o servidor.
├── seed.py                   ← Popula o banco com dados de exemplo
├── requirements.txt          ← Dependências Python
├── boleiro.html              ← Coloque aqui o arquivo do frontend
│
└── app/
    ├── database.py           ← Conexão com o banco (SQLite por padrão)
    ├── auth.py               ← JWT, hash de senha, verificação de token
    ├── schemas.py            ← Validação de dados (Pydantic)
    │
    ├── models/
    │   └── models.py         ← Tabelas do banco (SQLAlchemy)
    │
    └── routers/
        ├── auth.py           ← POST /auth/cadastro, POST /auth/login
        ├── jogos.py          ← GET/POST/PUT/DELETE /jogos
        └── inscricoes.py     ← POST /jogos/{id}/entrar, DELETE /jogos/{id}/sair
```

---

## Como rodar (passo a passo)

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Popular o banco com dados de exemplo

```bash
python seed.py
```

Isso cria o arquivo `boleiro.db` (SQLite) e insere os 8 rachões de exemplo.

### 3. Iniciar o servidor

```bash
uvicorn main:app --reload
```

O servidor vai rodar em: **http://localhost:8000**

### 4. Copiar o frontend

Coloque o arquivo `boleiro.html` na pasta raiz do projeto (junto com `main.py`).
Acesse **http://localhost:8000** e o site vai abrir automaticamente.

---

## Documentação automática da API

O FastAPI gera documentação interativa automaticamente:

- **Swagger UI**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc

Você pode testar todos os endpoints direto pelo navegador!

---

## Rotas disponíveis

### Autenticação
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/auth/cadastro` | Cria nova conta |
| POST | `/auth/login` | Login, retorna token JWT |
| GET | `/auth/me` | Dados do usuário logado |

### Jogos
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/jogos/` | Lista partidas (com filtros) |
| GET | `/jogos/{id}` | Detalhe de uma partida |
| POST | `/jogos/` | Anunciar novo racha (requer login) |
| PUT | `/jogos/{id}` | Editar racha (requer ser o dono) |
| DELETE | `/jogos/{id}` | Remover racha (requer ser o dono) |
| GET | `/jogos/meus/anunciados` | Meus rachões anunciados |

### Inscrições
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/jogos/{id}/entrar` | Entrar em um racha (requer login) |
| DELETE | `/jogos/{id}/sair` | Sair de um racha |
| GET | `/jogos/{id}/inscritos` | Ver inscritos (só o dono) |
| GET | `/jogos/meus/inscritos` | Rachões em que estou inscrito |

### Filtros disponíveis em GET /jogos/
```
?cidade=São Paulo - SP
?data=2025-06-21
?nivel=Intermediário
?tipo=Society
?posicao=Goleiro
?horario=manha   (ou tarde / noite)
```

---

## Para produção (opcional)

Troque o SQLite pelo PostgreSQL em `app/database.py`:

```python
DATABASE_URL = "postgresql://usuario:senha@localhost/boleiro"
```

E instale o driver:
```bash
pip install psycopg2-binary
```

---

## Usuário de teste (após rodar seed.py)

- **Email**: admin@boleiro.com
- **Senha**: boleiro123
