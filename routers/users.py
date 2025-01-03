from fastapi import APIRouter, Depends, HTTPException,Path
from typing import Annotated
from sqlalchemy.orm import Session
from ..models import Users
from ..database import SessionLocal
from starlette import status
from pydantic import BaseModel,Field
from .auth import get_current_user
from passlib.context import CryptContext

router =APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

class UserVerification(BaseModel):
    current_password:str
    new_password:str=Field(min_length=5)

@router.get('/',status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Authentication Failed')

    user_model=db.query(Users).filter(Users.id==user.get('id')).first()

    return user_model
 
@router.put('/password',status_code=status.HTTP_204_NO_CONTENT)
async def change_password(db:db_dependency,user:user_dependency,
                          user_verification:UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Authentication Failed')

    user_model=db.query(Users).filter(Users.id==user.get('id')).first()    
    if not bcrypt_context.verify(user_verification.current_password,user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Error in password change!')
    
    user_model.hashed_password=bcrypt_context.hash( user_verification.new_password)
    db.add(user_model)
    db.commit()

@router.put('/phonenumber/{phone_number}',status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(db:db_dependency,user:user_dependency,
                          phone_number:str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Authentication Failed')

    user_model=db.query(Users).filter(Users.id==user.get('id')).first()    

    user_model.phone_number=phone_number
    db.add(user_model)
    db.commit()
    
