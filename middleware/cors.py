# middleware/cors.py
from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):
    origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,          # Which origins can access
        allow_credentials=True,         # Allow cookies / Authorization headers
        allow_methods=["*"],            # GET, POST, PUT, DELETE, etc.
        allow_headers=["*"],            # Allow all headers
    )
