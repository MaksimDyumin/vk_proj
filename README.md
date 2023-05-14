# vk_proj

### if you want to start development:
You need to create .venv with python version 3.10.11, then use:
```
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

### if you want start docker file:

1) build container:

```
docker build -t name .
```

2) start container
```
docker run -p 8000:8000 --rm name
```