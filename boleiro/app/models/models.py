# app/models/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id         = Column(Integer, primary_key=True, index=True)
    nome       = Column(String(100), nullable=False)
    email      = Column(String(150), unique=True, index=True, nullable=False)
    senha_hash = Column(String(200), nullable=False)
    telefone   = Column(String(20), nullable=True)
    criado_em  = Column(DateTime, default=datetime.utcnow)

    # Um usuário pode anunciar vários jogos
    jogos_anunciados = relationship("Jogo", back_populates="anunciante")
    # Um usuário pode se inscrever em vários jogos
    inscricoes = relationship("Inscricao", back_populates="usuario")


class Jogo(Base):
    __tablename__ = "jogos"

    id           = Column(Integer, primary_key=True, index=True)
    nome         = Column(String(150), nullable=False)
    cidade       = Column(String(100), nullable=False)
    local        = Column(String(200), nullable=False)
    data         = Column(String(10),  nullable=False)   # formato: "2025-06-21"
    hora         = Column(String(5),   nullable=False)   # formato: "19:00"
    nivel        = Column(String(20),  nullable=False)   # Básico | Intermediário | Avançado
    tipo         = Column(String(30),  nullable=False)   # Society | Futsal | Campo | Pelada aberta
    vagas        = Column(Integer,     nullable=False)
    total_vagas  = Column(Integer,     nullable=False)
    posicoes     = Column(String(200), nullable=False)   # "Meia,Ponta,Goleiro"
    descricao    = Column(Text,        nullable=True)
    urgente      = Column(Boolean,     default=False)
    ativo        = Column(Boolean,     default=True)
    criado_em    = Column(DateTime,    default=datetime.utcnow)

    anunciante_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    anunciante    = relationship("Usuario", back_populates="jogos_anunciados")
    inscricoes    = relationship("Inscricao", back_populates="jogo")


class Inscricao(Base):
    __tablename__ = "inscricoes"

    id           = Column(Integer, primary_key=True, index=True)
    usuario_id   = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    jogo_id      = Column(Integer, ForeignKey("jogos.id"),    nullable=False)
    posicao      = Column(String(30), nullable=True)
    inscrito_em  = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="inscricoes")
    jogo    = relationship("Jogo",    back_populates="inscricoes")
