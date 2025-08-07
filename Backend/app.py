from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Router import auth, chat, usage

app = FastAPI(title="MoonKnight Backend API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(usage.router)

@app.get("/")
def health_check():
    return {"status": "healthy", "message": "MoonKnight Backend API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
