from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
db = SQLAlchemy(app)

# Kiểm tra loại file hợp lệ
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Model bài đăng
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    image_filename = db.Column(db.String(200), nullable=True)
    comments = db.relationship('Comment', backref='post', lazy=True)

# Model bình luận
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_commented = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    image_filename = db.Column(db.String(200), nullable=True)

# Trang chủ - hiển thị danh sách bài đăng
@app.route('/')
def index():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

# Trang đăng bài
@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image = request.files.get('image')

        image_filename = None
        if image and allowed_file(image.filename):
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        new_post = Post(title=title, content=content, image_filename=image_filename)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/')
    return render_template('new_post.html')

# Trang hiển thị bài đăng và bình luận
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        comment_content = request.form['comment']
        image = request.files.get('comment_image')

        image_filename = None
        if image and allowed_file(image.filename):
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        new_comment = Comment(content=comment_content, post_id=post.id, image_filename=image_filename)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('post_detail', post_id=post.id))

    comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.date_commented.asc()).all()
    return render_template('post_detail.html', post=post, comments=comments)

# Để trả về hình ảnh đã tải lên
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tạo các bảng trong cơ sở dữ liệu
    app.run(debug=True)
