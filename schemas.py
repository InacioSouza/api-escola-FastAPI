from typing import List, Optional
from pydantic import BaseModel
from datetime import date

# ----------------------------- Schemas Perfil -----------------------------
class Perfil(BaseModel):
    id: int
    idade: int
    endereco: str

    class Config:
        from_attributes = True

class PerfilCreate(BaseModel):
    idade: int
    endereco: str

class PerfilUpdate(BaseModel):
    id: Optional[int] = None
    idade: Optional[int] = None
    endereco: Optional[str] = None

# ----------------------------- Schemas Estudante -----------------------------

class Estudante(BaseModel):
    id: int
    nome: str
    perfil: Perfil

    class Config:
        from_attributes=True

class EstudanteCreate(BaseModel): 
    nome: str
    email: str
    perfil: PerfilCreate

class EstudanteUpdate(BaseModel):
    id: Optional[int] = None
    nome: Optional[str] = None
    email: Optional[str] = None
    perfil: Optional[PerfilUpdate] = None

# ----------------------------- Schemas Professor -----------------------------

class Professor(BaseModel):
    id: int
    nome: str

    class config:
        from_attributes=True

class ProfessorCreate(BaseModel):
    nome: str

class ProfessorUpdate(ProfessorCreate):
    id: Optional[int] = None

# ----------------------------- Schemas Disciplina -----------------------------
class Disciplina(BaseModel):
    id: int
    nome: str
    descricao: str
    professor: Optional[Professor] = None

    class config:
        from_attributes=True

class DisciplinaCreate(BaseModel):
    nome: str
    descricao: str
    id_professor: Optional[int] = None 

class DisciplinaUpdate(BaseModel):
    id: Optional[int] = None
    nome: Optional[str] = None
    descricao: Optional[str] = None
    professor: Optional[ProfessorUpdate] = None

# ----------------------------- Schemas Matricula -----------------------------

class Matricula(BaseModel):
    id: int
    disciplina: Disciplina
    estudante: Estudante
    data_matricula: date

class MatriculaCreate(BaseModel):
    id_disciplina: int
    id_estudante: int
    data_matricula: date

class MatriculaUpdate(BaseModel):
    id: Optional[int] = None
    disciplina: Optional[DisciplinaUpdate] = None
    estudante: Optional[EstudanteUpdate] = None
    data_matricula: Optional[date] = None