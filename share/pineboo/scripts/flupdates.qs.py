# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING
from pineboolib.qsa import qsa

# /** @file */


# /** @class_declaration interna */
class interna(object):
    ctx = qsa.Object()

    def __init__(self, context=None):
        self.ctx = context

    def main(self):
        self.ctx.interna_main()


# /** @class_declaration oficial */
class oficial(interna):
    def __init__(self, context=None):
        super(oficial, self).__init__(context)


# /** @class_declaration head */
class head(oficial):
    def __init__(self, context=None):
        super(head, self).__init__(context)


# /** @class_declaration ifaceCtx */
class ifaceCtx(head):
    def __init__(self, context=None):
        super(ifaceCtx, self).__init__(context)


# /** @class_declaration FormInternalObj */
class FormInternalObj(qsa.FormDBWidget):
    iface: ifaceCtx

    # /** @class_definition FormInternalObj */
    def _class_init(self):
        self.iface = ifaceCtx(self)

    # /** @class_definition interna */
    def interna_main(self):
        qsa.sys.updateAbanQ()


if TYPE_CHECKING:
    form: FormInternalObj = FormInternalObj()
    iface = form.iface
else:
    form = None
