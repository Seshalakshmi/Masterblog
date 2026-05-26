from flask import Flask, render_template, request, redirect, url_for
import json

FILE_PATH = "data.json"
app = Flask(__name__)

def read_data():
    with open(FILE_PATH, "r") as read_file:
        data = json.load(read_file)
        return data

def write_data(new_posts):
    with open(FILE_PATH, "w") as write_file:
        json.dump(new_posts, write_file)

@app.route('/')
def index():
    blog_posts = read_data()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    blog_posts = read_data()
    if request.method == 'POST':
        if not blog_posts:
            author_id = 1
        else:
            author_id = blog_posts[-1]['id'] + 1
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        new_post = {
            "id": author_id,
            "author": author,
            "title": title,
            "content": content
        }
        blog_posts.append(new_post)

        write_data(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    # Find the blog post with the given id and remove it from the list
    # Redirect back to the home page
    blog_posts = read_data()
    for posts in blog_posts:
        if posts['id'] == post_id:
            blog_posts.remove(posts)

    write_data(blog_posts)
    return redirect(url_for('index'))


def fetch_post_by_id(post_id):
    blog_posts = read_data()
    for posts in blog_posts:
        if posts['id'] == post_id:
            return posts
    return None

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = read_data()
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        for posts in blog_posts:
            if posts['id'] == post_id:
                posts['title'] = request.form.get('title')
                posts['author'] = request.form.get('author')
                posts['content'] = request.form.get('content')

        write_data(blog_posts)
        return redirect(url_for('index'))

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>')
def add_like(post_id):
    blog_posts = read_data()
    for posts in blog_posts:
        if posts['id'] == post_id:
            if 'likes' not in posts:
                posts['likes'] = 0
            posts['likes'] += 1

    write_data(blog_posts)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)