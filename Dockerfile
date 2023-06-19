FROM python:3.10

ADD variables.py .

ADD logic.py .

ADD app.py .

RUN pip install customtkinter numpy matplotlib

CMD [ "python3", "./app.py"]
