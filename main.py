from fastapi import Depends,FastAPI
from fastapi.security import OAuth2PasswordBearer

from db.db import * 


from typing import Optional, Union
from pydantic import BaseModel
from models import samples as samples_model

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


@app.get("/")
async def root(token: str = Depends(oauth2_scheme)):
    return {"token": token}

@app.get("/samples")
async def read_samples():
    samples = await get_all_samples()

    return samples

@app.get("/samples/{sample_id}")
async def sample(sample_id: str):
    return await get_single_sample(sample_id)

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user