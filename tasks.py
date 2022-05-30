import secrets
from fastapi import Depends, FastAPI, HTTPException, status, Response
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
from typing import Union


@app.get('/info')
def header(format: Union[str, None] = None, user_agent: str = Header(default=None)):
    if format == 'html':
        html_content = f'<input type="text" id=user-agent name=agent value="{user_agent}">'
        return HTMLResponse(content=html_content, status_code=200)

    elif format == 'json':
        return {
            "user_agent": user_agent
        }


    else:
        return HTMLResponse(status_code=400)


lst = []


@app.put('/save/{string}')
def use_path(string: str):
    lst.append(string)
    return HTMLResponse(status_code=200)


@app.get('/save/{string}')
def check_path(string: str, response: Response):
    if string not in lst:
        return HTMLResponse(status_code=404)
    else:
        response.headers['Location'] = 'info'
        return response, HTMLResponse(status_code=301)
@app.delete('/save/{string}')
def del_string(string: str):
    lst.remove(string)

