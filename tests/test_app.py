import os, tempfile, pytest
from app import create_app
from app.extensions import db
from app.models import Post

@pytest.fixture()
def app():
    fd,path=tempfile.mkstemp(suffix=".db"); os.close(fd)
    app=create_app({"TESTING":True,"SQLALCHEMY_DATABASE_URI":"sqlite:///"+path,"SECRET_KEY":"test-secret","JWT_SECRET_KEY":"jwt-test-secret"})
    with app.app_context(): db.drop_all(); db.create_all()
    yield app
    with app.app_context(): db.session.remove(); db.drop_all()
    os.unlink(path)

def register(c,username="tester",email="tester@example.com",password="password123"):
    return c.post("/register",data={"username":username,"email":email,"password":password},follow_redirects=True)
def login(c,identity="tester",password="password123"):
    return c.post("/login",data={"identity":identity,"password":password},follow_redirects=True)

def test_health(app): assert app.test_client().get("/api/health").json["status"]=="ok"
def test_registration_and_login(app):
    c=app.test_client(); assert b"Account created successfully" in register(c).data; assert b"Welcome back" in login(c).data
def test_duplicate_registration(app):
    c=app.test_client(); register(c); assert b"Email is already registered" in register(c,"tester2").data
def test_post_crud_and_comments(app):
    c=app.test_client(); register(c); login(c)
    r=c.post("/posts/new",data={"title":"Hello World","content":"First post"},follow_redirects=True); assert b"Hello World" in r.data
    with app.app_context(): pid=Post.query.first().id
    assert b"Great post!" in c.post(f"/post/{pid}/comments",data={"content":"Great post!"},follow_redirects=True).data
    assert b"Updated" in c.post(f"/posts/{pid}/edit",data={"title":"Updated","content":"Changed"},follow_redirects=True).data
    assert b"Post deleted" in c.post(f"/posts/{pid}/delete",follow_redirects=True).data
def test_api_requires_jwt(app): assert app.test_client().post("/api/posts",json={"title":"Nope","content":"No token"}).status_code==401
def test_api_login_and_post(app):
    c=app.test_client(); register(c); r=c.post("/api/auth/login",json={"identity":"tester","password":"password123"}); assert r.status_code==200
    token=r.json["access_token"]; r=c.post("/api/posts",json={"title":"API Post","content":"REST"},headers={"Authorization":f"Bearer {token}"}); assert r.status_code==201
def test_api_search(app):
    c=app.test_client(); register(c); login(c); c.post("/posts/new",data={"title":"Python Flask","content":"Backend"}); c.post("/posts/new",data={"title":"Database","content":"SQL"})
    assert c.get("/api/posts?q=Python").json["total"]==1
