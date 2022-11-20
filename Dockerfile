FROM python:3.10.8-alpine
RUN pip install --upgrade pip
COPY . .
RUN rm -rf .venv/
RUN rm -rf .vscode/
RUN rm -rf .editorconfig
RUN rm -rf instance/
RUN pip install -r requirements.txt
EXPOSE 5000

CMD ["python", "serve.py"]
