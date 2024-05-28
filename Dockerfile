FROM python:3.12

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY scripts/fetch_fake_data.py scripts/
COPY app/ app/

ENTRYPOINT ["sh", "-c"]

CMD ["python scripts/fetch_fake_data.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

