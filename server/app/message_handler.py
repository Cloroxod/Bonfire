class MessageHandler(object):
    @classmethod
    def handle_post(cls, message):
        print 'Received message: name=%s, latitude=%s, longitude=%s' % (message.name, message.latitude, message.longitude)
        pass

    @classmethod
    def handle_update(cls, update_message):
        pass
