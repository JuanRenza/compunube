FROM centos
MAINTAINER Juan Renza
RUN yum install httpd -y
COPY voldocker/ /var/www/html/
RUN chmod -R 777 /var/www/html
EXPOSE 80
CMD ["/usr/sbin/httpd", "-D", "FOREGROUND"]