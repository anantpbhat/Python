"""Class to send secure Email with attachment"""

import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from myclass.decrypt_it import Decrypt

class SendEmail():
  """Class to send Emails with attachments using SMTP authentication"""
  def smail(self, rcvr, subj, msg, enc, key, atchfls=None):
    """This function will take all email args and do the job"""
    port = 587
    smtp_server = "smtp.abc.net"
    sndr_email = "sndr@abc.net"
    smtp_login = "smtp_user"
    dcrt = Decrypt
    em_pswd = dcrt.do_decrypt(enc, key)
    em_pswd = em_pswd.rstrip()
    message = MIMEMultipart()
    message["From"] = sndr_email
    message["To"] = rcvr
    message["Subject"] = subj
    message.attach(MIMEText(msg, "plain"))
    rcvr_eml_list = rcvr.split(',')
    if atchfls:
      afilelst = atchfls.aplit(",")
      for atchfl in afilelst:
        with open(atchfl, "rb") as afile:
          apart = MIMEBase("application, "octet-stream")
          apart.set_payload(afile.read())
        encoders.encode_base64(apart)
        apart.add_header("Content-Disposition", f"attachment; filename={atchfl}",)
        message.attach(apart)
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as emsrvr:
          emsrvr.starttls(context=context)
          emsrvr.login(smtp_login, em_pswd)
          emsrvr.sendmail(sndr_email, rcvr_eml_lst, message.as_string())
          print("Email Sent...")
        return
