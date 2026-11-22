from fastapi import FastAPI

app = FastAPI(title="RHC API")


@app.get("/health")
def health():
    """서버가 살아 있는지 확인하는 가장 작은 엔드포인트"""
    return {"status": "ok"}