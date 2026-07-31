### Klasna - шкільний електронний журнал та щоденник

```bash
# run app
uv run fastapi dev main.py

# test app
uv run pytest

# get code coverage
uv run pytest --cov=src/klasna

# get lines not covered with tests
uv run pytest --cov=src/klasna --cov-report=term-missing
```
