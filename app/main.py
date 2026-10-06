from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_
from .extensions import db
from .models import Comment, Post
from .utils import unique_slug, validate_post

main_bp = Blueprint("main", __name__)

@main_bp.get("/")
def home():
    page = max(request.args.get("page", 1, type=int), 1)
    search = request.args.get("q", "").strip()
    query = Post.query
    if search:
        like = f"%{search}%"
        query = query.filter(or_(Post.title.ilike(like), Post.content.ilike(like)))
    pagination = query.order_by(Post.created_at.desc()).paginate(page=page, per_page=6, error_out=False)
    return render_template("home.html", pagination=pagination, posts=pagination.items, search=search)

@main_bp.get("/post/<int:post_id>")
def post_detail(post_id):
    return render_template("post_detail.html", post=Post.query.get_or_404(post_id))

@main_bp.route("/posts/new", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        title=request.form.get("title","").strip(); content=request.form.get("content","").strip()
        errors=validate_post(title,content)
        if errors:
            for error in errors: flash(error,"danger")
            return render_template("post_form.html",post=None)
        post=Post(title=title,slug=unique_slug(title),content=content,author_id=current_user.id)
        db.session.add(post); db.session.commit()
        flash("Post published successfully.","success")
        return redirect(url_for("main.post_detail",post_id=post.id))
    return render_template("post_form.html",post=None)

@main_bp.route("/posts/<int:post_id>/edit", methods=["GET","POST"])
@login_required
def edit_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author_id != current_user.id and current_user.role != "admin":
        flash("You are not allowed to edit this post.","danger"); return redirect(url_for("main.post_detail",post_id=post.id))
    if request.method=="POST":
        title=request.form.get("title","").strip(); content=request.form.get("content","").strip()
        errors=validate_post(title,content)
        if errors:
            for error in errors: flash(error,"danger")
            return render_template("post_form.html",post=post)
        post.title=title; post.slug=unique_slug(title,post.id); post.content=content
        db.session.commit(); flash("Post updated successfully.","success")
        return redirect(url_for("main.post_detail",post_id=post.id))
    return render_template("post_form.html",post=post)

@main_bp.post("/posts/<int:post_id>/delete")
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author_id != current_user.id and current_user.role != "admin":
        flash("You are not allowed to delete this post.","danger"); return redirect(url_for("main.post_detail",post_id=post.id))
    db.session.delete(post); db.session.commit(); flash("Post deleted.","info")
    return redirect(url_for("main.home"))

@main_bp.post("/post/<int:post_id>/comments")
@login_required
def add_comment(post_id):
    post=Post.query.get_or_404(post_id); content=request.form.get("content","").strip()
    if not content: flash("Comment cannot be empty.","danger")
    elif len(content)>1000: flash("Comment must be 1000 characters or fewer.","danger")
    else:
        db.session.add(Comment(content=content,author_id=current_user.id,post_id=post.id)); db.session.commit()
        flash("Comment added.","success")
    return redirect(url_for("main.post_detail",post_id=post.id)+"#comments")

@main_bp.post("/comments/<int:comment_id>/delete")
@login_required
def delete_comment(comment_id):
    comment=Comment.query.get_or_404(comment_id)
    if comment.author_id != current_user.id and current_user.role != "admin":
        flash("You are not allowed to delete this comment.","danger")
    else:
        post_id=comment.post_id; db.session.delete(comment); db.session.commit(); flash("Comment deleted.","info")
        return redirect(url_for("main.post_detail",post_id=post_id)+"#comments")
    return redirect(url_for("main.post_detail",post_id=comment.post_id)+"#comments")
