from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from ..extensions import bcrypt, db
from ..models import Comment, Post, User
from ..utils import unique_slug, validate_post

api_bp=Blueprint("api",__name__)
def user_json(user): return {"id":user.id,"username":user.username}
def comment_json(c): return {"id":c.id,"content":c.content,"author":user_json(c.author),"post_id":c.post_id,"created_at":c.created_at.isoformat()}
def post_json(p,include_comments=False):
    d={"id":p.id,"title":p.title,"slug":p.slug,"content":p.content,"author":user_json(p.author),"created_at":p.created_at.isoformat(),"updated_at":p.updated_at.isoformat()}
    if include_comments: d["comments"]=[comment_json(c) for c in p.comments]
    return d
def current_api_user(): return db.session.get(User,int(get_jwt_identity()))

@api_bp.get("/health")
def health(): return jsonify({"status":"ok","service":"BlogSphere API","version":"1.0.0"})

@api_bp.post("/auth/login")
def api_login():
    data=request.get_json(silent=True) or {}; identity=str(data.get("identity","")).strip(); password=str(data.get("password",""))
    user=User.query.filter((User.email==identity.lower())|(User.username==identity)).first()
    if not user or not bcrypt.check_password_hash(user.password_hash,password): return jsonify({"error":"invalid credentials"}),401
    token=create_access_token(identity=str(user.id))
    return jsonify({"access_token":token,"token_type":"Bearer","user":{"id":user.id,"username":user.username,"role":user.role}})

@api_bp.get("/posts")
def list_posts():
    page=max(request.args.get("page",1,type=int),1); per_page=min(max(request.args.get("per_page",10,type=int),1),50); search=request.args.get("q","").strip()
    query=Post.query
    if search:
        from sqlalchemy import or_
        like=f"%{search}%"; query=query.filter(or_(Post.title.ilike(like),Post.content.ilike(like)))
    p=query.order_by(Post.created_at.desc()).paginate(page=page,per_page=per_page,error_out=False)
    return jsonify({"items":[post_json(x) for x in p.items],"page":p.page,"per_page":p.per_page,"pages":p.pages,"total":p.total})

@api_bp.get("/posts/<int:post_id>")
def get_post(post_id): return jsonify(post_json(Post.query.get_or_404(post_id),True))

@api_bp.post("/posts")
@jwt_required()
def create_post_api():
    data=request.get_json(silent=True) or {}; title=str(data.get("title","")).strip(); content=str(data.get("content","")).strip(); errors=validate_post(title,content)
    if errors: return jsonify({"errors":errors}),400
    user=current_api_user(); post=Post(title=title,slug=unique_slug(title),content=content,author_id=user.id)
    db.session.add(post); db.session.commit(); return jsonify(post_json(post)),201

@api_bp.put("/posts/<int:post_id>")
@jwt_required()
def update_post_api(post_id):
    post=Post.query.get_or_404(post_id); user=current_api_user()
    if post.author_id!=user.id and user.role!="admin": return jsonify({"error":"forbidden"}),403
    data=request.get_json(silent=True) or {}; title=str(data.get("title",post.title)).strip(); content=str(data.get("content",post.content)).strip(); errors=validate_post(title,content)
    if errors: return jsonify({"errors":errors}),400
    post.title=title; post.slug=unique_slug(title,post.id); post.content=content; db.session.commit(); return jsonify(post_json(post))

@api_bp.delete("/posts/<int:post_id>")
@jwt_required()
def delete_post_api(post_id):
    post=Post.query.get_or_404(post_id); user=current_api_user()
    if post.author_id!=user.id and user.role!="admin": return jsonify({"error":"forbidden"}),403
    db.session.delete(post); db.session.commit(); return jsonify({"message":"post deleted"})

@api_bp.post("/posts/<int:post_id>/comments")
@jwt_required()
def create_comment_api(post_id):
    Post.query.get_or_404(post_id); data=request.get_json(silent=True) or {}; content=str(data.get("content","")).strip()
    if not content: return jsonify({"error":"content is required"}),400
    if len(content)>1000: return jsonify({"error":"comment is too long"}),400
    user=current_api_user(); c=Comment(content=content,author_id=user.id,post_id=post_id); db.session.add(c); db.session.commit()
    return jsonify(comment_json(c)),201

@api_bp.delete("/comments/<int:comment_id>")
@jwt_required()
def delete_comment_api(comment_id):
    c=Comment.query.get_or_404(comment_id); user=current_api_user()
    if c.author_id!=user.id and user.role!="admin": return jsonify({"error":"forbidden"}),403
    db.session.delete(c); db.session.commit(); return jsonify({"message":"comment deleted"})

@api_bp.get("/users/me")
@jwt_required()
def me():
    user=current_api_user(); return jsonify({"id":user.id,"username":user.username,"email":user.email,"role":user.role})
