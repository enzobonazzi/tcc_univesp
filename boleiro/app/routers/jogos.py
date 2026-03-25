# app/routers/jogos.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.models import Jogo, Inscricao, Usuario
from app.schemas import JogoCriar, JogoResposta
from app.auth import get_usuario_atual

router = APIRouter(prefix="/jogos", tags=["Jogos"])


def _serializar(jogo: Jogo, db: Session) -> dict:
    """Converte o model Jogo para o formato que o frontend espera."""
    total_inscritos = db.query(Inscricao).filter(Inscricao.jogo_id == jogo.id).count()
    return {
        "id": jogo.id,
        "nome": jogo.nome,
        "cidade": jogo.cidade,
        "local": jogo.local,
        "data": jogo.data,
        "hora": jogo.hora,
        "nivel": jogo.nivel,
        "tipo": jogo.tipo,
        "vagas": jogo.vagas,
        "total_vagas": jogo.total_vagas,
        "posicoes": jogo.posicoes.split(",") if jogo.posicoes else [],
        "descricao": jogo.descricao,
        "urgente": jogo.urgente,
        "ativo": jogo.ativo,
        "criado_em": jogo.criado_em,
        "anunciante_id": jogo.anunciante_id,
        "anunciante_nome": jogo.anunciante.nome if jogo.anunciante else None,
        "anunciante_telefone": jogo.anunciante.telefone if jogo.anunciante else None,
        "total_inscritos": total_inscritos,
    }


@router.get("/", response_model=List[JogoResposta])
def listar_jogos(
    cidade:  Optional[str] = Query(None, description="Filtrar por cidade"),
    data:    Optional[str] = Query(None, description="Filtrar por data (YYYY-MM-DD)"),
    nivel:   Optional[str] = Query(None, description="Básico | Intermediário | Avançado"),
    tipo:    Optional[str] = Query(None, description="Society | Futsal | Campo | Pelada aberta"),
    posicao: Optional[str] = Query(None, description="Posição desejada"),
    horario: Optional[str] = Query(None, description="manha | tarde | noite"),
    db: Session = Depends(get_db)
):
    """Lista partidas com filtros opcionais — mesmo comportamento do frontend."""
    query = db.query(Jogo).filter(Jogo.ativo == True)

    if cidade:
        query = query.filter(Jogo.cidade == cidade)
    if data:
        query = query.filter(Jogo.data == data)
    if nivel:
        query = query.filter(Jogo.nivel == nivel)
    if tipo:
        query = query.filter(Jogo.tipo == tipo)
    if posicao:
        query = query.filter(
            Jogo.posicoes.contains(posicao) | Jogo.posicoes.contains("Qualquer")
        )
    if horario:
        jogos_todos = query.all()
        filtrados = []
        for j in jogos_todos:
            h = int(j.hora.split(":")[0])
            if horario == "manha" and h < 12:
                filtrados.append(j)
            elif horario == "tarde" and 12 <= h < 18:
                filtrados.append(j)
            elif horario == "noite" and h >= 18:
                filtrados.append(j)
        return [_serializar(j, db) for j in filtrados]

    jogos = query.order_by(Jogo.data.asc(), Jogo.hora.asc()).all()
    return [_serializar(j, db) for j in jogos]


@router.get("/{jogo_id}", response_model=JogoResposta)
def detalhe_jogo(jogo_id: int, db: Session = Depends(get_db)):
    """Retorna os detalhes de uma partida específica."""
    jogo = db.query(Jogo).filter(Jogo.id == jogo_id, Jogo.ativo == True).first()
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return _serializar(jogo, db)


@router.post("/", response_model=JogoResposta, status_code=201)
def criar_jogo(
    dados: JogoCriar,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual)
):
    """Anuncia um novo racha. Requer login."""
    # Marca urgente automaticamente se restar ≤ 2 vagas
    urgente = dados.vagas <= 2

    jogo = Jogo(
        nome=dados.nome,
        cidade=dados.cidade,
        local=dados.local,
        data=dados.data,
        hora=dados.hora,
        nivel=dados.nivel,
        tipo=dados.tipo,
        vagas=dados.vagas,
        total_vagas=dados.total_vagas,
        posicoes=",".join(dados.posicoes),
        descricao=dados.descricao,
        urgente=urgente,
        anunciante_id=usuario.id,
    )
    db.add(jogo)
    db.commit()
    db.refresh(jogo)
    return _serializar(jogo, db)


@router.put("/{jogo_id}", response_model=JogoResposta)
def editar_jogo(
    jogo_id: int,
    dados: JogoCriar,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual)
):
    """Edita um racha. Só o dono pode editar."""
    jogo = db.query(Jogo).filter(Jogo.id == jogo_id).first()
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    if jogo.anunciante_id != usuario.id:
        raise HTTPException(status_code=403, detail="Você não é o dono deste racha")

    jogo.nome        = dados.nome
    jogo.cidade      = dados.cidade
    jogo.local       = dados.local
    jogo.data        = dados.data
    jogo.hora        = dados.hora
    jogo.nivel       = dados.nivel
    jogo.tipo        = dados.tipo
    jogo.vagas       = dados.vagas
    jogo.total_vagas = dados.total_vagas
    jogo.posicoes    = ",".join(dados.posicoes)
    jogo.descricao   = dados.descricao
    jogo.urgente     = dados.vagas <= 2

    db.commit()
    db.refresh(jogo)
    return _serializar(jogo, db)


@router.delete("/{jogo_id}", status_code=204)
def deletar_jogo(
    jogo_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual)
):
    """Remove (desativa) um racha. Só o dono pode remover."""
    jogo = db.query(Jogo).filter(Jogo.id == jogo_id).first()
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    if jogo.anunciante_id != usuario.id:
        raise HTTPException(status_code=403, detail="Você não é o dono deste racha")

    jogo.ativo = False  # soft delete: não apaga do banco
    db.commit()


@router.get("/meus/anunciados", response_model=List[JogoResposta])
def meus_jogos_anunciados(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual)
):
    """Retorna os rachões anunciados pelo usuário logado."""
    jogos = db.query(Jogo).filter(
        Jogo.anunciante_id == usuario.id,
        Jogo.ativo == True
    ).all()
    return [_serializar(j, db) for j in jogos]
