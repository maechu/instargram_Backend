from fastapi import FastAPI

from api import test_api
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
def include_router(app):
    app.include_router(test_api.router, prefix='/test')
    
def start_application():
    app = FastAPI()
    origins = [
		"*"
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    include_router(app)
    # app.mount('/static/images', StaticFiles(directory="static/images", html=True), name="static")
    return app



app = start_application()

