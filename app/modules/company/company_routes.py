from fastapi import APIRouter, Depends
from fastapi_pagination import Params
from sqlalchemy.orm import Session
from app.auth.jwt_bearer import JWTBearer
from app.auth.jwt_handler import decode_jwt_token
from app.models.user_model import UserModel
from app.modules.company import company_service
from config.database import get_db, msg
from typing import List, Optional
from app.schemas.response_schema import ResponseSchema
from app.schemas.company_response_schema import CompanyResponseSchema
from app.schemas.company_register_schema import CompanyRegisterSchema
from app.schemas.company_update_schema import CompanyUpdateSchema

router = APIRouter(tags = ["Company"])

# # Register a new company
# @router.post("/company/register", summary="Register a new company", response_model=ResponseSchema[CompanyResponseSchema], dependencies=[Depends(JWTBearer())])
# def register_company(company: CompanyRegisterSchema, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
#     email = decode_jwt_token(token)
    
#     if email is None:
#         return None

#     user = db.query(UserModel).filter(UserModel.email == email).first()
#     if not user:
#         return None

#     new_company = company_service.create_company(company=company, user_id=user.id, db=db)

#     if new_company:
#         return ResponseSchema(status=True,  response=msg["company_register"],  data=new_company.__dict__)
#     else:
#         return ResponseSchema(status=False,  response=msg["company_already_exists"],  data=None)



# # Get all company list 
# @router.get("/company/list", summary="List of company", response_model = ResponseSchema[List[CompanyResponseSchema]], dependencies = [Depends(JWTBearer())])
# def list_companies(params: Params = Depends(), db: Session = Depends(get_db), sort_by: Optional[str] = None, sort_direction: Optional[str] = None):
#     all_company = company_service.get_all_company(db = db, params = params, sort_by = sort_by, sort_direction = sort_direction)
#     if all_company:
#         return ResponseSchema(status = True, response = msg["company_list_found"], data = all_company.items) 
#     else:
#         return ResponseSchema(status = False, response = msg["company_list_not_found"], data = None)
    


# # Get company information by id 
# @router.get("/company/{company_id}", summary = "Get company information by id", response_model = ResponseSchema[CompanyResponseSchema], dependencies = [Depends(JWTBearer())])
# def view_company(company_id: int, db: Session = Depends(get_db)):
#     get_company = company_service.get_company_by_id(company_id = company_id, db = db)
#     if get_company is not None:
#         return ResponseSchema(status = True, response = msg["get_company_by_id"], data = get_company.__dict__)
#     else:
#         return ResponseSchema(status = False, response = msg["get_company_by_id_not_found"], data = None)
    


# # Delete compapny by id
# @router.delete("/company/{company_id}", summary = "Delete company by id", response_model = ResponseSchema[CompanyResponseSchema], dependencies = [Depends(JWTBearer())])
# def delete_company(company_id: int, db: Session = Depends(get_db)):
#     delete_company = company_service.delete_company_by_id(company_id = company_id, db = db)
    # if delete_company is not None:
    #     return ResponseSchema(status = True, response = msg["delete_company_by_id"], data = delete_company.__dict__)
    # else:
    #     return ResponseSchema(status = False, response = msg["delete_company_by_id_not_found"], data = None)
    
    

# # Update company by id
# @router.put("/company/{company_id}", summary="Update company by id", response_model = ResponseSchema[CompanyResponseSchema], dependencies = [Depends(JWTBearer())])
# def update_company(company_data: CompanyUpdateSchema, company_id: int, db: Session = Depends(get_db)):
#     updated_company = company_service.update_company_by_id(update_data = company_data, company_id = company_id, db = db)
#     if updated_company:
#         return ResponseSchema(status = True, response = msg["update_company_by_id"], data = updated_company.__dict__)
#     else:
#         return ResponseSchema(status = False, response = msg["update_company_by_id_not_found"], data = None)




# Register a new company
@router.post("/company/register", summary="Register a new company", response_model=ResponseSchema[CompanyResponseSchema], dependencies=[Depends(JWTBearer())])
def register_company(company: CompanyRegisterSchema, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    email = decode_jwt_token(token)
    
    if email is None:
        return None

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        return None

    # if the user has role_id 1 (superadmin) to allow register a company
    if user.role_id != 1:
        return ResponseSchema(status = False, response = msg["create_not_authorized"], data=None)

    new_company = company_service.create_company(company = company, user_id = user.id, db = db)

    if new_company:
        return ResponseSchema(status = True, response = msg["company_register"], data = new_company.__dict__)
    else:
        return ResponseSchema(status = False, response = msg["company_already_exists"], data = None)




# Get all company list 
@router.get("/company/list", summary="List of companies", response_model=ResponseSchema[List[CompanyResponseSchema]], dependencies=[Depends(JWTBearer())])
def list_companies(params: Params = Depends(), db: Session = Depends(get_db), sort_by: Optional[str] = None, sort_direction: Optional[str] = None, token: str = Depends(JWTBearer())):
    email = decode_jwt_token(token)
    
    if email is None:
        return None

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        return None

    # if the user has role_id 1 (superadmin) to allow company list view
    if user.role_id != 1:
        return ResponseSchema(status = False, response = msg["view_not_authorized"], data=None)

    all_company = company_service.get_all_company(db = db, params = params, sort_by = sort_by, sort_direction = sort_direction)
    if all_company:
        return ResponseSchema(status = True, response = msg["company_list_found"], data = all_company.items) 
    else:
        return ResponseSchema(status = False, response = msg["company_list_not_found"], data = None)
    

    

# Get company information by id 
@router.get("/company/{company_id}", summary = "Get company information by ID", response_model = ResponseSchema[CompanyResponseSchema], dependencies = [Depends(JWTBearer())])
def view_company(company_id: int, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    email = decode_jwt_token(token)
    
    if email is None:
        return None
    
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        return None
    
    # if the user has role_id 1 (superadmin) and role_id 2 (companyadmin) to allow view a company
    if user.role_id != 1 and user.role_id != 2:
        return ResponseSchema(status = False, response = msg["not_allowed_to_view"], data = None)

    get_company = company_service.get_company_by_id(company_id = company_id, db = db)
    if get_company is not None:
        return ResponseSchema(status = True, response = msg["get_company_by_id"], data = get_company.__dict__)
    else:
        return ResponseSchema(status = False, response = msg["get_company_by_id_not_found"], data = None)



# Delete compapny by id
@router.delete("/company/{company_id}", summary="Delete company by ID", response_model=ResponseSchema[CompanyResponseSchema], dependencies=[Depends(JWTBearer())])
def delete_company(company_id: int, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    email = decode_jwt_token(token)
    
    if email is None:
        return None
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        return None

    # Check if the user has role_id 1 (superadmin) to allow deletion
    if user.role_id != 1:
        return ResponseSchema(status = False, response = msg["delete_not_authorized"], data = None)

    delete_company = company_service.delete_company_by_id(company_id = company_id, db = db)
    if delete_company is not None:
        return ResponseSchema(status = True, response = msg["delete_company_by_id"], data = delete_company.__dict__)
    else:
        return ResponseSchema(status = False, response = msg["delete_company_by_id_not_found"], data = None)

    
    
# Update company by id
@router.put("/company/{company_id}", summary="Update company by ID", response_model=ResponseSchema[CompanyResponseSchema], dependencies=[Depends(JWTBearer())])
def update_company(company_data: CompanyUpdateSchema, company_id: int, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    email = decode_jwt_token(token)
    
    if email is None:
        return None

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        return None

    # Check if the user has role_id 1 (superadmin) to allow updates
    if user.role_id != 1:
        return ResponseSchema(status = False, response = msg["update_not_authorized"], data = None)

    updated_company = company_service.update_company_by_id(company_id = company_id, db = db, company_data = company_data)
    if updated_company:
        return ResponseSchema(status = True, response = msg["update_company_by_id"], data = updated_company.__dict__)
    else:
        return ResponseSchema(status = False, response = msg["update_company_by_id_not_found"], data = None)

