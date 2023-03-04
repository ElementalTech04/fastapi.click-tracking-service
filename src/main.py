from os import environ

from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.security import APIKeyHeader, HTTPBasic, HTTPBasicCredentials
from redis import Redis
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

app = FastAPI()

# configure rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# configure redis connection
redis = Redis(host=environ.get("REDIS_CONN_HOST"), port=environ.get("REDIS_CONN_PORT"),
              password=environ.get("REDIS_CONN_PW"))

# API key security
api_key = APIKeyHeader(name="X-API-Key")
api_key_value = "mysecretapikey"

# HTTP basic auth security
security = HTTPBasic()


# endpoints
@app.get("/")
async def redirect(request: Request, redirection_url: str = ''):
    if redirection_url == '':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing redirection_url in request body")
    destination_url = redis.get(redirection_url)
    if not destination_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Redirection URL not found")
    return RedirectResponse(url=destination_url)


@app.get("/registration")
async def get_registrations(api_key: str = Depends(api_key)):
    registrations = {}
    for redirection_url, destination_url in redis.scan_iter("*"):
        registrations[redirection_url.decode()] = destination_url.decode()
    return registrations


@app.post("/registration")
async def create_registration(source_url: str, redirection_url: str,
                              credentials: HTTPBasicCredentials = Depends(security), api_key: str = Depends(api_key)):
    if not credentials.username == "admin" and credentials.password == "secret":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    redis.set(redirection_url, source_url)
    return {"message": "Registration created successfully"}


@app.delete("/registration")
async def delete_registration(redirection_url: str, credentials: HTTPBasicCredentials = Depends(security),
                              api_key: str = Depends(api_key)):
    if not credentials.username == "admin" and credentials.password == "secret":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    if not redis.delete(redirection_url):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Redirection URL not found")
    return {"message": "Registration deleted successfully"}
