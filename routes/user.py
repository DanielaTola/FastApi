from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from config.db import SessionLocal
from models.user import users
from schemas.user import User
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user.get("/users", tags=["Users"])
def get_users(db: Session = Depends(get_db)):
    result = db.execute(users.select()).fetchall()
    users_list = [dict(row._mapping) for row in result] 
    return users_list

@user.post("/users", response_model=User, tags=["Users"])
def create_user(user: User, db: Session = Depends(get_db)):
    new_user = {"name": user.name, "email": user.email}
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    try:
        # Ejecutar la inserción y confirmar la transacción
        result = db.execute(users.insert().values(new_user))
        db.commit()
        # Obtener el ID del nuevo usuario
        new_user_id = result.lastrowid
        # Consultar y retornar el nuevo usuario
        created_user = db.execute(users.select().where(users.c.id == new_user_id)).first()
        return dict(created_user._mapping)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

@user.get("/users/{id}",response_model=User, tags=["Users"])
def get_user(id: int,db: Session = Depends(get_db)):
    if id <= 0:
        raise HTTPException(status_code=400, detail="Id debe ser un valor positivo")
    result = db.execute(users.select().where(users.c.id == id)).first()
    
    if result is None:
        raise HTTPException(status_code=404, detail="Usuario no existe")

    return dict(result._mapping)

@user.delete("/users/{id}", tags=["Users"])
def delete_user(id: int,db: Session = Depends(get_db)):
    if id <= 0:
        raise HTTPException(status_code=400, detail="Id debe ser un valor positivo")
    result = db.execute(users.select().where(users.c.id == id)).first()
    
    if result is None:
        raise HTTPException(status_code=404, detail="Usuario no existe")

    
    db.execute(users.delete().where(users.c.id==id))
    db.commit()
    return {"message": "Usuario eliminado correctamente"}

@user.put("/users/{id}",response_model=User, tags=["Users"])
def update_user(id: int, user:User, db: Session = Depends(get_db)):
    if id <= 0:
        raise HTTPException(status_code=400, detail="Id debe ser un valor positivo")
    db.execute(users.update().values(name=user.name, email=user.email,password=f.encrypt(user.password.encode("utf-8"))).where(users.c.id==id))
    db.commit()
    updated_user =db.execute(users.select().where(users.c.id==id)).first()

    if updated_user is None:
        raise HTTPException(status_code=404, detail="Usuario no existe")

    return dict(updated_user._mapping)