from fastapi import FastAPI, Request
from web.api import users, sets
from fastapi.responses import JSONResponse
import time

app = FastAPI()


app.include_router(users.router, prefix="/api/users")
app.include_router(sets.router, prefix="/api/v1/sets")


@app.middleware("http")
async def debug_middleware(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
    except Exception as e:
        print(f"\n⚠️ Błąd: {str(e)}")
        print(f"Ścieżka: {request.url.path}")
        response = JSONResponse(
            status_code=500,
            content={"detail": "Wewnętrzny błąd serwera"}
        )
    finally:
        process_time = time.time() - start_time
        status_code = response.status_code if response else 500
        print(f"{request.method} {request.url.path} - {status_code} ({process_time:.2f}s)")
        return response