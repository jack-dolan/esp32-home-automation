from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import devices, states

from app.api.routes import devices

app = FastAPI(title="Home Automation Device Management Service")

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In prod, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(devices.router, prefix="/devices", tags=["devices"])
app.include_router(states.router, prefix="/states", tags=["states"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Home Automation Device Management Service"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)