# setup

```bash
python -m venv vnev
> venv/scripts/activate
> pip install fastapi
> pip install pymongo  # mongodb
> pip install pymongo[srv] # mongodb
> pip install pydantic[email]
> pip install motor  # async client

# 비동기 서버 실행
> pip install uvicorn
```

# MongoDB 연결 URL변수 설정

```bash
export MONGODB_URL="mongodb+srv://<username>:<password>@<url>/<db>?retryWrites=true&w=majority"
```

# fastapi 시작
```
uvicorn app:app --reload
```