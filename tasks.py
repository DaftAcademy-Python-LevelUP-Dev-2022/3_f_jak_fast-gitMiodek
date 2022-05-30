import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()


@app.get('/start', response_class=HTMLResponse)
def html_static():
    return '''
    <html>
        <head>
            
        </head>
        <body>
            <h1>The unix epoch started at 1970-01-01</h1>
        </body>
    </html>
    
    '''


security = HTTPBasic()


def check_usr_psw(credentials: HTTPBasicCredentials = Depends(security)):
    if (2022 - int(credentials.password.split('-')[0])) < 16 or int(credentials.password.split('-')[1]) > 12:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong date format or not old enough",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.password, credentials.username


@app.post('/check', response_class=HTMLResponse)
def get_usr(username: str = Depends(check_usr_psw), password: str = Depends(check_usr_psw)):
    wiek = (2022 - int(password.split('-')[0]))
    return f'''
<html>
        <head>
            
        </head>
        <body>
            <h1>Welcome {username}! You are {wiek}</h1>
        </body>
    </html>
'''
from pydantic import BaseModel
class Login(BaseModel):
    login: str
    password: str
@app.post('/test',response_class=HTMLResponse)
def post_login(item: Login):
    return f'''
<html>
        <head>
            
        </head>
        <body>
            <h1>Welcome {item.login}! You are {item.password}</h1>
        </body>
    </html>
'''