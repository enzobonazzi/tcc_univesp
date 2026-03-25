# app/routers/inscricoes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import Jogo, Inscricao, Usuario
from app.schemas import InscricaoCriar, InscricaoResposta
from app.auth import get_usuario_atual

router = APIRouter(prefix="/jogos", tags=["Inscrições"])


@router.post("/{jogo_id}/entrar", response_model=InscricaoResposta, status_code=201)
def entrar_no_jogo(
    jogo_id: int,
    dados: InscricaoCriar,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual)
):
    """Inscreve o usuário logado em um racha."""
    jogo = db.query(Jogo).filter(Jogo.id == jogo_id, Jogo.ativo == True).first()
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")

    if jogo.vagas <= 0:
        raise HTTPException(status_code=400, detail="Não há vagas disponíveis")

    # Verifica se já está inscrito
    ja_inscrito = db.query(Inscricao).filter(
        Inscricao.usuario_id == usuario.id,
        Inscricao.jogo_id == jogo_id
    ).first()
    if ja_inscrito:
        raise HTTPException(status_code=400, detail="Você já está inscrito neste racha")

    # Cria inscrição e desconta vaga
    inscricao = Inscricao(
        usuario_id=usuario.id,
        jogo_id=jogo_id,
        posicao=dados.posicao,
    )
    jogo.vagas -= 1
    if jogo.vagas <= 2:
        jogo.urgente = True

    db.add(inscricao)
    db.commit()
    db.refresh(inscricao)
    return inscricao


@router.delete("/{jogo_id}/sair", status_code=204)
def sair_do_jogo(
    jogo_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual)
):
    """Remove a inscrição do usuário logado de um racha."""
    inscricao = db.query(Inscricao).filter(
        Inscricao.usuario_id == usuario.id,
        Inscricao.jogo_id == jogo_id
    ).first()
    if not inscricao:
        raise HTTPException(status_code=404, detail="Você não está inscrito neste racha")

    # Devolve a vaga
    jogo = db.query(Jogo).filter(Jogo.id == jogo_id).first()
    if jogo:
        jogo.vagas += 1
        if jogo.vagas > 2:
            jogo.urgente = False

    db.delete(inscricao)
    db.commit()


@router.get("/{jogo_id}/inscritos", response_model=List[InscricaoResposta])
def listar_inscritos(
    jogo_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual)
):
    """Lista os inscritos de um racha. Só o dono do racha pode ver."""
    jogo = db.query(Jogo).filter(Jogo.id == jogo_id).first()
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    if jogo.anunciante_id != usuario.id:
        raise HTTPException(status_code=403, detail="Só o dono do racha pode ver os inscritos")

    return db.query(Inscricao).filter(Inscricao.jogo_id == jogo_id).all()


@router.get("/meus/inscritos", response_model=List[InscricaoResposta])
def meus_jogos_inscritos(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual)
):
    """Retorna os rachões em que o usuário logado está inscrito."""
    return db.query(Inscricao).filter(Inscricao.usuario_id == usuario.id).all()
