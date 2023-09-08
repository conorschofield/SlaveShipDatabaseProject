FROM python:alpine

RUN pip install mysql-connector-python openpyxl

WORKDIR /usr/src/app
COPY workbooks workbooks
COPY betterimport.py .
COPY create.sql .
COPY hcaconcordance hcaconcordance
COPY hcacourts hcacourts
COPY hcadateparser hcadateparser

CMD [ "python", "./betterimport.py" ]
