FROM python:3.10

WORKDIR /marco

COPY . /marco/

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod -R 777 .

CMD ["python", "main.py"]
