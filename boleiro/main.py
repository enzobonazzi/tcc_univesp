# main.py — ponto de entrada da aplicação
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.database import engine
from app.models.models import Base
from app.routers import auth, jogos, inscricoes

# Cria as tabelas no banco automaticamente ao iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BoleirApp API",
    description="Backend do Acha Racha — encontre e anuncie rachões de futebol",
    version="1.0.0",
)

# ─── CORS ────────────────────────────────────────────────────
# Permite que o frontend (arquivo HTML aberto no navegador) chame a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Em produção, troque por ["https://seudominio.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── ROTAS ───────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(jogos.router)
app.include_router(inscricoes.router)

# ─── SERVE O FRONTEND ────────────────────────────────────────
# O arquivo boleiro.html fica na raiz do projeto.
# Acesse http://localhost:8000 e o próprio servidor entrega o site.
@app.get("/", include_in_schema=False)
def serve_frontend():
    html_path = os.path.join(os.path.dirname(__file__), "boleiro.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"mensagem": "Coloque o arquivo boleiro.html na raiz do projeto"}

@app.get("/health")
def health():
    return {"status": "ok", "app": "BoleirApp"}
