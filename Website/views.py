from flask import Blueprint, redirect,render_template, request, flash, url_for
from .models import Blog, User
from .forms import BlogForm, EditPostForm
from . import db
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/' , methods = ['GET'])
@login_required
def home():
    blogs = Blog.query.order_by(Blog.date.desc()).all()
    return render_template('home.html', user = current_user, blogs = blogs)


@views.route('/entry', methods = ['GET', 'POST'])
@login_required
def add_entry():
    form = BlogForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_post = Blog(
                            title=form.title.data, 
                            category=form.category.data, 
                            date = request.form.get('date'),
                            content=form.content.data, 
                            user_id = current_user.id
                            )

        
            try:
                db.session.add(new_post)
                db.session.commit()
                flash('New post created successfully!', category='success')
                return redirect(url_for('views.home'))
            except Exception as e:
                db.session.rollback()
                flash('Error creating blog post', category='error')
                print(e)
                return redirect(url_for('views.add_entry'))
            
        print("Something went wrong here!!!")    
        return redirect(url_for('views.add_entry'))

    return render_template('entry.html', user=current_user, form = form)

@views.route('/categories', methods = ['GET'])
@login_required
def categories():
    categories = {blog.category for blog in Blog.query.all()}
    return render_template('categories.html', user=current_user, categories=categories )


@views.route('/post/<int:post_id>', methods = ['GET'])
@login_required
def blog_post(post_id):
    post = Blog.query.get_or_404(post_id)
    return render_template('blogPost.html', user=current_user, post=post)

@views.route('/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Blog.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash('You do not have permission to delete this post.')
        return redirect(url_for('views.myposts'))

    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted.')
    return redirect(url_for('views.myposts'))


@views.route('/myposts')
@login_required
def myposts():
    posts = Blog.query.filter_by(user_id = current_user.id).order_by(Blog.date.desc()).all()
    return render_template('myposts.html', user=current_user, posts=posts)

@views.route('/author/<username>')
@login_required
def author(username):
    users = User.query.filter_by(username=username).first_or_404()
    posts = Blog.query.filter_by(user_id=users.id).order_by(Blog.date.desc()).all()
    return render_template('author.html', user=current_user, posts=posts, author=users)


@views.route('/edit-post/<int:post_id>', methods = ['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Blog.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash('You do not have permission to edit this post.')
        return redirect(url_for('views.myposts'))
        

    form = EditPostForm()
    if form.validate_on_submit():
        
        post.title = form.title.data
        post.category = form.category.data
        post.content = form.content.data
                
        db.session.commit() 
        print(post.title) 
        flash('Your post has been updated!', category='success')
        return redirect(url_for('views.myposts'))
    
    form.title.data = post.title
    form.category.data = post.category
    form.content.data = post.content
        
    return render_template('editposts.html',user=current_user, form=form, post=post)


@views.route('/category/<category_name>')
def category_posts(category_name):
    posts = Blog.query.filter_by(category=category_name).all()
    return render_template('categoryposts.html', user=current_user, posts=posts, category_name=category_name)
