def send_comment_notification(
    post_author_email: str,
    commenter_username: str,
    post_title: str
):
    print(
        f"""
EMAIL NOTIFICATION

To: {post_author_email}
Subject: New Comment

{commenter_username} commented on your post:
{post_title}
"""
    )


def send_like_notification(
    post_author_email: str,
    liker_username: str,
    post_title: str
):
    print(
        f"""
EMAIL NOTIFICATION

To: {post_author_email}
Subject: New Like

{liker_username} liked your post:
{post_title}
"""
    )