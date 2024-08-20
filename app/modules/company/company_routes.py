from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi_pagination import Params
from sqlalchemy.orm import Session
from app.auth.jwt_bearer import JWTBearer
from app.auth.jwt_handler import decode_jwt_token
from app.models.company_model import CompanyModel
from app.models.user_company_model import UserCompany
from app.models.user_model import UserModel
from app.modules.company import company_service
from app.schemas.user_company_schema import UserCompanySchema
from config.database import get_db, msg
from typing import List, Optional
from app.schemas.response_schema import ResponseSchema
from app.schemas.company_response_schema import CompanyDetailsSchema, CompanyResponseSchema, CompanyWithUsersSchema
from app.schemas.company_update_schema import CompanyUpdateSchema

router = APIRouter(prefix="/company", tags = ["Company"])


# Register a new company
@router.post("/register", summary="Register a new company", response_model=ResponseSchema[CompanyResponseSchema], dependencies=[Depends(JWTBearer())])
async def register_company(company_name: str = Form(...), company_email: str = Form(...), company_number: str = Form(...), company_zipcode: Optional[str] = Form(None), company_city: Optional[str] = Form(None), company_state: Optional[str] = Form(None), company_country: Optional[str] = Form(None), company_profile: Optional[UploadFile] = File(None), db: Session = Depends(get_db), token: str = Depends(JWTBearer())):

    email = decode_jwt_token(token)
    if email is None:
        return ResponseSchema(status=False, response=msg['wrong_token'], data=None)

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user or user.role_id != 1:
        return ResponseSchema(status=False, response=msg["create_not_authorized"], data=None)

    new_company = await company_service.create_company(company_name=company_name, company_email=company_email, company_number=company_number, company_zipcode=company_zipcode, company_city=company_city, company_state=company_state, company_country=company_country, company_profile=company_profile, user_id=user.id, db=db)


    if new_company:
        return ResponseSchema(status=True, response=msg["company_register"], data=new_company)
    else:
        return ResponseSchema(status=False, response=msg["company_already_exists"], data=None)
    


# Get all company list 
@router.get("/list", summary="List of companies", response_model=ResponseSchema[List[CompanyResponseSchema]], dependencies=[Depends(JWTBearer())])
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
@router.get("/{company_id}", summary = "Get company information by ID", response_model = ResponseSchema[CompanyResponseSchema], dependencies = [Depends(JWTBearer())])
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
@router.delete("/delete/{company_id}", summary="Delete company by ID", response_model=ResponseSchema[CompanyResponseSchema], dependencies=[Depends(JWTBearer())])
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
@router.put("/update/{company_id}", summary="Update company by ID", response_model=ResponseSchema[CompanyResponseSchema], dependencies=[Depends(JWTBearer())])
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
    


# add user in the specific company 
@router.post("/add_user/{company_id}/{user_id}", summary = "Add user to a company", response_model = ResponseSchema[UserCompanySchema], dependencies = [Depends(JWTBearer())])
def add_user_to_company_route(company_id: int, user_id: int, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    email = decode_jwt_token(token)

    if email is None:
        return ResponseSchema(status = False, response = msg["wrong_token"], data = None)

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        return ResponseSchema(status = False, response = msg["user_not_found"], data = None)


    # check if the user has role_id 2 (companyadmin)
    if user.role_id != 2:
        return ResponseSchema(status = False, response = msg["not_authorized"], data = None)


    # check if the company exists in the database
    company = db.query(CompanyModel).filter(CompanyModel.id == company_id).first()
    if not company:
        return ResponseSchema(status = False, response = msg["company_not_found"], data = None)


    # add the user to the company
    user_to_add = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user_to_add:
        return ResponseSchema(status = False, response = msg["user_to_add_not_found"], data = None)
    

    # check if the user already in the company
    existing_user_company = db.query(UserCompany).filter_by(user_id = user_id, company_id = company_id).first()
    if existing_user_company:
        return ResponseSchema(status = False, response = msg["user_already_in_company"], data = None)


    # check if the user is already associated with any other company
    user_association = db.query(UserCompany).filter_by(user_id=user_id).first()
    if user_association:
        user_associated_company = db.query(CompanyModel).filter(CompanyModel.id == user_association.company_id).first()
        return ResponseSchema(status = False, response = msg["user_in_another_company"].format(company_name = user_associated_company.company_name), data = None)

    result = company_service.add_user_to_company(company_id = company_id, user_id = user_id, db = db)
    if result:
        user_company_schema = UserCompanySchema(
            user_id = result.user_id,
            company_id = result.company_id,
            user_name = user_to_add.name,  
            user_email = user_to_add.email,
            company_name = company.company_name,  
            company_email = company.company_email
        )
        return ResponseSchema(status = True, response = msg["user_added_to_company"], data = user_company_schema)
    else:
        return ResponseSchema(status = False, response = msg["user_add_failed"], data = None)




# get all users of a company 
@router.get("/userlist/{company_id}", summary="Get company details with associated users", response_model=ResponseSchema[CompanyWithUsersSchema], dependencies=[Depends(JWTBearer())])
def get_company_with_users_route(company_id: int, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    email = decode_jwt_token(token)

    if email is None:
        return ResponseSchema(status = False, response = msg["wrong_token"], data = None)

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        return ResponseSchema(status = False, response = msg["user_not_found"], data = None)

    company_with_users = company_service.get_company_users(company_id = company_id, db = db)
    
    if company_with_users:
        if not company_with_users.users:
            return ResponseSchema(status = True, response = msg["no_users_found"], data = company_with_users)
        return ResponseSchema(status = True, response = msg["users_found"], data = company_with_users)
    else:
        return ResponseSchema(status = False, response = msg["company_not_found"], data = None)


# @router.get("/companyinfo/{company_id}", response_model=ResponseSchema[CompanyDetailsSchema])
@router.get("/companyinfo/{company_id}", response_model=ResponseSchema)

def get_company_details(company_id: int, db: Session = Depends(get_db)):
    company_details = company_service.get_company_details_by_id(company_id=company_id, db=db)
    
    if company_details is None:
        return ResponseSchema(status = False, response = msg["company_not_found"], data = None)
    else:
        return ResponseSchema(status = True, response = msg["company_details_fetched"], data = company_details)
    