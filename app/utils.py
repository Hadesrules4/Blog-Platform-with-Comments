import re
import unicodedata
from functools import wraps
from flask import abort
from flask_login import current_user


def slugify(text):
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", normalized).strip("-").lower()
    return slug or "post"


def unique_slug(title, post_id=None):
    from .models import Post
    base = slugify(title)[:200]
    candidate = base
    counter = 2
    while True:
        query = Post.query.filter_by(slug=candidate)
        if post_id:
            query = query.filter(Post.id != post_id)
        if query.first() is None:
            return candidate[:220]
        suffix = f"-{counter}"
        candidate = f"{base[:220-len(suffix)]}{suffix}"
        counter += 1


def validate_credentials(username, email, password):
    errors = []
    if not re.fullmatch(r"[A-Za-z0-9_]{3,30}", username):
        errors.append("Username must be 3–30 characters and use only letters, numbers, or underscores.")
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        errors.append("Enter a valid email address.")
    if len(password) < 8:
        errors.append("Password must contain at least 8 characters.")
    if len(password) > 128:
        errors.append("Password must be 128 characters or fewer.")
    return errors


def validate_post(title, content):
    errors = []
    if not title:
        errors.append("Title is required.")
    elif len(title) > 200:
        errors.append("Title must be 200 characters or fewer.")
    if not content:
        errors.append("Content is required.")
    elif len(content) > 20000:
        errors.append("Content must be 20,000 characters or fewer.")
    return errors


def post_owner_required(view):
    @wraps(view)
    def wrapped(post_id, *args, **kwargs):
        from .models import Post
        post = Post.query.get_or_404(post_id)
        if post.author_id != current_user.id and current_user.role != "admin":
            abort(403)
        return view(post_id, *args, **kwargs)
    return wrapped
