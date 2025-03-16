FROM python:3.12-slim

WORKDIR /app

# Set non-root user name and group
# In case host user has other UID, entrypoint will take them
# From environment variables when container will be run
ARG UID=1001
ARG GID=1001

# Set non-root user and groups names as env variables
ENV APPUSER=appuser
ENV APPGROUP=appgroup
ENV APPUSER_HOME=/home/appuser

# We create user here
RUN apt-get update && \
    apt-get install gosu && \
    groupadd -g ${GID} ${APPGROUP} && \
    useradd -u ${UID} -g ${APPGROUP} -m -d ${APPUSER_HOME} ${APPUSER}

# Dependencies change less than code - so move it up
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Note that persmissions nust be set for current user that runs docker run
ADD . /app

RUN chmod +x /app/entrypoint.sh

# If user on host has other UID/GID - they will be updated
ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD ["python", "./bot.py"]
