import json

from flask import Flask, render_template, request, redirect, url_for

FILE_PATH = "data.json"
app = Flask(__name__)


def read_data():
    """
       Read and load blog post data from the JSON file.

       Returns:
           list: A list of blog post dictionaries loaded from the JSON file.
    """
    with open(FILE_PATH, "r") as read_file:
        data = json.load(read_file)
        return data


def write_data(new_posts):
    """
        Write updated blog post data to the JSON file.

        Args:
            new_posts (list): A list of blog post dictionaries to be saved.
    """
    with open(FILE_PATH, "w") as write_file:
        json.dump(new_posts, write_file)


@app.route('/')
def index():
    """
        Render the homepage displaying all blog posts.

        Returns:
            str: Rendered HTML template for the homepage.
    """
    blog_posts = read_data()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
       Handle the creation of a new blog post.

       GET:
           Render the form for adding a new post.

       POST:
           Collect form data, create a new post entry,
           save it to the JSON file, and redirect to the homepage.

       Returns:
           str: Rendered HTML template or redirect response.
    """
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
    """
        Delete a blog post by its unique ID.

        Args:
            post_id (int): The ID of the blog post to delete.

        Returns:
            Response: Redirects to the homepage after deletion.
    """
    blog_posts = read_data()
    for posts in blog_posts:
        if posts['id'] == post_id:
            blog_posts.remove(posts)

    write_data(blog_posts)
    return redirect(url_for('index'))


def fetch_post_by_id(post_id):
    """
        Retrieve a blog post by its unique ID.

        Args:
            post_id (int): The ID of the blog post to retrieve.

        Returns:
            dict | None:
                The matching blog post dictionary if found,
                otherwise None.
    """
    blog_posts = read_data()
    for posts in blog_posts:
        if posts['id'] == post_id:
            return posts
    return None


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
        Update an existing blog post.

        GET:
            Render the update form with the existing post data.

        POST:
            Update the selected post with new form data,
            save changes, and redirect to the homepage.

        Args:
            post_id (int): The ID of the blog post to update.

        Returns:
            str | Response:
                Rendered HTML template, redirect response,
                or 404 error message if the post is not found.
    """
    blog_posts = read_data()
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        post['title'] = request.form.get('title')
        post['author'] = request.form.get('author')
        post['content'] = request.form.get('content')

        write_data(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>')
def add_like(post_id):
    """
        Increment the like count of a blog post.

        If the post does not yet contain a 'likes' field,
        it initializes the field before incrementing.

        Args:
            post_id (int): The ID of the blog post to like.

        Returns:
            Response: Redirects to the homepage after updating likes.
    """
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
