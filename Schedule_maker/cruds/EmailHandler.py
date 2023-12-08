import jwt

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from starlette.exceptions import HTTPException

from Schedule_maker.models import User
from Schedule_maker.config.settings import Settings, settings


class EmailHandler:
    def __init__(self, _settings: Settings):
        self.settings = _settings

    async def send_verification_email(self, email: str, user: User) -> None:
        token_data = {
            "id": user.id,
            "username": user.username
        }

        token = jwt.encode(token_data, self.settings.SECRET_KEY)

        template = f"""
            <!DOCTYPE html>
            <html>
            <head>
            </head>
            <body>
                <div style=" display: flex; align-items: center; justify-content: center; flex-direction: column;">
                    <h3> Account Verification </h3>
                    <br>
                    <p>Thanks for choosing Schedule-Maker, please 
                    click on the link below to verify your account</p> 

                    <a style="margin-top:1rem; padding: 1rem; border-radius: 0.5rem; font-size: 1rem;
                     text-decoration: none; background: #0275d8; color: white;"
                     href="http://localhost:8000/verification/?token={token}">
                        Verify your email
                    <a>

                    <p style="margin-top:1rem;">If you did not register for Schedule-Maker, 
                    please kindly ignore this email and nothing will happen. Thanks<p>
                </div>
            </body>
            </html>
        """

        # Construct the email
        msg = MIMEMultipart()
        msg["From"] = settings.MAIL_USERNAME
        msg["To"] = email
        msg["Subject"] = "Email Verification"
        msg.attach(MIMEText(template, "html"))

        try:
            # Connect to the SMTP server and send the email
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
            server.sendmail(settings.MAIL_USERNAME, email, msg.as_string())
            server.quit()
        except Exception:
            raise HTTPException(status_code=500, detail=f"Failed to send email")


email_handler = EmailHandler(settings)
