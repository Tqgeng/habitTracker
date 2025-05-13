from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn


from app.api import auth, habits
# from app.db import models 

app = FastAPI()

app.include_router(auth.router)
app.include_router(habits.router)

app.mount('/frontend', StaticFiles(directory='app/frontend'))

@app.get('/', tags=['Root'], summary='Test API')
def read_root():
    return FileResponse('app/frontend/register.html')
    # return {'message': 'hello it is good'}

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)