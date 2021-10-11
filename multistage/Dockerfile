FROM python:3.8.2 as base

FROM base as builder
RUN adduser --disabled-password --gecos '' blog
ENV PYTHONUNBUFFERED 1
COPY --chown=blog requirements/requirements.txt /tmp/
COPY --chown=blog ./multistage/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN --mount=type=cache,target=/root/.cache/pip \
     pip install -r /tmp/requirements.txt


FROM builder as dev

ENV DEBUG 1
WORKDIR /code
ENTRYPOINT ["/entrypoint.sh"]
CMD ["run_dev"]



