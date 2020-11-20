from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from passlib.hash import sha256_crypt
from functools import wraps
from app.email_sender import send_emails
from validate_email import validate_email

web = Blueprint('web',__name__)

admin_email = '$5$rounds=535000$hlTQK9Z8RdX8L30t$qf80NcItqhmoKomntCss4FsGSgzYl/AxZTeZfweRQ87'
admin_password = '$5$rounds=535000$t0kBxknXP37MT7y6$AsV8m9GvhXD4QzqFAUzK1K3jR8U.BDxK8AASm3bJZt2'
secrete_admin_key = '$5$rounds=535000$0jmzks/cLR1FdRtX$qIBqKg/rjTrPuR5vIyp5zdt6BMXBBqBAfoUT/E8X4X5'

# (This login_required decorator checks if Admin is logged in ) => any route
# which require admin to login and (if Admin have choosed number of receivers before
# going to send_email route if admin tryed to do it) => only on send_email route.
def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'admin_email' in session:
            return func(*args, **kwargs)
        flash('You must login to contiunue.')
        return redirect(url_for('web.login'))
    return wrap


@web.route('/', methods=['GET'])
def home():
    return render_template('home_page.html')

@web.route('/admin/secret/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember_me = request.form.get('remember')
        if sha256_crypt.verify(email, admin_email) and sha256_crypt.verify(password, admin_password):
            if remember_me:
                session.permanent = True
            session['admin_email'] = email 
            session['admin_password'] = password
            flash('Admin logged in successful')
            return redirect(url_for('web.total_receiver'))
        flash('You email or password is incorrect')
        return render_template('login_page.html')
    return render_template('login_page.html')
@web.route('/admin/send/email', methods=['GET', 'POST'])
@login_required
def send_email():
    total_receivers = request.args.get('receivers', None)
    if total_receivers.isnumeric() and not total_receivers == '0':
        receivers = int(total_receivers)
        if request.method == 'POST':
            admin_key = request.form['admin_key']
            client_data = []
            email = request.form['client_email']
            subject = request.form['client_subject']
            body = request.form['client_body']
            footer = request.form['client_footer']
            client_data.extend((email, subject, body, footer))
            client_error_msg = None
            for item in client_data:
                if item == '':
                    client_error_msg = 'You must fiilout or fields'
            admin_key_error = None
            if not sha256_crypt.verify(admin_key, secrete_admin_key):
                admin_key_error = 'You admin key is incorrect'
            founded_receivers = []
            unfounded_receivers = []
            for i in range(receivers):
                i = i+1
                receiver_provided = request.form["receiver_" + str(i)] is not ''
                if receiver_provided:
                    is_valid = validate_email(request.form["receiver_" + str(i)],verify=True) is not None
                    if is_valid:
                        founded_receivers.append(request.form["receiver_" + str(i)])
                    else:
                        unfounded_receivers.append(request.form["receiver_" + str(i)])
            print(unfounded_receivers)
            if founded_receivers:
                admin_email = session.get('admin_email', None)
                admin_password = session.get('admin_password', None)
                send_emails(
                    Admin_email=admin_email,Admin_password=admin_password,Sender=email,Receiver=founded_receivers,
                    Subject=subject,Body=body,Footer=footer)
            return render_template(
                'email_page.html',receivers=receivers,client_error_msg=client_error_msg,
                admin_key_error=admin_key_error,founded_receivers=founded_receivers,
                unfounded_receivers=unfounded_receivers)
        return render_template('email_page.html',receivers=receivers)
    flash('You must choose number of receiver to send email')
    return redirect(url_for('web.total_receiver'))

@web.route('/admin/receiver/number', methods=['GET','POST'])
@login_required
def total_receiver():
    if request.method == 'POST':
        total_receivers = request.form['inputs_number']
        if total_receivers.isnumeric() and not total_receivers == '0':
            receivers = int(total_receivers)
            return redirect(url_for('web.send_email', receivers=receivers))
        error_msg = 'You must fillout this field (with numbers only , greater than 0)'
        return render_template('total_receiver.html', error=error_msg)
    return render_template('total_receiver.html')

@web.route('/admin/secret/logout', methods=['GET'])
def logout():
    session.pop('admin_email', None)
    session.pop('admin_password', None)
    flash('Admin logged out successful')
    return redirect(url_for('web.login'))


