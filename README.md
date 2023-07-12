# Group Chat

Abstract: This application is a web service for group chat application

## Installation Instructions

- Clone this repository
- Setup Virtual Environment and activate it

```
virtualenv venv
source venv/Scripts/activate
```

- Install the dependencies

```
pip install -r requirements.txt
```

- Run the test application to setup some data

```
pytest test.py
```

- Run the main application

```
uvicorn server:app --port 3000
```

Visit http://localhost:3000/docs to view the documentation and interact with the swagger UI

## Directory Hierarchy

```

|—— chatapp
|    |—— database.py
|    |—— models.py
|    |—— schemas.py
|    |—— utils.py
|    |—— __init__.py
|
|—— requirements.txt
|—— server.py
|—— test.py

```

## Code Details

Implementation using FastAPI, Pydantics and SQLAlchemy

### Tested Platform

- software

  ```
  OS: Windows 11
  Python: 3.8.5

  ```

- hardware
  ```
  CPU: Intel Core i5
  ```

## License

MIT License

## Citing

Please connect to contribute
