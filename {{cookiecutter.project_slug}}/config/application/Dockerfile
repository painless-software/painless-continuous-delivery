FROM python:3.5
WORKDIR /opt/{{ cookiecutter.project_slug }}
COPY . .
RUN groupadd -r application && \
    useradd -r -g application application && \
    chown -R application:application .
RUN pip install -r requirements.txt && \
    pip install uwsgi
CMD uwsgi --master --ini config/application/uwsgi.ini
