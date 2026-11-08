FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORTFOLIO_INTEGRATION_DB=/app/data/portfolio-integration.db
WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir . && useradd --create-home --uid 10001 appuser && mkdir -p /app/data && chown -R appuser:appuser /app
USER appuser
EXPOSE 8003
CMD ["uvicorn", "portfolio_integration.main:app", "--host", "0.0.0.0", "--port", "8003", "--app-dir", "src"]
