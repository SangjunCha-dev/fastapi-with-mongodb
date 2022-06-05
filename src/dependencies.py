from fastapi import Header, HTTPException


async def get_token_header(x_token: str = Header()):
    if x_token != "fake-token":
        raise HTTPException(status_code=400, detail="X-Tokent header invalid")

async def get_query_token(token: str):
    if token != "tester":
        raise HTTPException(status_code=400, detail="No tester token provided")
