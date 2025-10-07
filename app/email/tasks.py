from fastapi import BackgroundTasks
from app.email.email_service import send_email

# send welcome email to the user after signup
async def send_welcome_email(
    background_tasks: BackgroundTasks, user_email: str, username: str
):
    subject = "Welcome to SocialHub!"

    html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h2 style="color: #4A90E2;">Welcome to <span style="color: red;">SocialHub</span>, {username}!</h2>
            <p style="font-size: 16px; color: #333;">
                Thank you for signing up with <strong>SocialHub</strong>. Good to see you here.
            <p style="font-size: 16px; color: #333;">
                Start exploring, connecting, and sharing your thoughts with people from all around the world.
            </p>
            <h3 style="color: #E35335;">KEEP IT UP {username}...🤩</h3>
            </div>
        </body>
        </html>
    """

    background_tasks.add_task(send_email, user_email, subject, html_content)


# mail the followers when a user creates a new post
async def notify_followers_new_post(
    background_tasks: BackgroundTasks,
    follower_emails: list,
    post_content: str,
    username: str,
):
    subject = f"{username} has created new post on SocialHub"
    body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h2 style="color: #4A90E2; margin-bottom: 20px;">
                New Post on <span style="color: #e74c3c;">SocialHub</span> by <strong>{username}</strong>
            </h2> <hr>
            <p style="font-size: 16px; color: #333; line-height: 1.6;">
                {post_content}
            </p>
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 14px; color: #999;">
                You’re receiving this email because you follow {username} on SocialHub.
            </p>
            </div>
        </body>
        </html>
    """
    for email in follower_emails:
        background_tasks.add_task(send_email, email, subject, body)
