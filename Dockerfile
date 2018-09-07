FROM python:latest
RUN pip install pyscaffold==3.1rc2
WORKDIR /code
COPY . /code/
RUN python setup.py install

RUN git config --global user.email "you@example.com"
RUN  git config --global user.name "Your Name"

WORKDIR /test
RUN putup --custom-extension --no-skeleton some_extension

WORKDIR /test/some_extension
RUN python setup.py install
WORKDIR /test
RUN putup --some-extension result_project
WORKDIR /test/result_project
