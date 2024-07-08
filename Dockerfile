FROM python:3.12.2

WORKDIR /idf-site

COPY ./requirements.txt ./idf-site/requirements.txt

RUN pip install --no-cache-dir -r /idf-site/requirements.txt

COPY . ./idf-site

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


