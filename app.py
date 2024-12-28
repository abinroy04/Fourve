from flask import Flask, render_template, request, redirect, url_for, flash, g
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flashing messages

@app.before_request
def add_now():
    from datetime import datetime
    g.now = datetime.now()
    
@app.route('/')
def home():
    now = datetime.now()
    return render_template('home.html', active_page='home', now=now)

@app.route('/team')
def team():
    team_members = [
        {
            'name': 'Alen T Koshy',
            'position': 'CEO & Co-Founder',
            'description': 'Coconut',
            'image': 'images/team/CEO_founder.jpeg'
        },
        {
            'name': 'Danny Joseph Augustine',
            'position': 'CFO & Co-Founder',
            'description': 'Award-winning creative professional.',
            'image': 'images/team/Danny.jpeg'
        },
        {
            'name': 'Shalom Saji John',
            'position': 'CMO & Co-Founder',
            'description': 'Award-winning creative professional.',
            'image': 'images/team/Shalom.jpeg'
        },
        {
            'name': 'Cyril Luke Aneesh',
            'position': 'CTO & Co-Founder',
            'description': 'Award-winning creative professional.',
            'image': 'images/team/Cyril.jpg'
        }
    ]
    return render_template('team.html', active_page='team', team_members=team_members)

@app.route('/broadcasting')
def broadcasting():
    return render_template('broadcasting.html', active_page='broadcasting')

@app.route('/mediapro')
def mediapro():
    return render_template('mediapro.html', active_page='mediapro')

@app.route('/digimark')
def digimark():
    return render_template('digimark.html', active_page='digimark')

@app.route('/eventmgmt')
def eventmgmt():
    return render_template('eventmgmt.html', active_page='eventmgmt')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        sender_email = request.form.get('email')
        message = request.form.get('message')

        # Debugging print statements
        print(f"Received form data - Name: {name}, Email: {sender_email}, Message: {message}")

        if not name or not sender_email or not message:
            flash("All fields are required!", "error")
            return redirect(url_for('contact'))

        try:
            # Email configuration
            receiver_email = os.environ.get('EMAIL_ID')
            sender_account_email = os.environ.get('EMAIL_ID')
            sender_account_password = os.environ.get('APP_PASSWORD')

            msg = MIMEText(f"Name: {name}\nEmail: {sender_email}\nMessage: {message}")
            msg['Subject'] = 'New Contact Form Submission'
            msg['From'] = sender_account_email
            msg['To'] = receiver_email
            msg['Reply-To'] = sender_email

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_account_email, sender_account_password)
                server.send_message(msg)

            flash('Thank you for your message! We will get back to you soon.', 'success')
        except Exception as e:
            flash('We are unable to recieve your message at the moment. Try contacting us via mobile.', 'error')
            print(f"Error sending email: {e}")
            print(f"Email: {sender_account_email}, Password: {sender_account_password}")


        return redirect(url_for('contact'))

    return render_template('contact.html', active_page='contact')


@app.route('/join-us')
def join_us():
    job_listings = [
        {
            'title': 'Digital Marketing Specialist',
            'description': 'Looking for an experienced digital marketing professional.',
            'requirements': ['3+ years experience', 'Social media expertise', 'Content creation skills'],
            'location': 'Mumbai, India'
        },
        {
            'title': 'Video Editor',
            'description': 'Seeking talented video editor for our media production team.',
            'requirements': ['Adobe Premiere Pro', 'After Effects', 'Creative storytelling'],
            'location': 'Remote'
        },
        {
            'title': 'Event Coordinator',
            'description': 'Join our event management team to plan and execute memorable events.',
            'requirements': ['Event planning experience', 'Strong organizational skills', 'Excellent communication'],
            'location': 'Bangalore'
        }
        # Add more job listings as needed
    ]
    return render_template('join_us.html', active_page='join_us', jobs=job_listings)

if __name__ == '__main__':
    app.run(debug=False)

