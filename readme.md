# FastAPI With MongoDB

> FastAPI와 MongoDB를 사용한 간단한 RestAPI 서버 입니다.


# Tech/Framework Used

|명칭       |버전   |
|---        |---    |
|FastAPI    |0.78.0 |
|MongoDB    |5.0.8  |


# 라이브러리 설치

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

# 더빠른 json 처리
> pip install orjson
```


# DB 설정

- 설정 파일 : `src/config/settings.json`
- MongoDB Local 접속시 변수 형식
    ```bash
    export MONGODB_URL="mongodb://localhost:27017"
    ```
- MongoDB Cloud 접속시 변수 형식
    ```bash
    export MONGODB_URL="mongodb+srv://<username>:<password>@<url>/<db>?retryWrites=true&w=majority"
    ```


# 실행

## 1. FastAPI 서버 실행

```
> uvicorn src.main:app --reload
```

## 2. 접속

웹브라우저에서 `http://localhost:8000/docs` 주소로 접속
