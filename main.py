from fastapi import FastAPI
import uvicorn
from src.routes import user_profile
from src.routes import auth
from src.routes import photo
from src.routes import roles
from src.routes import comments
from src.routes import healthchecker


app = FastAPI()

@app.get("/", name='Home')
def read_root():
    return {"message": "Team6"} 

app.include_router(healthchecker.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(user_profile.profile_router, prefix="/api")
app.include_router(roles.router, prefix='/api')
app.include_router(photo.router, prefix='/api')
app.include_router(comments.router, prefix='/api')



