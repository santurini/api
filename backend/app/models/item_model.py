from pydantic import BaseModel, constr, conint

# define ingestion item model with constraints
class Item(BaseModel):
    key: conint(ge=1, le=6)
    payload: constr(min_length=10, max_length=255)