from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from fastapi import FastAPI
from config.database import engine, Base
from config.database import SessionLocal
from fastapi_pagination import add_pagination
from app.modules.user import user_route
from app.modules.login import login_route
from app.modules.forgot_password import forget_password_route
from app.modules.company import company_routes
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Ensure uploads directory exists, if not then create it
upload_dir = os.path.join(os.getcwd(), "uploads")
user_dir = os.path.join(upload_dir, "user")
company_dir = os.path.join(upload_dir, "company")

os.makedirs(user_dir, exist_ok=True)
os.makedirs(company_dir, exist_ok=True)

# Mount the uploads directory as a static file route
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

add_pagination(app)

Base.metadata.create_all(bind = engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

session = SessionLocal()

@app.get("/")
def welcome():
    return {"message": "Welcome to the FastAPI Project"}

app.include_router(login_route.router)
app.include_router(user_route.router)
app.include_router(company_routes.router)
app.include_router(forget_password_route.router)



if __name__ == '__main__':
    uvicorn.run("main:app", host = '192.168.1.53', port = 8000, log_level = "info", reload = True)
    print("running")

