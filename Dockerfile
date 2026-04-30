FROM python:3.12-slim

WORKDIR /app

COPY . /app

# Baseline container for CI/CD image publishing.
# Replace CMD with actual Odoo startup once runtime dependencies are finalized.
CMD ["python", "-V"]
