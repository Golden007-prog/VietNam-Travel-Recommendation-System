FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py data_processing.py recommendation.py translation.py weather.py ./
COPY data/DataSet.xlsx data/

EXPOSE 8501

# Pass the weather key at runtime: docker run --env-file .env -p 8501:8501 <image>
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=8501"]
