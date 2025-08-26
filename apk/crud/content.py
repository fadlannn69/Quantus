from fastapi import HTTPException , Form , Depends , File , UploadFile 
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session , select
from apk.model.model_user import User
from apk.core.auth import AuthHandler
from apk.database.session import get_session
from apk.model.model_content import Journal , Status , Category
from typing import List
from uuid import uuid4
from PIL import Image
from datetime import datetime
import shutil
import re
import os


auth_handler = AuthHandler()



class CrudJourney:
    
    # COVER_IMAGE FUNCTION
    @staticmethod
    def save_cover_image(cover_image: UploadFile | None) -> str | None:
        if cover_image is None:
            return None

        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)

        ext = cover_image.filename.split(".")[-1].lower()
        filename = f"{uuid4()}.{ext}"
        file_path = os.path.join(upload_dir, filename)

        with open(file_path, "wb") as f:
            f.write(cover_image.file.read())
        return filename
    
    
    # ADD CONTENT FUNCTION
    @staticmethod
    def TambahJournal(
        title: str ,
        category: Category,
        status: Status,
        content: str,
        cover_image : str | None,
        session : Session
    ):
        
        journal_data = Journal(
            title=title,
            category=category,
            status=status,
            cover_image=CrudJourney.save_cover_image(cover_image),
            content=content,
        )
        
        session.add(journal_data)
        session.commit()
        session.refresh(journal_data)
        return journal_data
        
    
    # GET ALL CONTENT FUNCTION
    @staticmethod
    def AmbilSemuaContent(
    limit: int ,
    offset: int ,
    session: Session = Depends(get_session)):
        
        Query = select(Journal).offset(offset).limit(limit)
        result = session.exec(Query).all()
        return result
    
    # GET CONTENT BY ID
    @staticmethod
    def AmbilSatuContent(
        content_id: str,
        session: Session
    ):
        statement = select(Journal).where(Journal.id == content_id)
        content_get = session.exec(statement).first()

        if not content_get:
            raise HTTPException(status_code=404, detail="Content not found")

        # tambah view_count
        content_get.view_count = (content_get.view_count or 0) + 1
        session.add(content_get)
        session.commit()
        session.refresh(content_get)

        return content_get

    
    # UPDATE CONTENT BY ID
    @staticmethod
    def UpdateContent(
        content_id,
        title: str ,
        category: Category,
        status: Status ,
        content: str,
        cover_image :  str | None,
        session : Session
    ):
        
        journal_data = session.exec(select(Journal).where(Journal.id == content_id)).first()
        if not journal_data:
            raise HTTPException(status_code=404, detail="Journal tidak ditemukan")
        
        
        journal_data.title = title
        journal_data.category = category
        journal_data.status = status
        journal_data.content = content
        journal_data.updated_at = datetime.utcnow()
        if cover_image:
            journal_data.cover_image= CrudJourney.save_cover_image(cover_image)
        
        session.add(journal_data)
        session.commit()
        session.refresh(journal_data)
        return journal_data
    
    # DELETE CONTENT BY ID
    @staticmethod
    def DeleteContent(content_id , session : Session):
        existing_content = session.exec(select(Journal).where(Journal.id == content_id)).first()
        if not existing_content:
            raise HTTPException(status_code=404, detail="Content tak ditemukan")
        session.delete(existing_content)
        session.commit()
        return {"detail": f"{existing_content.title} berhasil dihapus"}
