FROM python:3.12

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY scripts/fetch_fake_data.py scripts/
COPY app/ app/

# Run fetch_fake_data.py script on container start
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000","python", "fetch_fake_data.py"]

