FROM nginx
RUN rm /etc/nginx/conf.d/default.conf && \
    ln -s /opt/{{ cookiecutter.project_slug }}/config/webserver/nginx.conf /etc/nginx/conf.d/
CMD ["nginx", "-g", "daemon off;"]
