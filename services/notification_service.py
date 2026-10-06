from services.email_service import send_email


async def notify_post_owner(
    owner_email: str,
    post_title: str,
    user_name: str,
    activity_type: str,
    timestamp
):

    if activity_type == "comment":

        activity = "Commented on your post"

    elif activity_type == "like":

        activity = "Liked your post"

    else:

        activity = "Activity on your post"


    formatted_time = timestamp.strftime(
        "%Y-%m-%d %I:%M %p"
    )


    subject = (
        f"New activity on your post: "
        f"{post_title}"
    )


    body = f"""
Hello,

There is new activity on your blog post.

Post: {post_title}

User: {user_name}

Activity: {activity}

Time: {formatted_time}

Regards,
Blog Management Team
"""


    await send_email(
        recipient_email=owner_email,
        subject=subject,
        body=body
    )