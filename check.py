import sqlite3
import os

# Đường dẫn đúng đến cơ sở dữ liệu
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'forum.db')

# Kết nối đến cơ sở dữ liệu SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Truy vấn tất cả bài đăng
cursor.execute("SELECT id, title, content, date_posted FROM post")
posts = cursor.fetchall()

# Hiển thị các bài đăng
print("Posts:")
for post in posts:
    print(f"ID: {post[0]}, Title: {post[1]}, Content: {post[2]}, Date Posted: {post[3]}")

# Truy vấn tất cả bình luận
cursor.execute("SELECT id, content, date_commented, post_id FROM comment")
comments = cursor.fetchall()

# Hiển thị các bình luận
print("\nComments:")
for comment in comments:
    print(f"ID: {comment[0]}, Content: {comment[1]}, Date Commented: {comment[2]}, Post ID: {comment[3]}")

# Đóng kết nối
conn.close()
