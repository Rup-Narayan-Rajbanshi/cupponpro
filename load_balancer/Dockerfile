

FROM nginx
#RUN rm /etc/nginx/conf.d/default.conf
COPY .certi /home/.certi/
RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/nginx.conf

