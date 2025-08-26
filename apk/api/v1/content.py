from fastapi import APIRouter , Form , Depends , UploadFile , File , Query
from apk.crud.content import CrudJourney
from apk.database.session import get_session
from apk.model.model_content import Category , Status , Journal
from sqlmodel import Session
from typing import List
from apk.core.wrapper import ProtectEndpoint

protect = ProtectEndpoint()
fx = CrudJourney()
ContentEndpoint = APIRouter()


# TAMBAH CONTENT
@ContentEndpoint.post("/AddContent")
def TambahJournal(
        title: str = Form(...) ,
        category: Category = Category.OTHER,
        status: Status = Status.DRAFT,
        content: str = Form(...),
        cover_image : UploadFile = File(None),
        session : Session = Depends(get_session),
        current_user=Depends(protect.allAccess)
    ):
    return fx.TambahJournal(title,category,status,content,cover_image,session)

# AMBIL SEMUA CONTENT
@ContentEndpoint.get("/GetAllContent",response_model=List[Journal])
def AmbilSemuaContent( 
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
    current_user=Depends(protect.allAccess)
    ):
    return fx.AmbilSemuaContent(limit,offset,session)

# AMBIL 1 CONTENT
@ContentEndpoint.get("/GetOneContent/{content_id}")
def AmbilSatuContent(
    content_id : str ,
    session:Session = Depends(get_session),
    current_user=Depends(protect.allAccess)
    ):
    return fx.AmbilSatuContent(content_id,session)

# UPDATE CONTENT
@ContentEndpoint.put("/UpdateContent/{content_id}")
def UpdateContent(
    content_id : str,
    title: str = Form(...) ,
    category: Category = Category.OTHER,
    status: Status = Status.DRAFT,
    content: str = Form(...),
    cover_image :  UploadFile = File(None),
    session : Session = Depends(get_session),
    current_user=Depends(protect.allAccess)
):
    return fx.UpdateContent(content_id,title,category,status,content,cover_image,session)

# DELETE CONTENT
@ContentEndpoint.delete("/DeleteContent/{content_id}")
def DeteleContent(
    content_id : str ,
    session : Session = Depends(get_session),
    current_user=Depends(protect.allAccess)
    ):
    return fx.DeleteContent(content_id,session)