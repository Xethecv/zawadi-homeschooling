from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

app = Flask(__name__, static_folder='.', static_url_path='')
load_dotenv()

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')  # You'll need to set this
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')  # You'll need to set this
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')

mail = Mail(app)

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        data = request.form
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        curriculum = data.get('curriculum')
        message = data.get('message')

        # Create email content
        email_body = f"""
        New Contact Form Submission:
        
        Name: {name}
        Email: {email}
        Phone: {phone}
        Curriculum: {curriculum}
        Message: {message}
        """

        # Send email
        msg = Message(
            subject="New Inquiry from Zawadi Homeschooling Website",
            recipients=[os.getenv('RECIPIENT_EMAIL', 'christine.adekee@gmail.com')],
            body=email_body
        )
        mail.send(msg)

        return jsonify({"status": "success", "message": "Thank you for your message! We will get back to you soon."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
