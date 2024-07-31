FROM python:3.12.4
WORKDIR /bot
COPY requirements.txt /bot/
RUN pip install -r requirements.txt
COPY . /bot
RUN mkdir -p bot/logs
EXPOSE 8080
CMD python __main__.py