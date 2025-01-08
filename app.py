from flask import Flask, render_template, request, redirect, url_for, flash, g, send_from_directory, session
import smtplib
from flask_session import Session
import shutil
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from functools import wraps
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(app.root_path, 'flask_session')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
# Create session directory if it doesn't exist
if not os.path.exists(app.config['SESSION_FILE_DIR']):
    os.makedirs(app.config['SESSION_FILE_DIR'])

Session(app)

@app.before_request
def before_request():
    session.permanent = False  # Session will expire when browser closes
    g.now = datetime.now()

# Set secret key from environment variable
app.secret_key = os.environ.get('SECRET_KEY')
if not app.secret_key:
    raise ValueError("No SECRET_KEY set in environment variables")

app.config['ADMIN_USERNAME'] = os.environ.get('ADMIN_USERNAME', 'admin')
app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', 'admin123')

@app.route('/sitemap.xml')
def serve_sitemap():
    return send_from_directory('static', 'sitemap.xml')

@app.route('/robots.txt')
def serve_robots():
    return send_from_directory('static', 'robots.txt')

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
            'image': 'images/team/Alen_T_Koshy.jpeg'
        },
        {
            'name': 'Danie Joseph Augustine',
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
            'name': 'Cyril Luke Anish',
            'position': 'Co-Founder',
            'description': 'Creative professional.',
            'image': 'images/team/Cyril.jpeg'
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


#intialize AWS S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name=os.environ.get('AWS_REGION')
)
BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_to_s3(file, bucket_name, folder_name, acl="private"):
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        file_key = f"{folder_name}/{file.filename}"
        s3.upload_fileobj(
            file,
            bucket_name,
            file_key,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
        return f"https://{bucket_name}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{file_key}"
    except NoCredentialsError:
        print("AWS credentials not found.")
        return None
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return None

@app.route('/join-us', methods=['GET', 'POST'])
def join_us():
    job_listings = [
        {
            'title': 'Digital Marketing Specialist',
            'description': 'Looking for an experienced digital marketing professional.',
            'requirements': [
                'Experienced or freshers'
                'Social media expertise',
                'Content creation skills'
            ],
            'location': 'Remote / Kerala'
        },
        {
            'title': 'Video Editor',
            'description': 'Seeking creative video editor for digital content.',
            'requirements': [
                'Proficiency in Adobe Premiere Pro/After Effects',
                'Portfolio of work',
                'Understanding of social media formats'
            ],
            'location': 'Remote / Kerala'
        },
        {
            'title': 'Web Developer',
            'description': 'Looking for a web developer to join our team.',
            'requirements': [
                'Experience with HTML, CSS, JavaScript or other full stack technologies',
                'Portfolio of work',
                'Understanding of social media formats'
            ],
            'location': 'Remote / Kerala'
        },
        {
            'title': 'E-Sports Manager',
            'description': 'Seeking an E-Sports manager to join our team.',
            'requirements': [
                'Experience in E-Sports management',
                'Stable internet connection',
                'Understanding of game formats and tournaments'
            ],
            'location': 'Remote / Kerala'
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
            if 'resume' not in request.files or request.files['resume'].filename == '':
                flash('No resume file uploaded', 'error')
                return redirect(request.url)

            file = request.files['resume']

            if file and allowed_file(file.filename):
                # Upload file to S3
                file_url = upload_to_s3(file, os.getenv('AWS_BUCKET_NAME'), "resumes")
                if not file_url:
                    flash('Error uploading file. Please try again.', 'error')
                    return redirect(request.url)

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

                    Resume link: {file_url}
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

    return render_template('join_us.html', active_page='join_us', job_listings=job_listings)


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

@app.teardown_appcontext
def cleanup(error):
    if error:
        clear_session_files()


@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    try:
        # List files in the S3 bucket
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix="resumes/")
        resumes = [
            obj['Key'].split('/')[-1]  # Extract the filename from the S3 key
            for obj in response.get('Contents', [])
            if obj['Key'] != "resumes/"  # Exclude the folder itself
        ]
        return render_template('admin_dashboard.html', resumes=resumes)
    except ClientError as e:
        print(f"Error listing files: {e}")
        flash("Error loading files from S3.", "error")
        return redirect(url_for('home'))


def clear_session_files():
    session_dir = app.config['SESSION_FILE_DIR']
    if os.path.exists(session_dir):
        try:
            for file in os.listdir(session_dir):
                file_path = os.path.join(session_dir, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
        except Exception as e:
            print(f"Error clearing session files: {e}")

@app.route('/admin/logout')
def admin_logout():
    if session.get('is_admin'):
        session.clear()
        flash('Successfully logged out', 'success')
    return redirect(url_for('home'))

# Update the download_resume route with the decorator
@app.route('/uploads/resumes/<filename>')
@admin_required
def download_resume(filename):
    try:
        # Validate filename to prevent directory traversal
        if '..' in filename or filename.startswith('/'):
            flash('Invalid file path', 'error')
            return redirect(url_for('admin_dashboard'))
        
        # Generate a presigned URL for the file
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': f"resumes/{filename}"},
            ExpiresIn=3600  # Link valid for 1 hour
        )
        return redirect(presigned_url)
    except ClientError as e:
        print(f"Error downloading file: {e}")
        flash('Error downloading file from S3.', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_resume/<filename>')
@admin_required
def delete_resume(filename):
    try:
        # Validate filename to prevent directory traversal
        if '..' in filename or filename.startswith('/'):
            flash('Invalid file path', 'error')
            return redirect(url_for('admin_dashboard'))
        
        # Delete the file from S3
        s3.delete_object(Bucket=BUCKET_NAME, Key=f"resumes/{filename}")
        flash(f"Successfully deleted {filename} from S3.", "success")
    except ClientError as e:
        print(f"Error deleting file: {e}")
        flash('Error deleting file from S3.', 'error')
    
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=False)
