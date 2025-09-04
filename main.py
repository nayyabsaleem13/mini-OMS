from typing import List, Optional
from beanie import init_beanie
from fastapi import Depends, FastAPI , HTTPException, Query
from fastapi_pagination import Page, add_pagination, paginate
from motor.motor_asyncio import AsyncIOMotorClient

from models import AccessControl, CreateUser, Products, SigninPayload, User
from responses.user import AuthResponse, UserJWTtoken, UserResponse
from utils.security import create_access_token, get_current_user, hash_password, verify_password

app = FastAPI()
add_pagination(app)

@app.on_event("startup")
async def app_init():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database= client.project1,document_models=[User,Products,AccessControl])
    print("DB connection successfull")


@app.post("/sign-in")
async def sign_in(payload:SigninPayload):
    user = await User.find_one(payload.email == User.email)
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=400,detail="Invalid credentials")
    else:
        access_token = create_access_token(data= {"email":user.email})
        response = AuthResponse(
            token= access_token,
            user= UserResponse(
                _id=str(user.id),
                name = user.name,
                email = user.email,
                phone = user.phone,
                role = user.role
            )
        )
        return response

    
@app.post("/sign-up")
async def sign_up(payload: CreateUser):
    existing_user = await User.find_one(User.email == payload.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=payload.name,
        phone=payload.phone,
        email=payload.email,
        password=hash_password(payload.password),
        role=payload.role
    )
    await new_user.insert()

    access_control = AccessControl(userid=new_user.id)  
    await access_control.insert()

    access_token = create_access_token(data={"email": payload.email})
    response = AuthResponse(
        token=access_token,
        user=UserResponse(
            _id=new_user.id, 
            name=new_user.name,
            email=new_user.email,
            phone=new_user.phone,
            role=new_user.role
        )
    )
    return response


@app.post("/create-product", response_model=Products)
async def create_product(
    product: Products,
    current_user: UserJWTtoken = Depends(get_current_user)
):
    if current_user.role != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can add new products")
    if not product.vendor:
        product.vendor = current_user.name
    await product.insert()
    return product


@app.get("/get-all-products", response_model=Page[Products])
async def get_all_products(search: Optional[str] = Query(None)):
    query = {}
    if search:
        query = {"title": {"$regex": search, "$options": "i"}}
    
    products = await Products.find(query).to_list()
    return paginate(products)

    