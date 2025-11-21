from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_senha(senha: str):
    return pwd_context.hash(senha)

def verifica_senha(plain_senha, hashed_senha):
    return pwd_context.verify(plain_senha, hashed_senha)
