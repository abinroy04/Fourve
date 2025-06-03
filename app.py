from flask import Flask, render_template, request, redirect, url_for, flash, g, send_from_directory, session
import smtplib
from flask_session import Session
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from functools import wraps
from supabase import create_client, Client

app = Flask(__name__)

load_dotenv()

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(app.root_path, 'flask_session')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
if not os.path.exists(app.config['SESSION_FILE_DIR']):
    os.makedirs(app.config['SESSION_FILE_DIR'])

Session(app)

@app.before_request
def before_request():
    g.now = datetime.now()

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

        print(f"Received form data - Name: {name}, Email: {sender_email}, Message: {message}")

        if not name or not sender_email or not message:
            flash("All fields are required!", "error")
            return redirect(url_for('contact'))

        try:
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


supabase: Client = create_client(
    os.environ.get('SUPABASE_URL'),
    os.environ.get('SUPABASE_KEY')
)
BUCKET_NAME = 'resumes'

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_to_supabase(file, bucket_name, folder_name):
    try:
        # Create a unique filename to avoid collisions
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        secure_name = secure_filename(file.filename)
        file_key = f"{folder_name}/{timestamp}_{secure_name}"
        
        # Upload file to Supabase Storage
        file_data = file.read()
        response = supabase.storage.from_(bucket_name).upload(file_key, file_data, {"content-type": file.content_type})
        
        if response.get("error"):
            print(f"Error uploading to Supabase: {response.get('error')}")
            return None
        
        # Get the public URL for the file
        file_url = supabase.storage.from_(bucket_name).get_public_url(file_key)
        return {"url": file_url, "key": file_key}
    except Exception as e:
        print(f"Error uploading to Supabase: {e}")
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
            full_name = request.form.get('fullName')
            email = request.form.get('email')
            phone = request.form.get('phone')
            experience = request.form.get('experience')
            cover_letter = request.form.get('coverLetter')
            position = request.form.get('jobTitle', 'General Application')

            if 'resume' not in request.files or request.files['resume'].filename == '':
                flash('No resume file uploaded', 'error')
                return redirect(request.url)

            file = request.files['resume']

            if file and allowed_file(file.filename):
                upload_result = upload_to_supabase(file, BUCKET_NAME, "resumes")
                if not upload_result:
                    flash('Error uploading file. Please try again.', 'error')
                    return redirect(request.url)

                file_url = upload_result["url"]
                file_key = upload_result["key"]

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


def clear_session_files():
    """Remove expired session files from the session directory"""
    try:
        session_dir = app.config['SESSION_FILE_DIR']
        if os.path.exists(session_dir):
            # Get current time
            now = datetime.now()
            # Check each file in the session directory
            for filename in os.listdir(session_dir):
                filepath = os.path.join(session_dir, filename)
                # If it's a file and older than the session lifetime, remove it
                if os.path.isfile(filepath):
                    modified_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    if now - modified_time > app.config['PERMANENT_SESSION_LIFETIME']:
                        os.remove(filepath)
    except Exception as e:
        print(f"Error cleaning session files: {e}")


@app.teardown_appcontext
def cleanup(error):
    if error:
        clear_session_files()

@app.route('/admin')
def admin():
    """Redirect to admin dashboard if authenticated, otherwise to login page."""
    if is_authorized():
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_login'))

@app.route('/admin/logout', methods=['GET', 'POST'])
def admin_logout():
    """Log out the admin user and clear the session."""
    session.clear()
    flash('Successfully logged out', 'success')
    return redirect(url_for('home'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    
    resumes = []
    try:
        # List files in the Supabase storage bucket
        response = supabase.storage.from_(BUCKET_NAME).list()
        
        if response:
            resumes = []
            for item in response:
                
                if isinstance(item, dict) and "name" in item:
                    display_name = item["name"]
                    if display_name.startswith("resumes/"):
                        display_name = display_name[len("resumes/"):]
                    
                    # Create a record for the template
                    resumes.append({
                        "name": display_name,
                        "key": item["name"],
                        "created_at": item.get("created_at", "Unknown date"),
                        "size": item.get("metadata", {}).get("size", "Unknown size")
                    })
            
    except Exception as e:
        print(f"Error listing files: {e}")
        flash(f"Error loading files from Supabase storage: {str(e)}", "error")
    
    return render_template('admin_dashboard.html', resumes=resumes)


@app.route('/uploads/resumes/<filename>')
@admin_required
def download_resume(filename):
    try:
        # Validate filename to prevent directory traversal
        if '..' in filename or filename.startswith('/'):
            flash('Invalid file path', 'error')
            return redirect(url_for('admin_dashboard'))
        
        # Get the public URL for the file
        file_path = f"resumes/{filename}"
        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(file_path)
        
        return redirect(public_url)
    except Exception as e:
        print(f"Error downloading file: {e}")
        flash('Error downloading file from storage.', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_resume/<path:filename>')
@admin_required
def delete_resume(filename):
    try:
        # Validate filename to prevent directory traversal
        if '..' in filename or filename.startswith('/'):
            flash('Invalid file path', 'error')
            return redirect(url_for('admin_dashboard'))
        
        file_path = f"resumes/{filename}"
        
        supabase.storage.from_(BUCKET_NAME).remove([file_path])
        flash(f"Successfully deleted file from storage.", "success")
    except Exception as e:
        print(f"Error deleting file: {e}")
        flash('Error deleting file from storage.', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/blog')
def blog():
    return render_template('blog.html', active_page='blog')

@app.route('/secret_flag', methods=['GET', 'POST'])
def secret_flag():
    return render_template('secret_flag.html', active_page='secret_flag')

if __name__ == '__main__':
    app.run(debug=False)