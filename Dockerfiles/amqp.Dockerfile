FROM rabbitmq:3.7-management

COPY conf/rabbitmq.conf /etc/rabbitmq

RUN cat /etc/rabbitmq/rabbitmq.conf