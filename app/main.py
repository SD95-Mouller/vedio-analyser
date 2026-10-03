from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1.analyze import router as analyze_router

app = FastAPI()
app.include_router(analyze_router, prefix="/api")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"code": 400, "message": "请求参数校验失败", "data": None},
    )

@app.get("/")
async def root():
    return {"message": "Hello World"}