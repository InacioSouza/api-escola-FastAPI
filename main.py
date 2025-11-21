from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from typing import List

import models, schemas
from database import engine, SessionLocal
from utils import hash_senha
from auth import autenticar_usuario, cria_token, busca_usuario_atual



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------------- Rotas Estudante -----------------------------
@app.post('/estudantes/', response_model=schemas.Estudante)
def criar_estudante(
    estudante_create: schemas.EstudanteCreate,
    db: Session = Depends(get_db)
):
    db_estudante = models.Estudante(
        nome = estudante_create.nome,
        perfil = models.Perfil(**estudante_create.perfil.model_dump()),
        ativo=True
    )
    db.add(db_estudante)
    db.commit()
    db.refresh(db_estudante)
    return db_estudante

@app.get('/estudantes/', response_model=List[schemas.Estudante])
def listar_estudantes(db: Session = Depends(get_db)):
    estudantes = db.query(models.Estudante).options(
        joinedload(models.Estudante.perfil)
    ).all()
    return estudantes

@app.get("/estudantes/{id}", response_model=schemas.Estudante)
def busca_por_id_estudante(id: int, db: Session = Depends(get_db)):
    estudante = db.query(models.Estudante).filter(models.Estudante.id == id).first()
    if not estudante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return schemas.Estudante.model_validate(estudante)

@app.put("/estudantes/{id}", response_model=schemas.Estudante)
def altera_estudante(id: int, estudante_put: schemas.EstudanteUpdate, db: Session = Depends(get_db)):
    
    estudante = db.query(models.Estudante).filter(models.Estudante.id == id).first()
    
    if not estudante:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estudante não encontrado"
            )
    
    for key, value in estudante_put.model_dump().items():
        if value:
            setattr(estudante, key, value)

    db.commit()
    db.refresh(estudante)
    return estudante

# ----------------------------- Rotas Professor -----------------------------
@app.post("/professores/", response_model=schemas.Professor)
def criar_professor(
    professor: schemas.ProfessorCreate,
    db: Session = Depends(get_db)
):
    db_professor = models.Professor(nome=professor.nome, ativo=True)
    db.add(db_professor)
    db.commit()
    db.refresh(db_professor)
    return db_professor

@app.get("/professores/", response_model=List[schemas.Professor])
def listar_professores(db: Session = Depends(get_db)):

    listProfessores = db.query(models.Professor).options(
        joinedload(models.Professor.disciplinas)
    ).all()

    return listProfessores

@app.get("/professores/{id}", response_model=schemas.Professor)
def busca_por_id_professor(id: int, db: Session = Depends(get_db)):

    professor = db.query(models.Professor).filter(models.Professor.id == id).first()

    if not professor:
        raise HTTPException(
            status=status.HTTP_404_NOT_FOUND,
            detail=f"Professor com id = {id} não encontrado!"
        )
    return professor

@app.put("/professores/{id}", response_model=schemas.Professor)
def altera_professor(id: int, professor: schemas.ProfessorUpdate, db: Session = Depends(get_db)):

    professor_db = db.query(schemas.Professor).filter(schemas.Professor.id == id).first()

    if not professor_db:
        raise HTTPException(
            status=status.HTTP_404_NOT_FOUND,
            detail=f"Professor com id = {id} não encontrado!"
        )
    
    for key, value in professor.model_dump().items():
        if value:
            setattr(professor_db, key, value)

    db.commit()
    db.refresh(professor_db)
    return professor_db

# ----------------------------- Rotas Disciplina -----------------------------
@app.post("/disciplinas/", response_model=schemas.Disciplina)
def criar_disciplina(disciplina: schemas.DisciplinaCreate, db: Session = Depends(get_db)):
    disciplina_db = models.Disciplina(
        nome=disciplina.nome, 
        descricao=disciplina.descricao,
        ativa=True   
    )

    if disciplina.id_professor:
        professor_db = db.query(models.Professor).filter(models.Professor.id == disciplina.id_professor).first()
        if not professor_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Professor de id {disciplina.id_professor} não econtrado"
            )
        disciplina_db.professor = professor_db

    db.add(disciplina_db)
    db.commit()
    db.refresh(disciplina_db)
    return disciplina_db

@app.get("/disciplinas/", response_model=List[schemas.Disciplina])
def listar_disciplinas(db: Session = Depends(get_db)):
    list_disciplina = db.query(models.Disciplina).options(
        joinedload(models.Disciplina.professor)
    ).all()
    print('\n\n CHEGUEI ATÉ AQUI \n\n')
    return list_disciplina 

@app.get("/disciplinas/{id}", response_model=schemas.Disciplina)
def busca_por_id_disciplina(id: int, db: Session = Depends(get_db)):
    disciplina_db = db.query(models.Disciplina).filter(models.Disciplina.id == id).first()
    if not disciplina_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disciplina não encontrada"
        )
    return disciplina_db

@app.put("/disciplinas/{id}", response_model=schemas.DisciplinaUpdate)
def altera_disciplina(id: int, disciplina: schemas.DisciplinaUpdate, db: Session = Depends(get_db)):
    disciplina_db = db.query(models.Disciplina).filter(models.Disciplina.id == id).first()

    if not disciplina_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disciplina não encontrada"
        )
    for key, value in disciplina.model_dump().items():
        if value:
            setattr(disciplina_db, key, value)
    db.commit()
    db.refresh(disciplina_db)
    return disciplina_db

# ----------------------------- Rotas Matricula -----------------------------
@app.get("/matriculas/", response_model=List[schemas.Matricula])
def listar_matricula(db: Session = Depends(get_db)):
    list_matricula = db.query(models.Matricula).options(
        joinedload(models.Matricula.estudante)
    ).all()
    return list_matricula

@app.get("/matriculas/{id}", response_model=schemas.Matricula)
def busca_por_id_matricula(id: int, db: Session = Depends(get_db)):
    matricula_db = db.query(models.Matricula).filter(models.Matricula.id == id).first()
    if not matricula_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matricula não encontrada!"
        )
    return matricula_db

@app.post("/matriculas/", response_model=schemas.Matricula)
def criar_matricula(matricula: schemas.MatriculaCreate, db: Session = Depends(get_db)):
    matricula_db = models.Matricula(
        data_matricula=matricula.data_matricula,
        ativa=True
    )

    disciplina_db = db.query(models.Disciplina).filter(models.Disciplina.id == matricula.id_disciplina).first()

    if not disciplina_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Disciplina de id {matricula.id_disciplina} não encontrada"
        )
    matricula_db.disciplina = disciplina_db
    
    estudante_db = db.query(models.Estudante).filter(models.Estudante.id == matricula.id_estudante).first()

    if not estudante_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Estudante de id {matricula.id_estudante} não encontrado"
        )
    matricula_db.estudante = estudante_db
    
    db.add(matricula_db)
    db.commit()
    db.refresh(matricula_db)
    return matricula_db

# ----------------------------- Rota Login -----------------------------

@app.post("/usuarios/", response_model=schemas.Usuario)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    hashed = hash_senha(usuario.senha)
    db_usuario = models.Usuario(login=usuario.login, senha=hashed)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = autenticar_usuario(form_data.login, form_data.password, db)
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")
    token = cria_token({"sub": usuario.login})

    return {"access_token": token, "token_type": "bearer"}

@app.get("/me")
def me(usuario_atual = Depends(busca_usuario_atual)):
    return {"id": usuario_atual.id, "login": usuario_atual.login}
