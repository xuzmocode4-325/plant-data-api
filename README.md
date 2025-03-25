# Plant API Application

## Dockerfile Specs:
*   `FROM python:3.13-alpine3.21` -  This instruction sets the base image for the Docker image to `python:3.13-alpine3.21`. This image is a lightweight Linux distribution based on Alpine Linux, with Python 3.13 pre-installed.
*   `LABEL maintainer="xuzmonomi.com"` - This adds metadata to the image, indicating that "xuzmonomi.com" is the maintainer of this image.
*   `ENV PYTHONBUFFERED=1` - This sets an environment variable `PYTHONBUFFERED` to `1`.  This ensures that the Python output is not buffered, which is useful for seeing logs in real-time.
*   `COPY ./requirements.txt /tmp/requirments.txt` - This instruction copies the `requirements.txt` file from the current directory (`./`) on the host to the `/tmp/requirments.txt` directory in the Docker image. This file likely contains a list of Python dependencies for the application.
*   `COPY ./requirements.dev.txt /tmp/requirements.dev.txt` - This copies the `requirements.dev.txt` file from the local directory to the `/tmp` directory in the Docker image. This file likely contains development-related Python dependencies.
*   `COPY ./app /app`[5] - This copies the entire `./app` directory from the host machine to the `/app` directory within the Docker image. This directory likely contains the application's source code.
*   `WORKDIR /app` - This sets the working directory for any subsequent `RUN`, `CMD`, `ENTRYPOINT`, `COPY`, and `ADD` instructions to `/app`. This means that commands will be executed from within this directory.
*   `EXPOSE 8000` - This exposes port 8000 on the container, making it accessible from the outside. However, it doesn't publish the port, which requires using the `-p` flag when running the container.
*   `ARG DEV=false` -  This defines a build-time argument named `DEV` and sets its default value to `false`. This argument can be used to conditionally execute commands during the image build process.
*   `RUN python -m venv /py && \ /py/bin/pip install --upgrade pip && \ apk add --update --no-cache postgresql-client && \ apk add --update --no-cache --virtual .tmp-build-deps \ build-base postgresql-dev musl-dev && \ /py/bin/pip install -r /tmp/requirments.txt && \ if [ $DEV = "true" ]; \ then /py/bin/pip install -r /tmp/requirements.dev.txt ; \ fi && \ rm -rf /tmp && \ apk del .tmp-build-deps && \ adduser \ --disabled-password \ --no-create-home \ app-user` - This `RUN` instruction executes a series of commands:
    *   `python -m venv /py` - Creates a Python virtual environment in the `/py` directory.
    *   `/py/bin/pip install --upgrade pip` -  Upgrades `pip` to the latest version within the virtual environment.
    *   `apk add --update --no-cache postgresql-client` - Installs the `postgresql-client` package using Alpine's package manager (`apk`). The `--no-cache` flag prevents caching the package, reducing the image size.
    *   `apk add --update --no-cache --virtual .tmp-build-deps build-base postgresql-dev musl-dev` - Installs build dependencies required for compiling Python packages with native extensions. The `--virtual .tmp-build-deps` creates a temporary installation environment named `.tmp-build-deps`.
    *   `/py/bin/pip install -r /tmp/requirments.txt` - Installs Python dependencies from the `requirements.txt` file within the virtual environment.
    *   `if [ $DEV = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt ; fi` - Conditionally installs development dependencies from `requirements.dev.txt` if the `DEV` argument is set to `"true"`.
    *   `rm -rf /tmp` - Removes the `/tmp` directory to clean up temporary files and reduce the image size.
    *   `apk del .tmp-build-deps` - Removes the temporary build dependencies installed earlier.
    *   `adduser --disabled-password --no-create-home app-user` - Adds a new user named `app-user` with a disabled password and without creating a home directory.
*   `ENV PATH="/py/bin:$PATH"` - This sets the `PATH` environment variable to include the virtual environment's binary directory (`/py/bin`), ensuring that the Python interpreter and other tools installed in the virtual environment are accessible.
*   `USER app-user` -  This specifies that the container should run as the `app-user` user, which improves security by preventing the application from running as the root user.