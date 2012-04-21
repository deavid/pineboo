# encoding: UTF-8
from PyQt4 import QtCore,QtGui
import re

def connect(sender, signal, receiver, slot):
    print "Connect::", sender, signal, receiver, slot
    m = re.search("^(\w+).(\w+)(\(.*\))?", slot)
    if m:
        remote_obj = getattr(receiver, m.group(1))
        if remote_obj is None: raise AttribueError, "Object %s not found on %s" % (remote_obj, str(receiver))
        remote_fn = getattr(remote_obj, m.group(2))
        if remote_fn is None: raise AttribueError, "Object %s not found on %s" % (remote_fn, remote_obj)
        sender.connect(sender, QtCore.SIGNAL(signal), remote_fn)
    else:
        sender.connect(sender, QtCore.SIGNAL(signal), receiver, QtCore.SLOT(slot))
    return True
