# ----------------------------------------------------------------------------------------------------------------------
# Build stage
# ----------------------------------------------------------------------------------------------------------------------
ARG PYTHON_IMAGE=python:3.10-slim
FROM ${PYTHON_IMAGE} AS build-img

RUN apt-get update && \
    apt-get install -y virtualenv build-essential && \
    rm -rf /var/lib/apt/lists/*

# Create user and group
RUN useradd --uid 6016 -m -d /container container
USER container
RUN python3 -m venv /container/venv

COPY --chown=container sources/python /code
WORKDIR /code
RUN . /container/venv/bin/activate && pip install --upgrade pip && pip install --upgrade -r requirements.txt
RUN . /container/venv/bin/activate && python setup.py install

# ----------------------------------------------------------------------------------------------------------------------
# Target stage
# ----------------------------------------------------------------------------------------------------------------------
FROM ${PYTHON_IMAGE}

RUN apt-get update && apt-get install -y wait-for-it curl && rm -rf /var/lib/apt/lists/*

# Create user and group
RUN useradd --uid 6016 -m -d /container container
USER container

# App
COPY --chown=container sources/scripts /scripts
RUN chmod +x /scripts/*
COPY --chown=container sources/python /code

COPY --from=build-img /container/venv /container/venv

# Run
CMD /scripts/run.sh
