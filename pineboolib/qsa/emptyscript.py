# -*- coding: utf-8 -*-
from pineboolib.qt3_widgets.formdbwidget import FormDBWidget


class interna(object):
    ctx: FormDBWidget

    def __init__(self, context: FormDBWidget) -> None:
        self.ctx = context

    def init(self) -> None:
        self.ctx.interna_init()


class oficial(interna):
    def __init__(self, context: FormDBWidget):
        super(oficial, self).__init__(context)


class head(oficial):
    def __init__(self, context: FormDBWidget):
        super(head, self).__init__(context)


class ifaceCtx(head):
    def __init__(self, context: FormDBWidget):
        super(ifaceCtx, self).__init__(context)


class FormInternalObj(FormDBWidget):
    def _class_init(self) -> None:
        self.iface = ifaceCtx(self)

    def interna_init(self) -> None:
        pass


form = None
