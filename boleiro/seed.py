# seed.py — popula o banco com os dados de exemplo do site
# Execute com: python seed.py
from app.database import engine, SessionLocal
from app.models.models import Base, Usuario, Jogo
from app.auth import hash_senha
from datetime import datetime, timedelta

def seed():
    # Cria todas as tabelas
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Verifica se já tem dados
    if db.query(Usuario).count() > 0:
        print("Banco já populado. Pulando seed.")
        db.close()
        return

    # Cria usuário demo
    usuario = Usuario(
        nome="Admin BoleirApp",
        email="admin@boleiro.com",
        senha_hash=hash_senha("boleiro123"),
        telefone="(19) 9 9999-0000",
    )
    db.add(usuario)
    db.flush()  # gera o id sem commitar

    hoje = datetime.utcnow().date()

    jogos_seed = [
        dict(nome="Racha da Sé",         cidade="São Paulo - SP",      local="Campo Sintético do Anhangabaú",             data=str(hoje),                       hora="19:00", nivel="Intermediário", tipo="Society",       vagas=3,  total_vagas=14, posicoes="Meia,Ponta,Centroavante",            descricao="Racha semanal firme! Galera comprometida, jogo limpo.",                urgente=False),
        dict(nome="Pelada Beira Rio",     cidade="Piracicaba - SP",     local="Campo do Parque do Povo, Av. Beira Rio",    data=str(hoje),                       hora="07:30", nivel="Básico",        tipo="Pelada aberta", vagas=5,  total_vagas=22, posicoes="Goleiro,Zagueiro,Qualquer",           descricao="Pelada aberta todo sábado de manhã. Nível tranquilo.",                 urgente=True),
        dict(nome="Copa Jardim America",  cidade="Campinas - SP",       local="Arena Campos — Rua Barão de Itapura",       data=str(hoje + timedelta(days=1)),   hora="20:00", nivel="Avançado",      tipo="Society",       vagas=1,  total_vagas=14, posicoes="Goleiro",                             descricao="Falta 1 goleiro para a rodada de amanhã.",                            urgente=True),
        dict(nome="Racha da Vila",        cidade="São Paulo - SP",      local="Campo Sintético Vila Madalena",             data=str(hoje + timedelta(days=2)),   hora="18:00", nivel="Intermediário", tipo="Futsal",        vagas=4,  total_vagas=10, posicoes="Lateral,Volante,Meia",                descricao="Racha de futsal nível intermediário. Pessoal unido.",                  urgente=False),
        dict(nome="Guerreiros do Sul",    cidade="Porto Alegre - RS",   local="Campo do Menino Deus — Rua Cel. Genuíno",   data=str(hoje + timedelta(days=3)),   hora="09:00", nivel="Básico",        tipo="Campo",         vagas=8,  total_vagas=22, posicoes="Zagueiro,Lateral,Volante,Centroavante",descricao="Partida no campo de grama natural! Domingão clássico.",                urgente=False),
        dict(nome="Fut Noturno Lapa",     cidade="São Paulo - SP",      local="Arena FutNight Lapa — R. Catão",            data=str(hoje + timedelta(days=4)),   hora="22:00", nivel="Intermediário", tipo="Society",       vagas=0,  total_vagas=14, posicoes="",                                    descricao="Partida noturna tradicional. Vagas esgotadas.",                        urgente=False),
        dict(nome="Racha da Praça",       cidade="Ribeirão Preto - SP", local="Campo da Praça do Coração — Centro",        data=str(hoje + timedelta(days=5)),   hora="16:00", nivel="Básico",        tipo="Pelada aberta", vagas=6,  total_vagas=22, posicoes="Qualquer",                            descricao="Clássico da cidade! Já tem 10 anos de racha.",                         urgente=False),
        dict(nome="Elite FC Futsal",      cidade="Belo Horizonte - MG", local="CT Elite Sports — Savassi",                data=str(hoje + timedelta(days=6)),   hora="20:30", nivel="Avançado",      tipo="Futsal",        vagas=2,  total_vagas=10, posicoes="Ponta,Fixo",                          descricao="Futsal de alto nível, galera ex-federação.",                           urgente=True),
    ]

    for j in jogos_seed:
        db.add(Jogo(anunciante_id=usuario.id, **j))

    db.commit()
    db.close()
    print("✅ Banco populado com sucesso!")
    print("   Usuário demo: admin@boleiro.com / boleiro123")

if __name__ == "__main__":
    seed()
