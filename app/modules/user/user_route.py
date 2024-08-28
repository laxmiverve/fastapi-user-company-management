from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile, Form
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi_pagination import Params
from app.modules.user import user_service
from config.database import get_db, msg
from app.schemas.response_schema import ResponseSchema
from app.auth.jwt_bearer import JWTBearer
from app.schemas.user_update_schema import UserUpdateSchema
from app.schemas.user_response_schema import UserResponseSchema

router = APIRouter(prefix="/user", tags=["User"])  


# New user register
@router.post('/register', summary="Register new users", response_model=ResponseSchema[UserResponseSchema])
async def register_user(background_tasks: BackgroundTasks, name: str = Form(...), email: str = Form(...), password: str = Form(...), role_id: int = Form(...), city: str = Form(None), state: str = Form(None), country: str = Form(None), profile_img: Optional[UploadFile] = File(None), db: Session = Depends(get_db)):

    new_user = await user_service.create_user(name=name, email=email, password=password, role_id=role_id, city=city, state=state, country=country, profile_img=profile_img, background_tasks=background_tasks, db=db)
    
    if new_user:
        return ResponseSchema(status=True, response=msg['user_register'], data=new_user)
    else:
        return ResponseSchema(status=False, response=msg['user_already_exists'], data=None)



# Get all user information
@router.get( "/list", summary = "List of users", response_model = ResponseSchema[List[UserResponseSchema]], dependencies =[Depends(JWTBearer())])
def list_users( params: Params = Depends(), db: Session = Depends(get_db), search_string: Optional[str] = None, sort_by: Optional[str] = None, sort_direction: Optional[str] = None):
    all_users = user_service.get_all_users(db = db, params = params, search_string = search_string, sort_by = sort_by, sort_direction = sort_direction)
    if all_users:
        return ResponseSchema(status = True, response = msg['user_list_found'], data = all_users.items)
    else:
        return ResponseSchema(status = False, response = msg['user_list_not_found'], data = None)



# Get user information by id
@router.get('/{id}', summary="Get user",  response_model = ResponseSchema[UserResponseSchema], dependencies = [Depends(JWTBearer())])

def get_user(id: int, db: Session = Depends(get_db)):
    user = user_service.show_user(id = id, db = db)
    if user is not None:
        return ResponseSchema(status = True, response = msg['get_user_by_id'], data = user)
    else:
        return ResponseSchema(status = False, response = msg['get_user_by_id_not_found'], data = None)



# Delete user by id
@router.delete('/delete/{id}', summary="Delete user", response_model = ResponseSchema[UserResponseSchema], dependencies = [Depends(JWTBearer())])

def delete_user(id: int, db: Session = Depends(get_db)):
    delete_user = user_service.delete_user_info(id = id, db = db)
    if delete_user is not None: 
        return ResponseSchema(status = True, response = msg['delete_user_by_id'], data = delete_user.__dict__)
    else:
        return ResponseSchema(status = False, response = msg['delete_user_by_id_not_found'], data = None)



# Update current logged user
@router.put('/update', summary="Update user",  response_model = ResponseSchema[UserResponseSchema], dependencies = [Depends(JWTBearer())])

def update_user_info(user_update_data: UserUpdateSchema, token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
    update_user = user_service.update_user_info(user_update_data = user_update_data, token = token, db = db)
    if update_user:
        return ResponseSchema(status = True, response = msg['update_current_logged_user'], data = update_user.__dict__)
    else:
        return ResponseSchema(status = False, response = msg['update_current_logged_user_error'], data = None)

