# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Usuario
from app.schemas import UsuarioCriar, UsuarioResposta, LoginResposta
from app.auth import hash_senha, verificar_senha, criar_token

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/cadastro", response_model=LoginResposta, status_code=201)
def cadastrar(dados: UsuarioCriar, db: Session = Depends(get_db)):
    """Cria uma nova conta de usuário."""
    # Verifica se o email já existe
    if db.query(Usuario).filter(Usuario.email == dados.email).first():
        raise HTTPException(
            status_code=400,
            detail="Este e-mail já está cadastrado"
        )

    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=hash_senha(dados.senha),
        telefone=dados.telefone,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    token = criar_token({"sub": str(usuario.id)})
    return {"access_token": token, "token_type": "bearer", "usuario": usuario}


@router.post("/login", response_model=LoginResposta)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Faz login com e-mail e senha. Retorna um token JWT."""
    usuario = db.query(Usuario).filter(Usuario.email == form.username).first()

    if not usuario or not verificar_senha(form.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
        )

    token = criar_token({"sub": str(usuario.id)})
    return {"access_token": token, "token_type": "bearer", "usuario": usuario}


@router.get("/me", response_model=UsuarioResposta)
def meu_perfil(db: Session = Depends(get_db), usuario=Depends(__import__("app.auth", fromlist=["get_usuario_atual"]).get_usuario_atual)):
    """Retorna os dados do usuário logado."""
    return usuario
