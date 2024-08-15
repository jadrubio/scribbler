# Use the Python 3 image specified in devcontainer.json
FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

WORKDIR /app

COPY .devcontainer/ /app/.devcontainer/
COPY . /app/

RUN sudo apt-get update && sudo apt-get install -y \
    && pip3 install --user -r /app/requirements.txt \
    && pip3 install --user streamlit

EXPOSE 8501

# Command to run the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]
