from flask import Flask, render_template, request, redirect, url_for, flash, g, send_from_directory, session
import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from datetime import datetime
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Set secret key from environment variable
app.secret_key = os.environ.get('SECRET_KEY')
if not app.secret_key:
    raise ValueError("No SECRET_KEY set in environment variables")

# Add these configurations after app initialization
app.config['ADMIN_USERNAME'] = os.environ.get('ADMIN_USERNAME', 'admin')
app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', 'admin123')

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads/resumes')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
            'position': 'Co-Founder',
            'description': 'Creative professional.',
            'image': 'images/team/CEO_founder.jpeg'
        },
        {
            'name': 'Danny Joseph Augustine',
            'position': 'Co-Founder',
            'description': 'Creative professional.',
            'image': 'images/team/Danny.jpeg'
        },
        {
            'name': 'Shalom Saji John',
            'position': 'Co-Founder',
            'description': 'Creative professional.',
            'image': 'images/team/Shalom.jpeg'
        },
        {
            'name': 'Cyril Luke Aneesh',
            'position': 'Co-Founder',
            'description': 'Creative professional.',
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


@app.route('/join-us', methods=['GET', 'POST'])
def join_us():
    job_listings = [
        {
            'title': 'Digital Marketing Specialist',
            'description': 'Looking for an experienced digital marketing professional.',
            'requirements': [
                '2+ years experience',
                'Social media expertise',
                'Content creation skills'
            ],
            'location': 'Remote / Kerala'
        },
        {
            'title': 'Video Editor',
            'description': 'Seeking creative video editor for digital content.',
            'requirements': [
                'Proficiency in Adobe Premiere Pro',
                'Portfolio of work',
                'Understanding of social media formats'
            ],
            'location': 'Remote / KErala'
        }
    ]
    if request.method == 'POST':
        try:
            # Get form data
            full_name = request.form.get('fullName')
            email = request.form.get('email')
            phone = request.form.get('phone')
            experience = request.form.get('experience')
            cover_letter = request.form.get('coverLetter')
            position = request.form.get('jobTitle', 'General Application')

            # Handle resume file upload
            if 'resume' not in request.files:
                flash('No resume file uploaded', 'error')
                return redirect(request.url)
            
            file = request.files['resume']
            if file.filename == '':
                flash('No selected file', 'error')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # Send email notification
                msg = MIMEText(f"""
                    New Job Application Received

                    Position: {position}
                    Name: {full_name}
                    Email: {email}
                    Phone: {phone}
                    Experience: {experience} years

                    Cover Letter:
                    {cover_letter}

                    Resume file saved as: {filename}
                """)
                
                msg['Subject'] = f'New Job Application - {position}'
                msg['From'] = os.environ.get('EMAIL_ID')
                msg['To'] = os.environ.get('EMAIL_ID')
                msg['Reply-To'] = email

                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(os.environ.get('EMAIL_ID'), os.environ.get('APP_PASSWORD'))
                    server.send_message(msg)

                flash('Your application has been submitted successfully!', 'success')
            else:
                flash('Invalid file type. Please upload a PDF, DOC, or DOCX file.', 'error')

        except Exception as e:
            print(f"Error processing application: {e}")
            flash('There was an error processing your application. Please try again.', 'error')

        return redirect(url_for('join_us'))
    return render_template('join_us.html',active_page='join_us', job_listings=job_listings)

@app.route('/test_env', methods=['GET'])
def test_env():
    email_id = os.environ.get('EMAIL_ID', 'Not Set')
    app_password = os.environ.get('APP_PASSWORD', 'Not Set')
    return f"EMAIL_ID: {email_id}, APP_PASSWORD: {app_password}"


def is_authorized():
    return session.get('is_admin', False)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authorized():
            flash('Please login as admin to access this page', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if (username == app.config['ADMIN_USERNAME'] and 
            password == app.config['ADMIN_PASSWORD']):
            session['is_admin'] = True
            flash('Successfully logged in as admin', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    flash('Successfully logged out', 'success')
    return redirect(url_for('home'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    # Get list of all resumes
    resume_dir = app.config['UPLOAD_FOLDER']
    resumes = []
    if os.path.exists(resume_dir):
        resumes = os.listdir(resume_dir)
    return render_template('admin_dashboard.html', resumes=resumes)

# Update the download_resume route with the decorator
@app.route('/uploads/resumes/<filename>')
@admin_required
def download_resume(filename):
    try:
        # Validate filename to prevent directory traversal
        if '..' in filename or filename.startswith('/'):
            flash('Invalid file path', 'error')
            return redirect(url_for('admin_dashboard'))
            
        if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            flash('File not found', 'error')
            return redirect(url_for('admin_dashboard'))
            
        return send_from_directory(
            app.config['UPLOAD_FOLDER'],
            filename,
            as_attachment=True
        )
    except Exception as e:
        print(f"Download error: {e}")  # For debugging
        flash('Error downloading file', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_resume/<filename>')
@admin_required
def delete_resume(filename):
    try:
        # Validate filename to prevent directory traversal
        if '..' in filename or filename.startswith('/'):
            flash('Invalid file path', 'error')
            return redirect(url_for('admin_dashboard'))
            
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            flash(f'Successfully deleted {filename}', 'success')
        else:
            flash('File not found', 'error')
    except Exception as e:
        print(f"Delete error: {e}")  # For debugging
        flash('Error deleting file', 'error')
    
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    app.run(debug=False)

