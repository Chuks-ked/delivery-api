from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from database import Session, engine
from schemas import SignupModel, LoginModel
from models import User
from werkzeug.security import generate_password_hash, check_password_hash


auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

session=Session(bind=engine)

@auth_router.get('/')
async def hello():
    return {"message":"Hello auth"}



@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user:SignupModel):
    db_email=session.query(User).filter(User.email==user.email).first()
    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with the email already exists")

    db_username=session.query(User).filter(User.username==user.username).first()

    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with the username already exists")
    
    new_user = User(
        username = user.username,
        email = user.email,
        password = generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )

    session.add(new_user)
    session.commit()

    return new_user


# login route
@auth_router.post('/login')
async def login(user:LoginModel, Authorize:AuthJWT=Depends()):
    db_user=session.query(User).filter(User.username==user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token=Authorize.create_access_token(subject=db_user.username)
        refresh_token=Auth