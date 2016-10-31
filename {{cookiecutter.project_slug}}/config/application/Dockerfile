FROM python:3.5
WORKDIR /opt/{{ cookiecutter.project_slug }}
COPY . .
RUN pip install -r requirements.txt && \
    pip install uwsgi
RUN groupadd -r -g 999 application && \
    useradd -r -g application application && \
    chown -R application:application .
RUN mkdir /run/{{ cookiecutter.project_slug }} && \
    mkdir /var/log/{{ cookiecutter.project_slug }} && \
    chown application:application /run/{{ cookiecutter.project_slug }} && \
    chown application:application /var/log/{{ cookiecutter.project_slug }}
VOLUME /opt/{{ cookiecutter.project_slug }} \
       /run/{{ cookiecutter.project_slug }} \
       /var/log/{{ cookiecutter.project_slug }}
CMD uwsgi --master --ini config/application/uwsgi.ini
