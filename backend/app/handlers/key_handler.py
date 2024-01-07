from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader

# list of registered API keys
api_keys = [
    "BigProfiles-API"
]

# create APIKeyHeader object to specify api key name for authentication
api_key_header = APIKeyHeader(name="x-api-key")

# define helper function to check if API key is valid otherwise raise auth error
def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )