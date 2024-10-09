# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import db.models as models
from jose import JWTError, jwt
import schemas
from db import database
from passlib.context import CryptContext
import db.crud as crud
from typing import Optional, List
import tokens.create_token as create_token
from fastapi import Request
from tokens.token_vars import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY


database.Base.metadata.create_all(bind=database.engine)
pwd_context = CryptContext(schemes=["bcrypt"],
                           deprecated="auto")

app = FastAPI()

def get_token_from_header(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token is missing or invalid")
    token = auth_header[len("Bearer "):]  # Remove 'Bearer ' prefix
    return token


def verify_password(plain_password, hashed_password):
    print("verified")
    return pwd_context.verify(plain_password, hashed_password)


def get_current_user(db: Session = Depends(database.get_db), token: str = Depends(get_token_from_header)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/register", response_model=schemas.UserRegistrationResponse)
def register_user(user: schemas.UserBase, db: Session = Depends(database.get_db)):
    is_user_registered = crud.get_user_by_username_or_email(db, name=user.name, email=user.email)
    if is_user_registered is not None:
        raise HTTPException(status_code=400, detail="User is already registered, go to Log In page")
    print(user.password)
    hashed_password = pwd_context.hash(user.password)

    new_user_data = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        is_activated=True
    )

    crud.create_user(db, new_user_data)

    return schemas.UserRegistrationResponse.model_validate(new_user_data)


@app.post("/login", response_model=schemas.Token)
def login_for_access_token(credentials: schemas.UserLogin,
                           db: Session = Depends(database.get_db)):
    user = crud.get_user_by_username(db, username=credentials.username)
    
    if not user or not verify_password(credentials.password,
                                       user.password):
        raise HTTPException(status_code=401, 
                            detail="Access denied: Invalid or missing authentication credentials.")

    token = create_token.create_access_token({"sub": user.name})
    print(user.id)

    return schemas.Token.model_validate({"access_token": token})



@app.get("/items/", response_model=List[schemas.Item])
def get_items(title: Optional[str] = None,
              db: Session = Depends(database.get_db),
              current_user: models.User = Depends(get_current_user)):
    return current_user.todos


@app.post("/create_item", response_model=schemas.CreateItem)
def create_item(
    item: schemas.CreateItem,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_item = models.TodoList(
        title=item.title,
        description=item.description,
        owner_id=current_user.id,
        due_date=item.due_date,
        status=item.status
    )

    crud.create_item(new_item)
    return new_item


@app.put("/items/{item_id}", response_model=schemas.UpdateItem)
def update_item(item_id: int, item: schemas.UpdateItem, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    updated_item = crud.update_user_item(db=db, item_id=item_id, item=item, user_id=current_user.id)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item


@app.delete("/items/{item_id}", response_model=List[schemas.Item])
def delete_item(item_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    crud.delete_item_by_id(db, item_id)
    return current_user.todos


# def change_password():
#     pass

# def get_todo_list_by_partual_entry():
#     pass


# def update_multiple_todos():
#     pass


# def delete_one_todo():
#     pass


# def delete_multiple_todo():
#     pass  need just to clean up it a bit. no changes are needed