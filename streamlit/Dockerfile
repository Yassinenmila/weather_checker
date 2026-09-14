FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBITECODE=1 

COPY streamlit/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt 

COPY streamlit/app.py .
COPY src/ ./src/

EXPOSE 8501

CMD [ "streamlit" , "run" , "app.py" , "--server.address=0.0.0.0" ]


