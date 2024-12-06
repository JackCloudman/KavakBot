import os

import uvicorn
from fastapi import FastAPI

from app.bootstrap.bootstrapper import bootstrap

app: FastAPI = bootstrap()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0',
                port=int(os.getenv('PORT', 8080)),
                reload=bool(os.getenv('RELOAD', False)))
