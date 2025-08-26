from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from apk.database.session import get_session
from apk.model.model_user import User
from apk.core.auth import AuthHandler

auth_handler = AuthHandler()
security = HTTPBearer()


class ProtectEndpoint:
    def auth_wrapper(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        session: Session = Depends(get_session)
    ):
        token = credentials.credentials 
        try:
            user_id = auth_handler.decode_token(token)  
        except HTTPException as e:
            raise e
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user 


    # ADMIN ONLY ROLE
    @staticmethod
    def admin_required(current_user=Depends(auth_wrapper)):
        if current_user.roles != "admin":
            raise HTTPException(status_code=403, detail="Admin only")
        return current_user

    # ALL USER CAN ACCESS
    @staticmethod
    def allAccess(current_user=Depends(auth_wrapper)):
        if current_user.roles not in ["admin", "user"]:
            raise HTTPException(status_code=403, detail="Admin or User only")
        return current_user

