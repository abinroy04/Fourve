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
    #now = datetime.now()
    #return render_template('home.html', active_page='home', now=now)
    return render_template('home.html')


    
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

@app.route('/services')
def services():
    services_list = {
        'live_streaming': {
            'title': 'Live Streaming',
            'description': 'Professional streaming services for events across India.',
            'features': ['High-quality streaming', 'Multiple platform support', 'Real-time engagement']
        },
        'media_production': {
            'title': 'Media Production',
            'description': 'Complete media production services for all your needs.',
            'features': ['Video production', 'Photography', 'Post-production']
        },
        'digital_marketing': {
            'title': 'Digital Marketing',
            'description': 'Comprehensive digital marketing solutions.',
            'features': ['Social media management', 'Content creation', 'SEO optimization']
        },
        'event_management': {
            'title': 'Event Management',
            'description': 'Full-service event planning and execution.',
            'features': ['Wedding planning', 'Corporate events', 'Social gatherings']
        }
    }
    return render_template('services.html', active_page='services', services=services_list)

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

@app.route('/join-us')
def join_us():
    job_listings = [
        {
            'title': 'Digital Marketing Specialist',
            'description': 'Looking for an experienced digital marketing professional.',
            'requirements': ['3+ years experience', 'Social media expertise', 'Content creation skills'],
            'location': 'Mumbai, India'
        }
    ]
    return render_template('join_us.html', active_page='join_us', jobs=job_listings)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        try:
            # Email configuration (replace with your email settings)
            sender_email = "your-email@example.com"
            receiver_email = "fourve.dimension@gmail.com"
            password = "your-email-password"

            msg = MIMEText(f"Name: {name}\nEmail: {email}\nMessage: {message}")
            msg['Subject'] = 'New Contact Form Submission'
            msg['From'] = sender_email
            msg['To'] = receiver_email

            # Send email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.send_message(msg)

            flash('Thank you for your message! We will get back to you soon.', 'success')
        except Exception as e:
            flash('Sorry, there was an error sending your message. Please try again later.', 'error')
            print(f"Error sending email: {e}")

        return redirect(url_for('contact'))
    
    return render_template('contact.html', active_page='contact')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host = '0.0.0.0',port=port)
