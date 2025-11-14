from typing import List, Optional
from pydantic import BaseModel

class Perfil(BaseModel):
    id: int
    idade: int
    endereco: str

    class Config:
        from_attributes = True

class PerfilCreate(BaseModel):
    idade: int
    endereco: str


class Estudante(BaseModel):
    id: int
    nome: str
    perfil: Optional[Perfil] = None

    class Config:
        from_attributes=True

class EstudanteCreate(BaseModel): 
    nome: Optional[str] = None
    email: Optional[str] = None
    perfil: Optional[PerfilCreate] = None

class Professor(BaseModel):
    id: Optional[int] = None
    nome: Optional[str] = None

    class config:
        from_attributes=True

class ProfessorCreate(BaseModel):
    nome: str

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
    professor: ProfessorCreate

class Matricula(BaseModel):
    id: int
    disciplina: Optional[Disciplina] = None
    estudante: Optional[Estudante] = None
    data_matricula: str

class MatriculaCreate(BaseModel):
    disciplina: DisciplinaCreate
    estudante: EstudanteCreate
    data_matricula: str