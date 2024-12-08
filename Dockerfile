##********************** MAIN BUILD **********************##
FROM python:3.12-alpine


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Set the working directory in the container
WORKDIR /usr/src/app



# Copy  requirements.txt from the current directory 
COPY ./requirements.txt ./requirements.txt


# Install dependencies and the package
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt && \
    rm -rf /root/.cache/pip



# Run cve-trove when the container launches
ENTRYPOINT [ "tail", "-f", "/dev/null" ]