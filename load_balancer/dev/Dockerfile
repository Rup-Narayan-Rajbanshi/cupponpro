

FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY .certi /home/.certi/
# COPY /etc/letsencrypt /etc/
COPY default.conf /etc/nginx/conf.d/nginx.conf
# RUN rm /etc/nginx/nginx.conf
# COPY nginx.conf /etc/nginx/nginx.conf
