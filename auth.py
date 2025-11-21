from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

import models
from database import SessionLocal
from utils import verifica_senha

SECRET_KEY = "CHAVE-SECRETA-MUITO-GRANDE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def autenticar_usuario(login: str, senha: str, db: Session):
    usuario = db.query(models.Usuario).filter(models.Usuario.login == login).first()
    if not usuario:
        return False
    if not verifica_senha(senha, usuario.senha):
        return False
    return usuario

def cria_token(data: dict, expires_delta=None):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) 

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def busca_usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.encode(token, SECRET_KEY, algorithm=[ALGORITHM])
        login: str = payload.get("sub")

        if login is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        usuario = db.query(models.Usuario).filter(models.Usuario.login == login).first()
        if usuario is None:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        
        return usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")