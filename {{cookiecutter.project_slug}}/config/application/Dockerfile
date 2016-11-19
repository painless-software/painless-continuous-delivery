FROM python:3.5
WORKDIR /opt/{{ cookiecutter.project_slug }}
COPY requirements.txt requirements.txt
RUN pip install uwsgi -r requirements.txt
COPY . .
RUN groupadd -r -g 999 application && \
    useradd -r -g application application && \
    chown -R application:application .
RUN mkdir /run/{{ cookiecutter.project_slug }} && \
    chown application:application /run/{{ cookiecutter.project_slug }}
VOLUME /opt/{{ cookiecutter.project_slug }} \
       /run/{{ cookiecutter.project_slug }}
CMD uwsgi --master --ini config/application/uwsgi.ini
