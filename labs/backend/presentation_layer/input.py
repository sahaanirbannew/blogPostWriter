from pydantic import BaseModel
from typing import Optional 


class Input_Payload(BaseModel):
    text: str