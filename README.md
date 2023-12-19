# participa

## Development

### Create or activate virtual environment

```bash
python -m venv env
source env/bin/activate
```


### Install dependencies

```bash
pip install -r requirements.txt
```

### Run migrations

```bash
python manage.py migrate
```

### Run server

```bash
python manage.py runserver
```

### Run tailwind
```bash
python manage.py tailwind start
```

## Internationalization (polis app)



### Extract strings

```bash
python manage.py makemessages -l es
```

### Compile strings

```bash
python manage.py compilemessages
```
