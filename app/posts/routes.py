from flask import render_template,redirect,url_for,Blueprint,flash
from flask_login import current_user,login_required
from app.posts.models import Post
from app.users.models import User,Follow
from app.posts.forms import PostForm
from app import db

blueprint=Blueprint('/posts',__name__)

@blueprint.route('/post/<int:id>',methods=['GET','POST'])
@login_required
def post(id):
    p=Post.query.get_or_404(id)
    post=None
    if p:
        if p.user_id==current_user.id:
            post=p
        else:
            follow=Follow.query.filter_by(follower=current_user.id,followed=p.user_id).first()
            if follow and follow.accept==True:
                post=p
            else:
                flash('For access to this post you have to follow the writer ','danger')
                return redirect(url_for('home'))
    else:
        flash('Somthing wrong this post dosent exist','danger')
        return redirect(url_for('/users/user',id=post.user_id))   



    return render_template('posts/post_content.html',post=post)



@blueprint.route('/update/<int:id>',methods=['GET','POST'])
@login_required
def update_post(id):
   
    post=Post.query.get_or_404(id)
    form=PostForm()
    if post:
        if post.user_id==current_user.id:
                if form.validate_on_submit():
            
                    post.title=form.title.data
                    post.content=form.content.data
                    db.session.add(post)
                    db.session.commit()
                    flash(f'{post.title[:30]}  Updated successfully','success')
                    return redirect(url_for('/posts.post',id=id))

        else:
            flash(f'{current_user.username}  you cannt uodate other person posts!!! ','danger')
            return redirect(url_for('home'))
                
    else:
        flash('Somethongs wrong try agin','danger')
        return redirect(url_for('/posts.post',id=id))

    form.title.data=post.title
    form.content.data=post.content

    return render_template('posts/update_post.html',form=form)


@blueprint.route('/delete/<int:id>',methods=['GET'])
@login_required
def post_delete(id):
    post=Post.query.get_or_404(id)
    if current_user==post.author:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted  ','info')
        return redirect(url_for('/users.user',id=current_user.id))
    else:
        flash('You cannt delete another persons post !!!!   ',['danger',current_user.username])
        return redirect(url_for('home'))

        

@blueprint.route('/new',methods=['GET','POST'])
@login_required
def new():
    form=PostForm()
    if form.validate_on_submit():
            post=Post(title=form.title.data,content=form.content.data,author=current_user)
            db.session.add(post)
            db.session.commit()
            flash(f'{form.title.data[:30 ]} / Successfully Added    ','success')
            return redirect(url_for('/users.user',id=current_user.id))
       
    
    return render_template('posts/create_post.html',form=form)