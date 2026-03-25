# app/schemas.py
from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Optional
from datetime import datetime


# ─── USUÁRIO ────────────────────────────────────────────────
class UsuarioCriar(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    telefone: Optional[str] = None

class UsuarioResposta(BaseModel):
    id: int
    nome: str
    email: str
    telefone: Optional[str]
    criado_em: datetime

    model_config = {"from_attributes": True}

class LoginResposta(BaseModel):
    access_token: str
    token_type: str
    usuario: UsuarioResposta


# ─── JOGO ───────────────────────────────────────────────────
class JogoCriar(BaseModel):
    nome: str
    cidade: str
    local: str
    data: str          # "2025-06-21"
    hora: str          # "19:00"
    nivel: str         # Básico | Intermediário | Avançado
    tipo: str          # Society | Futsal | Campo | Pelada aberta
    vagas: int
    total_vagas: int
    posicoes: List[str]
    descricao: Optional[str] = ""

    @field_validator("nivel")
    @classmethod
    def nivel_valido(cls, v):
        opcoes = ["Básico", "Intermediário", "Avançado"]
        if v not in opcoes:
            raise ValueError(f"Nível deve ser um de: {opcoes}")
        return v

    @field_validator("tipo")
    @classmethod
    def tipo_valido(cls, v):
        opcoes = ["Society", "Futsal", "Campo", "Pelada aberta"]
        if v not in opcoes:
            raise ValueError(f"Tipo deve ser um de: {opcoes}")
        return v

    @field_validator("vagas")
    @classmethod
    def vagas_positivas(cls, v):
        if v < 1:
            raise ValueError("Vagas deve ser pelo menos 1")
        return v


class JogoResposta(BaseModel):
    id: int
    nome: str
    cidade: str
    local: str
    data: str
    hora: str
    nivel: str
    tipo: str
    vagas: int
    total_vagas: int
    posicoes: List[str]
    descricao: Optional[str]
    urgente: bool
    ativo: bool
    criado_em: datetime
    anunciante_id: int
    anunciante_nome: Optional[str] = None
    anunciante_telefone: Optional[str] = None
    total_inscritos: int = 0

    model_config = {"from_attributes": True}


# ─── INSCRIÇÃO ──────────────────────────────────────────────
class InscricaoCriar(BaseModel):
    posicao: Optional[str] = "Qualquer"

class InscricaoResposta(BaseModel):
    id: int
    usuario_id: int
    jogo_id: int
    posicao: Optional[str]
    inscrito_em: datetime

    model_config = {"from_attributes": True}
