"""
Complete SendGrid Email Sender for AI Readiness Assessment
All email functions in one file
"""

import streamlit as st
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Bcc, Content, Attachment, FileContent, FileName, FileType, Disposition
import base64


def send_assessment_report_email(
    recipient_email: str,
    recipient_name: str,
    html_report: str,
    scores_data: dict,
    company_name: str = "Your Organization"
):
    """
    Send HTML assessment report via email using SendGrid with report as attachment
    
    Args:
        recipient_email: Recipient's email address
        recipient_name: Recipient's name
        html_report: HTML content of the report
        scores_data: Dictionary with assessment scores
        company_name: Name of the company/organization
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Get SendGrid credentials from Streamlit secrets
        api_key = st.secrets["sendgrid"]["api_key"]
        sender_email = st.secrets["sendgrid"]["sender_email"]
        sender_name = st.secrets["sendgrid"]["sender_name"]
        
        # Get total score
        total_score = scores_data.get('total', 0)
        
        # Get dimension scores
        raw_scores = scores_data.get('raw_dimension_scores', [0, 0, 0, 0, 0, 0])
        if isinstance(raw_scores, dict):
            dim1 = raw_scores.get(1, 0)
            dim2 = raw_scores.get(2, 0)
            dim3 = raw_scores.get(3, 0)
            dim4 = raw_scores.get(4, 0)
            dim5 = raw_scores.get(5, 0)
            dim6 = raw_scores.get(6, 0)
        else:
            dim1 = raw_scores[0] if len(raw_scores) > 0 else 0
            dim2 = raw_scores[1] if len(raw_scores) > 1 else 0
            dim3 = raw_scores[2] if len(raw_scores) > 2 else 0
            dim4 = raw_scores[3] if len(raw_scores) > 3 else 0
            dim5 = raw_scores[4] if len(raw_scores) > 4 else 0
            dim6 = raw_scores[5] if len(raw_scores) > 5 else 0
        
        # Create email subject
        subject = f"Your AI Readiness Assessment Results - Score: {total_score}/90"
        
        # Create email body (plain text version)
        plain_text = f"""
Hi {recipient_name},

Thank you for completing the AI Readiness Assessment!

Your Organization: {company_name}
Total AI Readiness Score: {total_score}/90

Your comprehensive HTML report is attached to this email. Open it in any browser to view:
• Detailed breakdown across 6 dimensions
• Personalized recommendations
• Industry benchmark comparisons
• Visual score charts

Key Scores:
• Process Maturity: {dim1}/15
• Technology Infrastructure: {dim2}/15
• Data Readiness: {dim3}/15
• People & Culture: {dim4}/15
• Leadership & Alignment: {dim5}/15
• Change Management: {dim6}/15

Questions or want to discuss your results?
Reply to this email or schedule a consultation at www.tlogicconsulting.com

Best regards,
{sender_name}
        """
        
        # Create HTML email body
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .header h1 {{ margin: 0; font-size: 24px; }}
        .score-box {{ background: #f0f9ff; padding: 20px; margin: 20px 0; border-radius: 8px; text-align: center; }}
        .score-box h2 {{ color: #1e3a8a; margin: 0 0 10px 0; font-size: 36px; }}
        .dimensions {{ background: white; padding: 20px; }}
        .dimension {{ margin: 15px 0; padding: 10px; background: #f9fafb; border-radius: 5px; }}
        .dimension strong {{ color: #1e3a8a; }}
        .footer {{ background: #f3f4f6; padding: 20px; text-align: center; margin-top: 30px; border-radius: 0 0 10px 10px; }}
        .button {{ display: inline-block; background: #3b82f6; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Your AI Readiness Assessment Results</h1>
            <p style="margin: 10px 0 0 0; opacity: 0.9;">{company_name}</p>
        </div>
        
        <div class="score-box">
            <p style="margin: 0; color: #6b7280; font-size: 14px;">TOTAL AI READINESS SCORE</p>
            <h2>{total_score}/90</h2>
            <p style="margin: 0; color: #6b7280;">Your comprehensive report is attached below</p>
        </div>
        
        <div class="dimensions">
            <h3 style="color: #1e3a8a;">Your Dimension Scores:</h3>
            
            <div class="dimension">
                <strong>Process Maturity:</strong> {dim1}/15
            </div>
            <div class="dimension">
                <strong>Technology Infrastructure:</strong> {dim2}/15
            </div>
            <div class="dimension">
                <strong>Data Readiness:</strong> {dim3}/15
            </div>
            <div class="dimension">
                <strong>People & Culture:</strong> {dim4}/15
            </div>
            <div class="dimension">
                <strong>Leadership & Alignment:</strong> {dim5}/15
            </div>
            <div class="dimension">
                <strong>Change Management:</strong> {dim6}/15
            </div>
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <p><strong>📎 Your detailed HTML report is attached to this email.</strong></p>
            <p style="color: #6b7280;">Open it in any browser to view interactive charts and personalized recommendations.</p>
        </div>
        
        <div class="footer">
            <p style="margin: 0 0 10px 0;"><strong>Want to discuss your results?</strong></p>
            <p style="margin: 0; color: #6b7280;">Reply to this email or visit www.tlogicconsulting.com</p>
        </div>
    </div>
</body>
</html>
        """
        
        # Create the email message
        message = Mail(
            from_email=Email(sender_email, sender_name),
            to_emails=To(recipient_email, recipient_name),
            subject=subject,
            plain_text_content=Content("text/plain", plain_text),
            html_content=Content("text/html", html_content)
        )
        
        # Add BCC to yourself so you get a copy of the report
        message.bcc = Bcc(sender_email)
        
        # Attach the HTML report
        # Create safe filename
        safe_company = "".join(c for c in company_name if c.isalnum() or c in (' ', '_')).rstrip()
        safe_company = safe_company.replace(' ', '_') or "Your_Company"
        filename = f"{safe_company}_AI_Readiness_Report.html"
        
        # Encode HTML report in base64
        encoded_report = base64.b64encode(html_report.encode()).decode()
        
        # Create attachment
        attached_file = Attachment(
            FileContent(encoded_report),
            FileName(filename),
            FileType('text/html'),
            Disposition('attachment')
        )
        message.attachment = attached_file
        
        # Send email via SendGrid
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        
        # Check response
        if response.status_code in [200, 201, 202]:
            return True, f"Report sent successfully to {recipient_email}"
        else:
            return False, f"SendGrid returned status code: {response.status_code}"
            
    except KeyError as e:
        return False, f"Missing SendGrid configuration in secrets: {str(e)}"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"


def send_notification_to_tlogic(
    user_name: str,
    user_email: str,
    user_company: str,
    scores_data: dict,
    user_title: str = "",
    user_phone: str = "",
    user_location: str = "",
    ai_stage: str = ""
):
    """
    Send notification to T-Logic team when someone completes assessment
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Get SendGrid credentials
        api_key = st.secrets["sendgrid"]["api_key"]
        sender_email = st.secrets["sendgrid"]["sender_email"]
        sender_name = st.secrets["sendgrid"]["sender_name"]
        
        # T-Logic notification email (you can change this)
        tlogic_email = sender_email  # Send to yourself
        
        total_score = scores_data.get('total', 0)
        
        # Get dimension scores - handle both formats
        raw_scores = scores_data.get('raw_dimension_scores', [0, 0, 0, 0, 0, 0])
        if isinstance(raw_scores, dict):
            # Convert dict format {1: 9, 2: 9...} to list
            dim1 = raw_scores.get(1, 0)
            dim2 = raw_scores.get(2, 0)
            dim3 = raw_scores.get(3, 0)
            dim4 = raw_scores.get(4, 0)
            dim5 = raw_scores.get(5, 0)
            dim6 = raw_scores.get(6, 0)
        else:
            # List format [9, 9, 9, 9, 9, 9]
            dim1 = raw_scores[0] if len(raw_scores) > 0 else 0
            dim2 = raw_scores[1] if len(raw_scores) > 1 else 0
            dim3 = raw_scores[2] if len(raw_scores) > 2 else 0
            dim4 = raw_scores[3] if len(raw_scores) > 3 else 0
            dim5 = raw_scores[4] if len(raw_scores) > 4 else 0
            dim6 = raw_scores[5] if len(raw_scores) > 5 else 0
        
        subject = f"New Assessment Completed: {user_name} from {user_company} - Score: {total_score}"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #1e3a8a; color: white; padding: 20px; }}
        .info {{ background: #f3f4f6; padding: 15px; margin: 15px 0; border-radius: 5px; }}
        .scores {{ background: white; padding: 15px; border: 1px solid #e5e7eb; border-radius: 5px; }}
        .score-item {{ padding: 8px; margin: 5px 0; background: #f9fafb; border-radius: 3px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>🎯 New Assessment Completed!</h2>
        </div>
        
        <div class="info">
            <h3>Contact Information:</h3>
            <p><strong>Name:</strong> {user_name}</p>
            <p><strong>Email:</strong> {user_email}</p>
            <p><strong>Company:</strong> {user_company}</p>
            <p><strong>Title:</strong> {user_title or 'Not provided'}</p>
            <p><strong>Phone:</strong> {user_phone or 'Not provided'}</p>
            <p><strong>Location:</strong> {user_location or 'Not provided'}</p>
            <p><strong>AI Stage:</strong> {ai_stage or 'Not provided'}</p>
        </div>
        
        <div class="scores">
            <h3>Assessment Scores:</h3>
            <div class="score-item"><strong>Total Score:</strong> {total_score}/90</div>
            <div class="score-item">Process Maturity: {dim1}/15</div>
            <div class="score-item">Technology: {dim2}/15</div>
            <div class="score-item">Data Readiness: {dim3}/15</div>
            <div class="score-item">People & Culture: {dim4}/15</div>
            <div class="score-item">Leadership: {dim5}/15</div>
            <div class="score-item">Change Management: {dim6}/15</div>
        </div>
        
        <p style="margin-top: 20px; color: #6b7280;">Follow up with this lead!</p>
    </div>
</body>
</html>
        """
        
        message = Mail(
            from_email=Email(sender_email, sender_name),
            to_emails=To(tlogic_email),
            subject=subject,
            html_content=Content("text/html", html_content)
        )
        
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        
        if response.status_code in [200, 201, 202]:
            return True, "Notification sent to T-Logic"
        else:
            return False, f"Status code: {response.status_code}"
            
    except Exception as e:
        return False, f"Error: {str(e)}"


def send_assistance_request_email(
    user_name: str,
    user_email: str,
    user_company: str,
    message: str,
    user_phone: str = "",
    user_title: str = ""
):
    """
    Send assistance request from user to T-Logic team via SendGrid
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Get SendGrid credentials from secrets
        api_key = st.secrets["sendgrid"]["api_key"]
        sender_email = st.secrets["sendgrid"]["sender_email"]
        sender_name = st.secrets["sendgrid"]["sender_name"]
        
        # Email to T-Logic
        tlogic_email = sender_email  # Send to yourself
        
        # Create subject
        subject = f"🆘 Assistance Request from {user_name} - {user_company}"
        
        # Create HTML email content
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #dc2626; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
        .content {{ background: white; padding: 20px; border: 1px solid #e5e7eb; }}
        .info-section {{ background: #f9fafb; padding: 15px; margin: 15px 0; border-left: 4px solid #3b82f6; border-radius: 4px; }}
        .message-section {{ background: #fef3c7; padding: 15px; margin: 15px 0; border-left: 4px solid #f59e0b; border-radius: 4px; }}
        .label {{ font-weight: bold; color: #1e3a8a; }}
        .footer {{ background: #f3f4f6; padding: 15px; text-align: center; border-radius: 0 0 8px 8px; color: #6b7280; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>🆘 Assistance Request Received</h2>
        </div>
        
        <div class="content">
            <div class="info-section">
                <h3 style="margin-top: 0; color: #1e3a8a;">Contact Information:</h3>
                <p><span class="label">Name:</span> {user_name}</p>
                <p><span class="label">Email:</span> {user_email}</p>
                <p><span class="label">Company:</span> {user_company}</p>
                <p><span class="label">Title:</span> {user_title or 'Not provided'}</p>
                <p><span class="label">Phone:</span> {user_phone or 'Not provided'}</p>
            </div>
            
            <div class="message-section">
                <h3 style="margin-top: 0; color: #f59e0b;">Their Message:</h3>
                <p style="white-space: pre-wrap;">{message}</p>
            </div>
            
            <div style="margin-top: 20px; padding: 15px; background: #e0f2fe; border-radius: 4px;">
                <p style="margin: 0;"><strong>⚡ Action Required:</strong> Please respond to this assistance request promptly!</p>
            </div>
        </div>
        
        <div class="footer">
            <p style="margin: 0;">AI Readiness Assessment Platform</p>
            <p style="margin: 5px 0 0 0; font-size: 12px;">Automated notification from Streamlit app</p>
        </div>
    </div>
</body>
</html>
        """
        
        # Create plain text version
        plain_text = f"""
ASSISTANCE REQUEST RECEIVED

Contact Information:
Name: {user_name}
Email: {user_email}
Company: {user_company}
Title: {user_title or 'Not provided'}
Phone: {user_phone or 'Not provided'}

Their Message:
{message}

Please respond to this assistance request promptly!
        """
        
        # Create and send email
        mail_message = Mail(
            from_email=Email(sender_email, sender_name),
            to_emails=To(tlogic_email),
            subject=subject,
            plain_text_content=Content("text/plain", plain_text),
            html_content=Content("text/html", html_content)
        )
        
        sg = SendGridAPIClient(api_key)
        response = sg.send(mail_message)
        
        if response.status_code in [200, 201, 202]:
            return True, f"Assistance request sent successfully to {tlogic_email}"
        else:
            return False, f"SendGrid returned status code: {response.status_code}"
            
    except KeyError as e:
        return False, f"Missing SendGrid configuration in secrets: {str(e)}"
    except Exception as e:
        return False, f"Error sending assistance request: {str(e)}"


def send_feedback_email(
    user_name: str,
    user_email: str,
    feedback_text: str,
    rating: str = "",
    user_company: str = "",
    assessment_score: str = ""
):
    """
    Send user feedback to T-Logic team via SendGrid
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Get SendGrid credentials from secrets
        api_key = st.secrets["sendgrid"]["api_key"]
        sender_email = st.secrets["sendgrid"]["sender_email"]
        sender_name = st.secrets["sendgrid"]["sender_name"]
        
        # Email to T-Logic
        tlogic_email = sender_email  # Send to yourself
        
        # Create subject
        subject = f"💬 Feedback from {user_name}" + (f" - {user_company}" if user_company else "")
        
        # Create HTML email content
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #8b5cf6; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
        .content {{ background: white; padding: 20px; border: 1px solid #e5e7eb; }}
        .info-section {{ background: #f9fafb; padding: 15px; margin: 15px 0; border-left: 4px solid #8b5cf6; border-radius: 4px; }}
        .feedback-section {{ background: #f0f9ff; padding: 15px; margin: 15px 0; border-left: 4px solid #3b82f6; border-radius: 4px; }}
        .rating {{ font-size: 24px; color: #f59e0b; }}
        .label {{ font-weight: bold; color: #1e3a8a; }}
        .footer {{ background: #f3f4f6; padding: 15px; text-align: center; border-radius: 0 0 8px 8px; color: #6b7280; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>💬 User Feedback Received</h2>
        </div>
        
        <div class="content">
            <div class="info-section">
                <h3 style="margin-top: 0; color: #8b5cf6;">From:</h3>
                <p><span class="label">Name:</span> {user_name}</p>
                <p><span class="label">Email:</span> {user_email}</p>
                {f'<p><span class="label">Company:</span> {user_company}</p>' if user_company else ''}
                {f'<p><span class="label">Assessment Score:</span> {assessment_score}</p>' if assessment_score else ''}
                {f'<p class="rating"><span class="label">Rating:</span> {rating}</p>' if rating else ''}
            </div>
            
            <div class="feedback-section">
                <h3 style="margin-top: 0; color: #3b82f6;">Feedback:</h3>
                <p style="white-space: pre-wrap;">{feedback_text}</p>
            </div>
            
            <div style="margin-top: 20px; padding: 15px; background: #f0fdf4; border-radius: 4px;">
                <p style="margin: 0;"><strong>💡 Great!</strong> User feedback helps improve the assessment experience.</p>
            </div>
        </div>
        
        <div class="footer">
            <p style="margin: 0;">AI Readiness Assessment Platform</p>
            <p style="margin: 5px 0 0 0; font-size: 12px;">Automated notification from Streamlit app</p>
        </div>
    </div>
</body>
</html>
        """
        
        # Create plain text version
        plain_text = f"""
USER FEEDBACK RECEIVED

From:
Name: {user_name}
Email: {user_email}
{f'Company: {user_company}' if user_company else ''}
{f'Assessment Score: {assessment_score}' if assessment_score else ''}
{f'Rating: {rating}' if rating else ''}

Feedback:
{feedback_text}

User feedback helps improve the assessment experience.
        """
        
        # Create and send email
        mail_message = Mail(
            from_email=Email(sender_email, sender_name),
            to_emails=To(tlogic_email),
            subject=subject,
            plain_text_content=Content("text/plain", plain_text),
            html_content=Content("text/html", html_content)
        )
        
        sg = SendGridAPIClient(api_key)
        response = sg.send(mail_message)
        
        if response.status_code in [200, 201, 202]:
            return True, f"Feedback sent successfully to {tlogic_email}"
        else:
            return False, f"SendGrid returned status code: {response.status_code}"
            
    except KeyError as e:
        return False, f"Missing SendGrid configuration in secrets: {str(e)}"
    except Exception as e:
        return False, f"Error sending feedback: {str(e)}"
