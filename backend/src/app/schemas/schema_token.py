from sqlmodel import SQLModel, Field

class TokenBase(SQLModel): 
    access_token: str = Field(nullable=False)
    token_type: str = "bearer"
    
class Token_payload(SQLModel): #
    sub: str | None = None

class Message(SQLModel): # message to client
    message: str