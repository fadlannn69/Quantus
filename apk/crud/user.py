from apk.model.model_user import User
from apk.core.auth import AuthHandler
from sqlmodel import Session , select
from apk.database.session import get_session
from apk.model.model_user import User , UserCreate
from fastapi import HTTPException , Form ,Depends
from fastapi.security import OAuth2PasswordRequestForm
import re


auth_handler = AuthHandler()

class CrudUser:

    # REGISTER USER
    @staticmethod
    def UserRegister(user: UserCreate, session: Session):
        # password minimal 8 karakter
        if len(user.password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

        # username tidak boleh mengandung angka
        if re.search(r"\d", user.nama):
            raise HTTPException(status_code=400, detail="Username must not contain numbers")

        # password harus mengandung huruf, angka, dan simbol
        if not re.search(r"[A-Za-z]", user.password):
            raise HTTPException(status_code=400, detail="Password must contain at least one letter")
        if not re.search(r"[0-9]", user.password):
            raise HTTPException(status_code=400, detail="Password must contain at least one digit")
        if not re.search(r"[^A-Za-z0-9]", user.password):
            raise HTTPException(status_code=400, detail="Password must contain at least one special character (!@#$%^&* etc.)")

        password = auth_handler.get_password_hash(user.password)
        
        db_user = User(nama=user.nama, password=password)
        
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return {"message": "User registered successfully"}
    
    # LOGIN USER
    @staticmethod
    def UserLogin(form_data: OAuth2PasswordRequestForm,session: Session):
        statement = select(User).where(User.nama == form_data.username)
        user = session.exec(statement).first()

        # validasi user + password
        if (not user) or (not auth_handler.verify_password(form_data.password, user.password)):
            raise HTTPException(status_code=401, detail="Incorrect username or password")

        # bikin JWT token
        token = auth_handler.encode_token(user.id)

        return {
            "access_token": token,
            "message": "User Login successfully"}
        
    #GET USER BY ID
    @staticmethod
    def GetUser(user_id , session : Session):
        statement = select(User).where(User.id == user_id)
        user_get = session.exec(statement).first()
        
        return user_get
    
    # UPDATE USER BY ID
    @staticmethod
    def UpdateUser(user_id ,nama : str, password : str,  session : Session):
        statement = select(User).where(User.id == user_id)
        user_put = session.exec(statement).first()
        if not user_put:
            raise HTTPException(status_code=404, detail="User tidak ditemukan")
        
        if len(password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

        # username tidak boleh mengandung angka
        if re.search(r"\d", nama):
            raise HTTPException(status_code=400, detail="Username must not contain numbers")

        # password harus mengandung huruf, angka, dan simbol
        if not re.search(r"[A-Za-z]", password):
            raise HTTPException(status_code=400, detail="Password must contain at least one letter")
        if not re.search(r"[0-9]", password):
            raise HTTPException(status_code=400, detail="Password must contain at least one digit")
        if not re.search(r"[^A-Za-z0-9]", password):
            raise HTTPException(status_code=400, detail="Password must contain at least one special character (!@#$%^&* etc.)")

        password = auth_handler.get_password_hash(password)
        
        user_put.nama = nama
        user_put.password = password
        
        session.add(user_put)
        session.commit()
        session.refresh(user_put)
        
        return user_put
    
    # DELETE USER BY ID
    @staticmethod
    def DeleteUser(user_id , session : Session):
        existing_user = session.exec(select(User).where(User.id == user_id)).first()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User tak ditemukan")
        session.delete(existing_user)
        session.commit()
        return {"detail": f"{existing_user.nama} berhasil dihapus"}
