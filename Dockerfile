FROM python:3.8 AS builder

RUN pip install -U pip
RUN pip install "poetry<=1.2"
COPY . /src
WORKDIR /src
RUN poetry build

FROM python:3.8-slim

COPY --from=builder /src/dist/*.whl /package/
RUN pip install /package/*.whl
ENTRYPOINT [ "mars_rover" ]
