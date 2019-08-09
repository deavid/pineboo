# -*- coding: utf-8 -*-
"""emptyscript module."""

from pineboolib.qt3_widgets import formdbwidget


class interna(object):
    """Interna class."""

    ctx: formdbwidget.FormDBWidget

    def __init__(self, context: formdbwidget.FormDBWidget) -> None:
        """Inicialize."""

        self.ctx = context

    def init(self) -> None:
        """Run optional inicialize script."""

        self.ctx.interna_init()


class oficial(interna):
    """Oficial class."""

    def __init__(self, context: formdbwidget.FormDBWidget) -> None:
        """Inicialize."""

        super().__init__(context)


class head(oficial):
    """Head class."""

    def __init__(self, context: formdbwidget.FormDBWidget) -> None:
        """Inicialize."""

        super().__init__(context)


class ifaceCtx(head):
    """IfaceCtx class."""

    def __init__(self, context: formdbwidget.FormDBWidget) -> None:
        """Inicialize."""

        super().__init__(context)


class FormInternalObj(formdbwidget.FormDBWidget):
    """FormInternalObj class."""

    def _class_init(self) -> None:
        """Inicialize ifaceCtx."""

        self.iface = ifaceCtx(self)

    def interna_init(self) -> None:
        """Run optional inicialize script."""
        pass


form = None
