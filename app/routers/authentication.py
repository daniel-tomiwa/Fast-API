from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import schemas, database, models, utils, oath2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    #username = ?
    #password = ?
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    
    #Check if the claimed user is in the database
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    #Check of the password of the user matches the password in the database
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    #create and return a token once the user has been validated
    access_token = oath2.create_access_token(data={"user_id": user.id})

    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }