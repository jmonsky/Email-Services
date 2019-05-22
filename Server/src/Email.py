class Email(object):

    def __init__(self, id, message):
        self.id = id
        self.message = message
        self.subject = message["subject"]
        self.sender = message["from"]
        


    def searchAgainst(self, key):
        return self.subject == key

    
        
        
