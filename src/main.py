from fastapi import FastAPI, Request, 


app = FastAPI()

class RedirectPair(BaseModel):
    id: int
    redirectUrl: str
    shortUrl:str


app.get("/")
def landingMethod(source: string, request: Request):
    logRequestDetails(source, request)
    redirectUrl = findRedirectUrl(request)
    return RedirectResponse(url=redirectUrl)

app.get("/register")
def getRegisterRecords():
    return {'hooo', 'heeyyyy'}

app.post("/register")
def postNewRegisterRecord(record: RedirectPair):
    return {'hooo', 'heeyyyy'}


# Services

def logRequestDetails(source: string, request: Request):
    hi = "hi"