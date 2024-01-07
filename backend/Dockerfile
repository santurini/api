FROM python:3.10
RUN mkdir -p /backend/app
WORKDIR /backend 

COPY requirements.txt /backend
RUN pip install --requirement /backend/requirements.txt

COPY ./app /backend/app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host=0.0.0.0" , "--reload" , "--port", "8000"]