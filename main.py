from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal
from typing import List
from sqlalchemy.orm import joinedload

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/estudantes/', response_model=schemas.Estudante)
def criar_estudante(
    estudante: schemas.EstudanteCreate,
    db: Session = Depends(get_db)
):
    db_estudante = models.Estudante(
        nome = estudante.nome,
        perfil = models.Perfil(**estudante.perfil.model_dump())
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
def get_by_id_estudante(id: int, db: Session = Depends(get_db)):
    estudante = db.query(models.Estudante).filter(models.Estudante.id == id).first()
    if not estudante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return schemas.Estudante.model_validate(estudante)

@app.put("/estudantes/{id}", response_model=schemas.Estudante)
def altera_estudante(id: int, estudante_put: schemas.EstudanteCreate, db: Session = Depends(get_db)):
    
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

@app.post("/professores/", response_model=schemas.Professor)
def criar_professor(
    professor: schemas.ProfessorCreate,
    db: Session = Depends(get_db)
):
    db_professor = models.Professor(nome=professor.nome)
    db.add(db_professor)
    db.commit()
    db.refresh(db_professor)
    return db_professor

@app.get("/professores/", response_model=List[schemas.Professor])
def get_all_professor(db: Session = Depends(get_db)):

    listProfessores = db.query(models.Professor).options(
        joinedload(models.Professor.disciplinas)
    ).all()

    return listProfessores

@app.get("/professores/{id}", response_model=schemas.Professor)
def get_by_id_professor(id: int, db: Session = Depends(get_db)):

    professor = db.query(models.Professor).filter(models.Professor.id == id).first()

    if not professor:
        raise HTTPException(
            status=status.HTTP_404_NOT_FOUND,
            detail=f"Professor com id = {id} não encontrado!"
        )
    return professor

@app.put("/professores/{id}", response_model=schemas.Professor)
def altera_professor(id: int, professor: schemas.ProfessorCreate, db: Session = Depends(get_db)):

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

@app.post("/disciplinas/", response_model=schemas.Disciplina)
def create_disciplina(disciplina: schemas.DisciplinaCreate, db: Session = Depends(get_db)):
    disciplina_db = models.Disciplina(**disciplina.model_dump())
    db.add(disciplina_db)
    db.commit()
    db.refresh(disciplina_db)
    return disciplina_db

@app.put("/disciplinas/{id}", response_model=schemas.Disciplina)
def altera_disciplina(id: int, disciplina: schemas.DisciplinaCreate):
    print()