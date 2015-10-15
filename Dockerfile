FROM python:2.7.10-slim

RUN mkdir /restgate
WORKDIR /restgate

COPY requirements.txt /restgate/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY requirements-tests.txt /restgate/requirements-tests.txt
RUN pip install --no-cache-dir -r requirements-tests.txt

COPY requirements-docs.txt /restgate/requirements-docs.txt
RUN pip install --no-cache-dir -r requirements-docs.txt

COPY . /restgate/
RUN python setup.py install
