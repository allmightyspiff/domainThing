import pika
import configparser 
import logging as logger


class pikaQueue():

    def __init__(self, config):

        credentials = pika.PlainCredentials(
                    config.get('rabbitmq','user'), 
                    config.get('rabbitmq','password')
                )
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                    config.get('rabbitmq','host'), 
                    config.getint('rabbitmq','port'), 
                    config.get('rabbitmq','vhost'), 
                    credentials, 
                    socket_timeout=15,
                    ssl=True)
                )
        self.channel = connection.channel()
        self.channel.queue_declare(queue='domain-queue')

    def sendMessage(self, message):
        logger.info("Sending message")
        self.channel.basic_publish(exchange='', routing_key='domain-queue', body=message)

    def close(self):
        self.connection.close()
