# -*- coding: utf-8 -*-
from PyQt5 import QtCore, Qt  # type: ignore
from os.path import basename
from pineboolib import logging

import smtplib
import socket

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage

from typing import List

logger = logging.getLogger(__name__)


class State(object):
    Init = 0
    Mail = 1
    Rcpt = 2
    Data = 3
    Body = 4
    Quit = 5
    Close = 6
    SmtpError = 7
    Connecting = 8
    Connected = 9
    MxDnsError = 10
    SendOk = 11
    SockedError = 12
    Composing = 13
    Attach = 14
    AttachError = 15
    ServerError = 16
    ClientError = 17
    StartTTLS = 18
    WaitingForSTARTTLS = 19
    SendAuthPlain = 20
    SendAuthLogin = 21
    WaitingForAuthPlain = 22
    WaitingForAuthLogin = 23
    WaitingForUser = 24
    WaitingForPass = 25


class AuthMethod(object):
    NoAuth = 0
    AuthPlain = 1
    AuthLogin = 2


class ConnectionType(object):
    TcpConnection = 0
    SslConnection = 1
    TlsConnection = 2


class FLSmtpClient(QtCore.QObject):

    from_value_ = None
    reply_to_ = None
    to_ = None
    cc_ = None
    bcc_ = None
    organization_ = None
    priority_ = None
    subject_ = None
    body_ = None

    attachments_: List[str] = []  # List with file paths

    mail_server_ = None
    mime_type_ = None
    port_ = None

    text_parts_: List[str] = []
    map_attach_cid_: dict = {}  # FIXME: unused

    status_msg_ = None
    state_code_ = None

    user_ = None
    password_ = None
    connection_type_ = None
    auth_method_ = None

    status = QtCore.pyqtSignal(str)
    sendStarted = QtCore.pyqtSignal()
    sendEnded = QtCore.pyqtSignal()
    sendTotalSteps = QtCore.pyqtSignal(int)
    sendStepNumber = QtCore.pyqtSignal(int)
    statusChanged = QtCore.pyqtSignal(str, int)

    def __init__(self, parent=None):
        super(FLSmtpClient, self).__init__(parent)
        self.state_code_ = State.Init
        self.priority_ = 0
        self.port_ = 25
        self.connection_type_ = ConnectionType.TcpConnection
        self.auth_method_ = AuthMethod.NoAuth

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

    def setBCC(self, cc):
        self.bcc_ = cc

    def BCC(self):
        return self.bcc_

    def setOrganization(self, org):
        self.organization_ = org

    def organization(self):
        return self.organization_

    def setPriority(self, prio):
        self.priority_ = prio

    def priority(self):
        return self.priority_

    def setSubject(self, subject):
        self.subject_ = subject

    def subject(self):
        return self.subject_

    def setBody(self, body):
        self.body_ = body

    def body(self):
        return self.body_

    def addAttachment(self, attach, cid=None):
        if QtCore.QFile.exists(attach) and QtCore.QFileInfo(attach).isReadable():
            if attach and attach not in self.attachments_:
                self.attachments_.append(attach)
                if cid:
                    self.map_attach_cid_[attach] = cid
        else:
            err_msg_ = self.tr("El fichero %s no existe o no se puede leer\n\n" % attach)
            logger.warning(err_msg_)
            self.changeStatus(err_msg_, State.AttachError)

    def addTextPart(self, text: str, mime_type="text/plain"):
        if text:
            self.text_parts_.append(text)
            self.text_parts_.append(mime_type)

    def setMailServer(self, mail_server):
        self.mail_server_ = mail_server

    def mailServer(self):
        return self.mail_server_

    def setMimeType(self, mine_type):
        self.mime_type_ = mine_type

    def mimeType(self):
        return self.mime_type_

    def setPort(self, port):
        self.port_ = port

    def port(self):
        return self.port_

    def lastStatusMsg(self):
        return self.status_msg_

    def lastStateCode(self):
        return self.state_code_

    def setUser(self, user):
        self.user_ = user

    def user(self):
        return self.user_

    def setPassword(self, password):
        self.password_ = password

    def password(self):
        return self.password_

    def setConnectionType(self, c):
        self.connection_type_ = c

    def connectionType(self):
        return self.connection_type_

    def setAuthMethod(self, method):
        self.auth_method_ = method

    def authMethod(self):
        return self.auth_method_

    def startSend(self):
        from pineboolib.core.utils.utils_base import pixmap_fromMimeSource
        from pineboolib.core.settings import settings
        from pineboolib.application import project

        self.sendStarted.emit()
        self.sendTotalSteps.emit(len(self.attachments_) + 3)

        step = 0

        self.changeStatus(self.tr("Componiendo mensaje"), State.Composing)

        outer = MIMEMultipart()
        outer["From"] = self.from_value_
        outer["To"] = self.to_
        if self.cc_:
            outer["Cc"] = self.cc_
        if self.bcc_:
            outer["Bcc"] = self.bcc_
        if self.organization_:
            outer["Organization"] = self.organization_
        if self.priority_ > 0:
            outer["Priority"] = self.priority_
        outer["Subject"] = self.subject_
        outer.preamble = "You will not see this in a MIME-aware mail reader.\n"
        outer.add_header("Content-Type", self.mime_type_)

        outer.attach(MIMEText(self.body_, self.mime_type_.split("/")[1], "utf-8"))

        step += 1
        self.sendStepNumber.emit(step)
        # Adjuntar logo
        if settings.value("email/sendMailLogo", True):
            logo = settings.value("email/mailLogo", "%s/logo_mail.png" % project.tmpdir)
            if not QtCore.QFile.exists(logo):
                logo = "%s/logo.png" % project.tmpdir
                Qt.QPixmap(pixmap_fromMimeSource("pineboo-logo.png")).save(logo, "PNG")

            fp = open(logo, "rb")
            logo_part = MIMEImage(fp.read())
            fp.close()

            logo_part.add_header("Content-ID", "<image>")
            outer.attach(logo_part)

        # Ficheros Adjuntos
        for att in self.attachments_:
            try:
                with open(att, "rb") as fil:
                    part = MIMEApplication(fil.read(), Name=basename(att))
                    part["Content-Disposition"] = 'attachment; filename="%s"' % basename(att)
                    outer.attach(part)
            except IOError:
                logger.warning("Error al adjuntar el fichero %s." % att)
                return False

        # Envio mail
        composed = outer.as_string()

        step += 1
        self.sendStepNumber.emit(step)

        try:
            s = smtplib.SMTP(self.mail_server_, self.port_)
            if self.connection_type_ == ConnectionType.TlsConnection:
                s.starttls()

            if self.user_ and self.password_:
                status_msg = "login."
                if self.auth_method_ == State.SendAuthLogin:
                    self.changeStatus(status_msg, State.SendAuthLogin)
                elif self.auth_method_ == State.SendAuthPlain:
                    self.changeStatus(status_msg, State.SendAuthPlain)

                s.login(self.user_, self.password_)

                self.changeStatus(
                    status_msg, State.WaitingForAuthLogin if self.auth_method_ == State.SendAuthLogin else State.WaitingForAuthPlain
                )

            s.sendmail(self.from_value_, self.to_, composed)
            self.changeStatus("Correo enviado", State.SendOk)
            s.quit()
            return True

        except smtplib.SMTPHeloError:
            status_msg = "El servidor no ha respondido correctamente al saludo."
            self.changeStatus(status_msg, State.ClientError)
            return False
        # except smtplib.SMTPNotSupportedError:
        #     status_msg = "El tipo de autenticación no está soportada por el servidor."
        #     self.changeStatus(status_msg, State.ClientError)
        #     return False
        except smtplib.SMTPConnectError:
            status_msg = "No se puede conectar al servidor SMTP."
            self.changeStatus(status_msg, State.ServerError)
            return False
        except smtplib.SMTPAuthenticationError:
            status_msg = "Error de autenticación SMTP."
            self.changeStatus(status_msg, State.ClientError)
            return False
        except smtplib.SMTPSenderRefused:
            status_msg = "Dirección de remitente rechazada."
            self.changeStatus(status_msg, State.ClientError)
            return False
        except smtplib.SMTPRecipientsRefused:
            status_msg = "Todas las direcciones de destinatarios se rechazaron."
            self.changeStatus(status_msg, State.ClientError)
            return False
        except smtplib.SMTPServerDisconnected:
            status_msg = "El servidor se desconecta inesperadamente."
            self.changeStatus(status_msg, State.ServerError)
            return False
        except smtplib.SMTPException:
            status_msg = "Error desconocido"
            self.changeStatus(status_msg, State.ClientError)
            return False
        except socket.gaierror:
            status_msg = "Servidor SMTP no encontrado.Verifique el nombre de host de su servidor SMTP."
            self.changeStatus(status_msg, State.SmtpError)
            return False
        except Exception as e:
            status_msg = "Error sending mail %s." % e
            return False

    def changeStatus(self, status_msg, state_code):
        self.status_msg_ = status_msg
        self.state_code_ = state_code
        self.statusChanged.emit(self.status_msg_, self.state_code_)
        self.status.emit(self.status_msg_)
