from fastapi import FastAPI
from app.controllers.item_controller import router

# create app and include router
app = FastAPI()
app.include_router(router=router)