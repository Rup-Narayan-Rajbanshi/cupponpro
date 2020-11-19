

FROM nginx
#RUN rm /etc/nginx/conf.d/default.conf
COPY /etc/letsencrypt/archive/api.cupponpro.com /home/api.cupponpro.com
RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/nginx.conf
