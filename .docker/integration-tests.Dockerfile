FROM python:3.12-slim
WORKDIR /integration-tests
COPY ./integration-tests ./
RUN pip install --no-cache-dir -r requirements.txt
ENV ENV_FILE_PATH .env
CMD if [ "$CI" = "true" ]; then \
        echo "Running on CI"; \
        pytest -s --alluredir=allure-results; \
    else \
        echo "Running on local"; \
        pytest -s; \
    fi