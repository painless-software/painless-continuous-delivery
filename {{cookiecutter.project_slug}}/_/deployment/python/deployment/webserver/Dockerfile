FROM nginx
RUN groupadd -r -g 999 application && \
    usermod -a -G application nginx
RUN rm /etc/nginx/conf.d/default.conf && \
    ln -s /opt/{{ cookiecutter.project_slug }}/deployment/webserver/nginx.conf /etc/nginx/conf.d/
CMD ["nginx", "-g", "daemon off;"]
