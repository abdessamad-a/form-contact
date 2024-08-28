from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

print("EMAIL_DEFAULT_SENDER:", os.getenv('EMAIL_DEFAULT_SENDER'))
print("EMAIL_PASSWORD:", os.getenv('EMAIL_PASSWORD'))

app = Flask(__name__)

# Clé secrète pour les sessions
app.secret_key = os.getenv('SECRET_KEY', 'your secret key')

# Configuration de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_DEFAULT_SENDER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_DEFAULT_SENDER')

mail = Mail(app)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/les_menus')
def les_menus():
    return render_template('les_menus.html')

@app.route('/reservations')
def reservations():
    return render_template('reservations.html')

@app.route('/qui_sommes_nous')
def qui_sommes_nous():
    return render_template('qui_sommes_nous.html')

@app.route('/mentions_légales')
def mentions_légales():
    return render_template('mentions_légales.html')


@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        nom = request.form['name']
        prenom = request.form['surname']
        email = request.form['email']
        objet = request.form['object']
        message = request.form['message']
        

        print(f"Nom: {nom}, Prénom: {prenom}, Email: {email}, Objet: {objet}, Message: {message}")

        msg = Message(
            subject=f"Message de {nom} {prenom}: {objet}",
            sender=email,
            recipients=['your email'],  # L'adresse email où vous voulez recevoir les messages
            body=f"Nom: {nom}\nPrénom: {prenom}\nEmail: {email}\nObjet: {objet}\n\nMessage:\n{message}"
        )

        try:
            mail.send(msg)
            flash('Votre message a été envoyé avec succès !', 'success')
        except Exception as e:
            flash(f'Une erreur s\'est produite lors de l\'envoi du message : {str(e)}', 'danger')

        return redirect(url_for('contact'))

if __name__ == '__main__':
    app.run(debug=True)