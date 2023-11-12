from fastapi import FastAPI
import uvicorn
from src.routes import user_profile
from src.routes import auth
from src.routes import users

app = FastAPI()
app.include_router(auth.router, prefix="/api")
app.include_router(user_profile.profile_router, prefix="/api")
app.include_router(users.router, prefix='/api')

@app.get("/")
def read_root():
    return {"message": "REST APP v1.0"}

if __name__ == "__main__":
    uvicorn.run(app)