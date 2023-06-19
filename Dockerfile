FROM python:3.10

ADD app.py .

ADD logic.py .

RUN pip install customtkinter numpy matplotlib

CMD [ "python3", "./app.py"]