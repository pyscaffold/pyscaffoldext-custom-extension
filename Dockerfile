FROM python:latest
RUN pip install pyscaffold
WORKDIR /code
COPY . /code/
RUN python setup.py install

RUN git config --global user.email "you@example.com"
RUN  git config --global user.name "Your Name"

WORKDIR /test
RUN putup --custom-extension --no-skeleton test_extension
RUN ls test_extension
WORKDIR /test/test_extension
RUN ls .
RUN python setup.py install
RUN putup --test-extension /code/result_project

