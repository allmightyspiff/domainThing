import threading
import mqlight
import configparser 
import os
import logging as logger

class mqlightQueue():

    def __init__(self, config, clientName):

        self.options = {
            'qos': mqlight.QOS_AT_LEAST_ONCE,
            'ttl': 999999
        }
        self.ready = False
        user = "N6KqE6X3MFvV"
        password = "/B/G%d=j8XT8"
        security_options = {}
        security_options['property_user'] = config.get('rabbitmq','user').__str__()
        security_options['property_password'] = config.get('rabbitmq','password').__str__()
        mqService = config.get('rabbitmq','host').__str__()
        logger.info("HOST: %s - %s -%s" % (mqService,security_options['property_user'], security_options['property_password']))
        mqClient = clientName
        self.client = mqlight.Client(
            service=mqService,
            security_options=security_options,
            client_id=mqClient,
            on_state_changed=self.stateChanged,
            on_started=self.started

        )
        self.lock = threading.RLock()
        self.thread = threading.Event()

    def __exit__(self):
        logger.info("Shutting mq down")
        self.close()

    def started(self, client):
        logger.info("Ready to go!")
        self.ready=True

    def subscribed(self, err, pattern, share):
        logger.info("Subscried to %s - %s" % (pattern,share))


    def sendMessage(self, message, topic):
        with self.lock:
            self.thread.clear()
            logger.info("%s - %s" % (topic,message[0:45]))

            if self.client.send(topic=topic,data=message,options=self.options,on_sent=self.on_sent):
                return True
            else:
                self.thread.wait()

    def close(self):
        with self.lock:
            self.thread.clear
            logger.info("Closing the connection")
            self.client.stop()
        # self.thread.exit()

    def stateChanged(self, client, state, message='EMPTY'):
        logger.info("State changed to %s" % state)

        if state == mqlight.ERROR:
            logger.info("Hit an error %s - %s" % (message,state))
            self.ready = False
            self.close()

        elif state == mqlight.DRAIN:
            logger.info("DRAIN")
            self.thread.set()
            


    def on_sent(self, error, topic, data, options):
        if error:
            logger.info("ERROR: %s" % error)
            return False
        else:
            logger.info("Sent to %s successfully" % topic)
            return True


    def subscribe(self,topic, callback):
        myOptions = {}
        myOptions['auto_confirm'] = False
        myOptions['credit'] = 1024
        myOptions['qos'] = mqlight.QOS_AT_LEAST_ONCE
        logger.info("BINDING: ")

        logger.info("Subscring to %s" % topic)

        self.client.subscribe(
            topic_pattern = topic,
            share = None,
            options = myOptions,
            on_message=callback,
            on_subscribed=self.subscribed
        )
        logger.info("Subscribed to %s" % topic)

    def unsubscribe(self,topic):
        self.client.unsubscribe(
            topic_pattern = topic,
            share = 'domainThing'
            )
        logger.info("STOP")


