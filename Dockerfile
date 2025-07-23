    # Dockerfile pour Render - BlackPyReconX
    FROM python:3.11.9-slim

    WORKDIR /app

    COPY . .

    RUN pip install --upgrade pip && pip install -r requirements.txt

    EXPOSE 10000

    RUN chmod +x start.sh
    CMD ["./start.sh"]


