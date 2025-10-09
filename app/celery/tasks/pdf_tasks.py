from io import BytesIO
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from app.celery.celery_app import celery
from app.db.models.user import User
from app.db.models.post import Post
from app.db.sync_session import SessionLocal
import base64
from reportlab.lib import colors


@celery.task
def generate_user_profile_pdf(user_id: int):
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.id == user_id).first()
        posts = db.query(Post).filter(Post.author_id == user_id).all()

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        title_font = "Helvetica-Bold"
        content_font = "Helvetica"
        margin = 40
        width, height = A4

        def wrap_text(text, max_width):
            text_object = c.beginText(margin, y)
            text_object.setFont(content_font, 12)
            text_object.setTextOrigin(margin, y)
            text_object.setLeading(14)

            wrapped_lines = []
            current_line = ''
            for word in text.split(' '):
                if c.stringWidth(current_line + ' ' + word) < max_width:
                    current_line += ' ' + word
                else:
                    wrapped_lines.append(current_line)
                    current_line = word
            wrapped_lines.append(current_line)

            for line in wrapped_lines:
                text_object.textLine(line)
            return text_object

        c.setFont(title_font, 18)
        c.setFillColor(colors.darkblue)
        c.drawString(margin, height - margin, f"Profile Report for {user.username}")
        c.setFont(content_font, 12)
        c.setFillColor(colors.black)
        c.drawString(margin, height - margin - 20, f"Email: {user.email}")
        c.drawString(margin, height - margin - 40, f"Joined on: {user.created_at.strftime('%Y-%m-%d')}")
        c.line(margin, height - margin - 50, width - margin, height - margin - 50)

        y = height - margin - 60

        if posts:
            post_counter = 1
            for post in posts:
                if y < 100:
                    c.showPage()
                    y = height - margin

                c.setFont(title_font, 14)
                c.setFillColor(colors.black)
                c.drawString(margin, y, f"Post {post_counter}:")
                y -= 20

                max_width = width - 2 * margin
                wrapped_post_content = wrap_text(post.content, max_width)
                c.drawText(wrapped_post_content)

                y -= 40

                c.setFont(content_font, 10)
                c.setFillColor(colors.black)
                c.drawString(margin, y-30, f"Created on: {post.created_at.strftime('%Y-%m-%d')}")
                y -= 50

                post_counter += 1
        else:
            c.setFont(content_font, 12)
            c.setFillColor(colors.red)
            c.drawString(margin, y, "No posts available.")
            y -= 40

        c.setFont("Helvetica-Oblique", 10)
        c.setFillColor(colors.grey)
        c.drawString(margin, 100, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.save()

        buffer.seek(0)
        encoded_pdf = base64.b64encode(buffer.read()).decode("utf-8")
        return encoded_pdf

    finally:
        db.close()
