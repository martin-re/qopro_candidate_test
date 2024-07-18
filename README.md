#### Dependecies

- python 3.8^
- docker

#### PostgreSQL setup
```bash
docker run --env=POSTGRES_PASSWORD=1234 --env=POSTGRES_DB=postgres --network=bridge -p 5432:5432 -d postgres
```

#### App standallone run
```python
pip install -r requirements.txt; python3 server.py
```

#### Gunicorn deployment
Unfortunatelly task is not completed, just prototype "server.py" is working but in standallone mode (not with gunicorn). "server2.py" uses the project structure, but it is not completed in the required deadline.