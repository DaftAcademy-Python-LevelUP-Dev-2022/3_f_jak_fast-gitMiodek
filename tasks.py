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





@app.post('/check', response_class=HTMLResponse)
def get_usr(credentials: HTTPBasicCredentials = Depends(security)):
    if (2022 - int(credentials.password.split('-')[0])) < 16 or int(credentials.password.split('-')[1]) > 12:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong date format or not old enough",
            headers={"WWW-Authenticate": "Basic"},
        )

    return f'''

            <h1>Welcome {credentials.username}! You are {(2022 - int(credentials.password.split('-')[0]))}</h1>
     
'''

from fastapi import Header
@app.get('/info')
def header(format: str , user: str = Header(default=None)):
    if format == 'html':
        html_content = f'<input type="text" id=user-agent name=agent value="{user}">'
        HTMLResponse(content=html_content, status_code=200)
    elif format == 'json':
        return {
    "user_agent": f"{user}"
}
    else:
        return status.HTTP_400_BAD_REQUEST



