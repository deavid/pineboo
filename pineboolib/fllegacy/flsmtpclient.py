# -*- coding: utf-8 -*-




class FLSmtpClient(object):
    
    from_value_ = None
    reply_to_ = None
    to_ = None
    cc_ = None
    
    def __init__(self, parent):
        super(FLSmtpClient, self).__init__(parent)
    
    def setFrom(self, from_):
        self.from_value_ = from_
    
    def from_(self):
        return self.from_value_
    
    def setReplyTo(self, reply_to):
        self.reply_to_ = reply_to
    
    def replyTo(self):
        return self.replyTo()
    
    def setTo(self, to):
        self.to_ = to
    
    def to(self):
        return self.to_
    
    def setCC(self, cc):
        self.cc_ = cc
    
    def CC(self):
        return self.cc_
    
    
        
        
        
