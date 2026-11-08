FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml .
COPY src ./src
RUN pip install --no-cache-dir .
RUN useradd --create-home appuser && mkdir -p /app/data && chown -R appuser:appuser /app/data
USER appuser
ENV DOCUMENT_INTELLIGENCE_DB=/app/data/documents.db
EXPOSE 8000
CMD ["uvicorn", "docintel.main:app", "--host", "0.0.0.0", "--port", "8000"]
