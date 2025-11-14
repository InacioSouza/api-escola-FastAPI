from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Estudante(Base):
    __tablename__ = 'estudantes'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String)
    perfil = relationship(
        "Perfil",
        back_populates="estudante",
        uselist=False,
        cascade="all, delete-orphan"
    )
    matriculas = relationship(
        "Matricula",
        back_populates="estudante"   
    )

class Perfil(Base):
    __tablename__ = 'perfis'
    id = Column(Integer, primary_key=True, index=True)
    idade = Column(Integer)
    endereco = Column(String)
    estudante_id = Column(
        Integer,
        ForeignKey("estudantes.id"),
        unique=True
    )
    estudante = relationship("Estudante", back_populates='perfil')

class Professor(Base):
    __tablename__ = "professores"
    id=Column(Integer, primary_key=True, index=True)
    nome=Column(String)
    disciplinas=relationship(
        "Disciplina",
        back_populates="professor",
        cascade="all, delete-orphan"
    )

class Disciplina(Base):
    __tablename__="disciplinas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    professor_id = Column(Integer, ForeignKey("professores.id"))
    professor = relationship(
        "Professor",
        back_populates="disciplinas",
        cascade="all"
    )

class Matricula(Base):
    __tablename__="matriculas"
    id=Column(Integer, primary_key=True, index=True)
    disciplina_id=Column(Integer, ForeignKey("disciplinas.id"))
    estudante_id=Column(Integer, ForeignKey("estudantes.id"))
    estudante = relationship(
        "Estudante",
        back_populates="matriculas"
    )
    data_matricula=Column(Date)