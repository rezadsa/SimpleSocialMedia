from flask import Flask,render_template,request,flash
from config import DevConfig
from flask_migrate import Migrate
from sqlalchemy import desc
from app.users.models import User,Code,Follow
from app.posts.models import Post


from app.exceptions import error_page_not_found,error_server_internal
from app.extentions import db,login_manager,bcrypt,mail
from app.users.routes import blueprint as users_blueprint
from app.posts.routes import blueprint as posts_blueprint







def register_error_page(app):
    app.register_error_handler(404,error_page_not_found)
    app.register_error_handler(500,error_server_internal)


def register_blueprint(app):
    app.register_blueprint(users_blueprint)
    app.register_blueprint(posts_blueprint)


def register_shell_context(app):
    def shell_context():
        return {
            'db':db,
            'User':User,
            'Code':Code,
            'Follow':Follow,
            'Post':Post
        }
    app.shell_context_processor(shell_context)


app=Flask(__name__)



app.config.from_object(DevConfig)
register_error_page(app)
register_blueprint(app)
register_shell_context(app)





db.init_app(app)

login_manager.init_app(app)
login_manager.login_view='/users.login'
login_manager.login_message='For access to this page you have to login '
login_manager.login_message_category='danger'

bcrypt.init_app(app)

mail.init_app(app)




migrate=Migrate(app,db)






@app.route('/')
def home():
    page=request.args.get('page')

    if page and page.isdigit():
        page=int(page)
    else:
        page=1
    
    
    pages=User.query.where(User.username != None).order_by(desc('create_at')).paginate(page=page,per_page=7)
    return render_template('home.html',pages=pages)



@app.route('/about_me')
def about_me():

    return render_template('about_me.html')



from app.users.forms import ContactMeForm
from flask_mail import Message
@app.route('/contact',methods=['GET','POST'])
def contact():
    form=ContactMeForm()
    if form.validate_on_submit():
       

       title=form.title.data
       email='rezasafarkhani@outlook.com'
       sender=form.email.data    
       msg=Message(title,recipients=[email],sender=sender)
       msg.body=f'{form.name.data} // {form.message.data}'
       mail.send(msg)
       flash('Thank you for contacting me, I will get back to you as soon as possible','primary')

        

    return render_template('contact.html',form=form)


