FROM python:3.8.0-slim
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update \
&& apt-get install gcc git ping -y \
&& apt-get clean

COPY ./ DashMachine
WORKDIR DashMachine
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "run.py"]