import smtplib
from email.message import EmailMessage

def send_emails(Admin_email, Admin_password, Sender, Receiver, Subject, Body, Footer):
    admin_email = Admin_email
    admin_password = Admin_password
    msg = EmailMessage()
    msg['From'] = Sender
    msg['To'] = Receiver
    msg['Subject'] = Subject
    msg.add_alternative(f"""
    <html>
        <body>
            <div class="container" style="background-color: rgb(22, 16, 16); color: white; text-align: center;
            padding:50px 10px";>
            <h2 class="company_header">This message was delivered by ( 
            <a href="" style="color: rgb(226, 75, 108);">Easy way Company</a>
             )</h2>
            <div class="client_form" style="background-color: rgb(4, 99, 102); color:rgb(34, 235, 241); width: 80%;
            margin: auto; text-align: center; border: 10px groove black; border-radius: 25px;">
                <div style="padding: 10px 50px;">
                    {Body}
                </div>
                <footer style="padding:10px 50px;">
                    {Footer}
                </footer>
            </div>
            <div class="company_footer">
                <p><a href="#">contact <span style="color: rgb(16, 199, 168);">us</span></a></p>
                <p>Copyright © 2020 & all rights reserved, made by iyera david.</p>
            </div>
            </div>
        </body>
    </html>
    """, subtype='html')
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.login(admin_email, admin_password)
    smtp.send_message(msg)
