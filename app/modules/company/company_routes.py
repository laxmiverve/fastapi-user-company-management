from fastapi import APIRouter, Depends, File, Form, Header, UploadFile
from fastapi_pagination import Params
from sqlalchemy.orm import Session
from app.auth.jwt_bearer import JWTBearer
from app.auth.jwt_handler import decode_jwt_token
from app.models.company_model import CompanyModel
from app.models.user_company_model import UserCompany
from app.models.user_model import UserModel
from app.modules.company import company_service
from app.schemas.company_register_schema import CompanyRegisterSchema
from app.schemas.user_company_schema import UserCompanySchema
from config.database import get_db, msg
from typing import List, Optional
from app.schemas.response_schema import ResponseSchema
from app.schemas.company_response_schema import CompanyResponseSchema, CompanyWithUsersSchema
from app.schemas.company_update_schema import CompanyUpdateSchema
from fastapi import Request


router = APIRouter(prefix="/company", tags = ["Company"])


# Register a new company
@router.post("/register", summary="Register a new company", response_model=ResponseSchema[CompanyResponseSchema], dependencies=[Depends(JWTBearer())])
async def register_company(company_data: CompanyRegisterSchema, request: Request, db: Session = Depends(get_db)):
    new_company = await company_service.create_company(company_data=company_data, request=request, db=db)

    if new_company == 1:
        return ResponseSchema(status=False, response=msg["invalid_email_format"], data=None)
    elif new_company == 2:
        return ResponseSchema(status=False, response=msg["create_not_authorized"], data=None)
    elif new_company:
        return ResponseSchema(status=True, response=msg["company_register"], data=new_company)
    else:
        return ResponseSchema(status=False, response=msg["company_already_exists"], data=None)


# Get all company list 
@router.get("/list", summary="List of companies", response_model=ResponseSchema[List[CompanyResponseSchema]], dependencies=[Depends(JWTBearer())])
def list_companies(request: Request, params: Params = Depends(), db: Session = Depends(get_db), sort_by: Optional[str] = None, sort_direction: Optional[str] = None):
    all_company = company_service.get_all_company(request=request, db=db, params=params, sort_by=sort_by, sort_direction=sort_direction)
    
    if all_company == 1:
        return ResponseSchema(status=False, response=msg["view_not_authorized"], data=None)
    elif all_company is None:
        return ResponseSchema(status=False, response=msg["company_list_not_found"], data=None)
    else:
        return ResponseSchema(status=True, response=msg["company_list_found"], data=all_company.items)



# Get company information by id 
@router.get("/{company_id}", summary="Get company information by ID", response_model=ResponseSchema[CompanyResponseSchema], dependencies=[Depends(JWTBearer())])
def view_company(company_id: int, request: Request, db: Session = Depends(get_db)):
    get_company = company_service.get_company_by_id(company_id=company_id, request=request, db=db)
    
    if get_company == 1:
        return ResponseSchema(status=False, response=msg["not_allowed_to_view"], data=None)
    elif get_company is None:
        return ResponseSchema(status=False, response=msg["get_company_by_id_not_found"], data=None)
    else:
        return ResponseSchema(status=True, response=msg["get_company_by_id"], data=get_company.__dict__)



# Delete compapny by id
@router.delete("/delete/{company_id}", summary="Delete company by ID", response_model=ResponseSchema[CompanyResponseSchema], dependencies=[Depends(JWTBearer())])
def delete_company(company_id: int, request: Request, db: Session = Depends(get_db)):
    delete_company = company_service.delete_company_by_id(company_id=company_id, request=request, db=db)
    
    if delete_company == 1:
        return ResponseSchema(status=False, response=msg["delete_not_authorized"], data=None)
    elif delete_company is None:
        return ResponseSchema(status=False, response=msg["delete_company_by_id_not_found"], data=None)
    else:
        return ResponseSchema(status=True, response=msg["delete_company_by_id"], data=delete_company.__dict__)

    
    
# Update company by id
@router.put("/update/{company_id}", summary="Update company by ID", response_model=ResponseSchema[CompanyResponseSchema], dependencies=[Depends(JWTBearer())])
def update_company(company_id: int, request: Request, company_data: CompanyUpdateSchema, db: Session = Depends(get_db)):
    updated_company = company_service.update_company_by_id(company_id=company_id, company_data=company_data, request=request, db=db)
    
    if updated_company == 1:
        return ResponseSchema(status=False, response=msg["update_not_authorized"], data=None)
    elif updated_company is None:
        return ResponseSchema(status=False, response=msg["update_company_by_id_not_found"], data=None)
    else:
        return ResponseSchema(status=True, response=msg["update_company_by_id"], data=updated_company.__dict__)
    


# add user in the specific company 
@router.post("/add_user/{company_id}/{user_id}", summary="Add user to a company", response_model=ResponseSchema[UserCompanySchema], dependencies=[Depends(JWTBearer())])
def add_user_to_company_route(company_id: int, request: Request, user_id: int, db: Session = Depends(get_db)):
    result = company_service.add_user_to_company(company_id=company_id, user_id=user_id, request=request, db=db)
    
    if result == 1:
        return ResponseSchema(status=False, response=msg["user_not_found"], data=None)
    elif result == 2:
        return ResponseSchema(status=False, response=msg["not_authorized"], data=None)
    elif result == 3:
        return ResponseSchema(status=False, response=msg["company_not_found"], data=None)
    elif result == 4:
        return ResponseSchema(status=False, response=msg["user_to_add_not_found"], data=None)
    elif result == 5:
        return ResponseSchema(status=False, response=msg["user_already_in_company"], data=None)
    elif result == 6:
        return ResponseSchema(status=False, response=msg["user_in_another_company"], data=None)
    elif result is None:
        return ResponseSchema(status=False, response=msg["user_add_failed"], data=None)
    else:
        return ResponseSchema(status=True, response=msg["user_added_to_company"], data=result)



# get all users of a company by company_id
@router.get("/userlist/{company_id}", summary="Get company details with associated users", response_model=ResponseSchema[CompanyWithUsersSchema], dependencies=[Depends(JWTBearer())])
def get_company_with_users_route(company_id: int, request: Request, db: Session = Depends(get_db)):
    company_with_users = company_service.get_company_users(company_id=company_id, request=request, db=db)
    
    if company_with_users == 1:
        return ResponseSchema(status=False, response=msg["company_not_found"], data=None)
    elif company_with_users == 2:
        return ResponseSchema(status=False, response=msg["not_authorized"], data=None)
    elif company_with_users == 3:
        return ResponseSchema(status=False, response=msg["no_users_found"], data=None)
    else:
        return ResponseSchema(status=True, response=msg["users_found"], data=company_with_users)



# get created and updated time of the company
@router.get("/companyinfo/{company_id}", summary="Get created and updated time of the company", response_model=ResponseSchema, dependencies=[Depends(JWTBearer())])
def get_company_details(company_id: int, request: Request, db: Session = Depends(get_db)):
    company_details = company_service.get_company_details_by_id(company_id=company_id, db=db, request=request)
    
    if company_details is None:
        return ResponseSchema(status=False, response=msg["company_not_found"], data=None)
    elif company_details == 1:
        return ResponseSchema(status=False, response=msg["not_authorized"], data=None)
    else:
        return ResponseSchema(status=True, response=msg["company_details_fetched"], data=company_details)



# get company details by using UUID (pass the uuid in header)
@router.post("/info", summary="Get company details by UUID", response_model=ResponseSchema[CompanyResponseSchema], dependencies=[Depends(JWTBearer())])
def get_company_details(uuid: str = Header(None), db: Session = Depends(get_db)):
    company = company_service.get_company_by_uuid(uuid=uuid, db=db)

    if company:
        return ResponseSchema(status = True, response = msg["company_details_fetched"], data = company)
    else:
        return ResponseSchema(status = False, response= msg["company_not_found"], data= None)