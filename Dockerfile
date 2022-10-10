FROM python:3.8

RUN pip install poetry
RUN mkdir /src
WORKDIR /src

COPY poetry.lock pyproject.toml /src/
RUN poetry config virtualenvs.create false \
  && poetry install --only main --no-interaction --no-ansi

COPY cncsmart /src/cncsmart
COPY data /src/data

ENV PYTHONPATH=$PWD:$PYTHONPATH

EXPOSE 8000
ENTRYPOINT ["uvicorn", "cncsmart.main:app", "--host", "0.0.0.0", "--port", "8022"]
