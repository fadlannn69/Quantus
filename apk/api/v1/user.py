from fastapi import APIRouter, Depends, HTTPException , Form
from fastapi.security import OAuth2PasswordRequestForm
from apk.crud.user import CrudUser 
from sqlmodel import Session
from apk.database.session import get_session
from apk.model.model_user import User , UserCreate 
from apk.core.wrapper import ProtectEndpoint

protect = ProtectEndpoint()
fx = CrudUser()
UserEndpoint = APIRouter()

# Register Endpoint
@UserEndpoint.post("/Register")
def UserRegister(
    user: UserCreate,
    session: Session = Depends(get_session)):
    if user.roles == "admin" and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Hanya admin yang bisa membuat admin")
    return fx.UserRegister(user , session)

# Login Endpoint
@UserEndpoint.post("/Login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    return fx.UserLogin(form_data,session)

# Get User By Id Endpoint
@UserEndpoint.get("/GetOneUser/{user_id}")
def GetUserById(
    user_id : str ,
    session : Session = Depends(get_session) ,
    current_user=Depends(protect.admin_required)
    ):
    
    return fx.GetUser(user_id , session)

# Update User Endpoint
@UserEndpoint.put("/UpdateUser/{user_id}")
def UpdateUser(
    user_id  : str,
    nama : str = Form(...) ,
    password : str = Form(...) ,
    session : Session = Depends(get_session),
    current_user=Depends(protect.allAccess)
    ):
    
    return fx.UpdateUser(user_id ,nama , password , session)

# Delete User Endpoint
@UserEndpoint.delete("/DeleteUser/{user_id}")
def DeleteUSer(
    user_id ,
    session : Session = Depends(get_session),
    current_user=Depends(protect.allAccess)
    ):
    return fx.DeleteUser(user_id,session)