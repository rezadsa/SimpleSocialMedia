from flask import Blueprint,redirect,render_template,session,url_for,flash
from app.users.forms import RegistrationForm,ValidateForm,UpdateProfileForm,LoginPhoneForm
from app.users.forms import FolowForm,LoginUsernameForm,AccessForm,EmailForm,EmailLoginForm
from app.users.forms import EmailUpdateForm,PhoneUpdateForm
from app.users.models import User,Code,Follow
from app.users.twilio import send_message
from app.users.mail import send_email
from app import db,bcrypt
import random,datetime
from sqlalchemy import and_,or_
from flask_login import login_user,login_required,logout_user,current_user
from app.posts.models import Post

blueprint=Blueprint('/users',__name__)

@blueprint.route('/register',methods=['POST','GET'])
def register():
    form=RegistrationForm()
    email_form=EmailForm()

    if email_form.validate_on_submit():
        session['email_register']=email_form.email.data
        verify_code=random.randint(100000,999999)
        title='noreplay@reza.com'
        body=f'your verification code is   {verify_code}'
        email=email_form.email.data
        # send_email(title=title,body=body,email=email)
        code=Code(number=verify_code,email=email,
                  expire=datetime.datetime.now()+datetime.timedelta(minutes=10))
        
        db.session.add(code)
        db.session.commit()

        expire=code.expire.strftime('%H:%M:%S')
        flash(f'Your Verify Code will be expired after 10 minutes on {expire}','info')
        flash(f'due to Message API charge me for every message I deactived this service / your code is  {verify_code}','primary')

        return redirect(url_for('/users.verify_email_register'))



    if form.validate_on_submit():
        phone=form.phone.data.strip()[-10:]
        if phone.isdigit():
            phone='+44'+phone
            if len(phone)==13:
                session['register_phone']=phone
                verify_code=random.randint(100000,999999)
                # send_message(message=verify_code,phone=phone)
                # verify_code=1111

                code=Code(number=verify_code,phone=phone,
                        expire=datetime.datetime.now()+datetime.timedelta(minutes=10))
                
                

                db.session.add(code)
                db.session.commit()
                expire=code.expire.strftime('%H:%M:%S')
                flash(f'Your Verify Code will be expired after 10 minutes on {expire}','info')
                flash(f'due to Message API charge me for every message I deactived this service / your code is  {verify_code}','success')
                return redirect(url_for('/users.verify_register'))
            else:
                flash('This number is not acceptable','warning')
        else:
            flash('Phone number  must be digits and cannt be contains a character','danger')
        
    return render_template('users/register.html',form=form,email_form=email_form)

# @blueprint.route('/register_by_email',methods=['GET','POST'])
# def register_by_email():
#     email=EmailForm()

@blueprint.route('/verify_email_register',methods=['GET','POST'])
def verify_email_register():
    form=ValidateForm()
    if form.validate_on_submit():
        email=session['email_register']
        code=Code.query.filter_by(email=email).first()
        if code:
            if code.expire>datetime.datetime.now():
                if str(code.number)==str(form.number.data):
                    user=User(email=email)
                    db.session.add(user)
                    db.session.commit()
                    flash(f'{email}  Registered Successfully ','success')
                    return redirect(url_for('home'))
                else:
                    flash(f'{form.number.data}  is wrong, please try agin  ','danger')
            
            else:
                flash('Sorry this code is expire','info')
                return redirect(url_for('/users.register'))
    
    return render_template('users/email_verify.html',form=form)



@blueprint.route('/verify_register',methods=['POST','GET'])
def verify_register():
    form=ValidateForm()
    if form.validate_on_submit():
        phone=session['register_phone']
        code=Code.query.filter_by(phone=phone).first()
        if code:
            if code.expire > datetime.datetime.now():
                if str(code.number)==str(form.number.data):
                    user=User(phone=phone)
                    db.session.add(user)
                    db.session.commit()
                    flash(f'{phone}  Registered Successfully ','success')
                    return redirect(url_for('home'))
                else:
                    flash(f'{form.number.data}  is wrong, please try agin  ','danger')
            else:
                flash('Sorry this code is expire','info')
                return redirect(url_for('/users.register'))


    return render_template('users/verify.html',form=form)


@blueprint.route('/login',methods=['POST','GET'])
def login():

    if current_user.is_authenticated:
        flash(f'you already logged in, if you want login by another account first logout ','warning')
        return redirect(url_for('home'))

    phone_form=LoginPhoneForm()
    username_form=LoginUsernameForm()
    email_form=EmailLoginForm()

    if email_form.validate_on_submit():          

                email=email_form.email.data
                session['login_email']=email
                user=User.query.filter_by(email=email).first()
                if user:
                    verify_code=random.randint(100000,999999)
                    title='noreplay@reza.com'
                    body=f'your verification code is   {verify_code}'
                    email=email_form.email.data
                    # send_email(title=title,body=body,email=email)
                    code=Code(number=verify_code,email=email,
                    expire=datetime.datetime.now()+datetime.timedelta(minutes=10))
        
                    db.session.add(code)
                    db.session.commit()

                    expire=code.expire.strftime('%H:%M:%S')
                    flash(f'Your Verify Code will be expired after 10 minutes on {expire}','info')
                    flash(f'due to Message API charge me for every message I deactived this service / your code is  {verify_code}','primary')

                    return redirect(url_for('/users.verify_email_login'))
                    
    
    if phone_form.validate_on_submit():
        # if form.login_type=='phone':
                phone=phone_form.phone.data.strip()[-10:]
                if phone.isdigit():
                    phone='+44'+phone
                    if len(phone)==13:
                        session['login_phone']=phone
                        user=User.query.filter_by(phone=phone).first()
                        if user:
                            rand_num=random.randint(100000,999999)
                            # send_message(message=rand_num,phone=phone)
                            # rand_num=2222
                            code=Code(phone=phone,number=rand_num,expire=datetime.datetime.now()+datetime.timedelta(minutes=10))
                            db.session.add(code)
                            db.session.commit()
                            expire=code.expire.strftime('%H:%M:%S')
                            flash(f'Your Verify Code will be expired after 10 minutes on {expire}','info')
                            flash(f'due to Message API charge me for every message I deactived this service / your code is  {rand_num}','primary')
                            
                            return redirect(url_for('/users.verify_login'))

                        else:
                            flash('Your are not registered, Please first register  ','info')
                            return redirect(url_for('/users.register'))

                    else:
                        flash('Please enter vaild phone number  ','warning')
                else:
                    flash('Phone number  must be digits and cannt be contains a character','danger')




        # elif form.login_type=='username':
    if username_form.validate_on_submit():
        user=User.query.filter_by(username=username_form.username.data).first()
        if user:
            password_correct=bcrypt.check_password_hash(user.password,username_form.password.data) 
            if password_correct  and  user.login_attempt <=3:
                login_user(user,remember=username_form.remember.data)
                current_user.login_attempt=0
                db.session.commit()
                flash(f'{current_user.username}, Welcome  ','success')
                return redirect(url_for('home'))
            else:
                user.login_attempt=user.login_attempt+1
                db.session.add(user)
                db.session.commit()
                flash(f'Your password is incorrect {user.login_attempt} time(s), after 3 times you just can use phone number for login ','danger')
                
        else:
            flash(f'{username_form.username.data}   doesnt exist ','danger')



    return render_template('users/login_by_username.html',phone_form=phone_form,username_form=username_form,email_form=email_form)

@blueprint.route('/verify_email_login',methods=['POST','GET'])
def verify_email_login():

    form=ValidateForm()
    if form.validate_on_submit():
        email=session['login_email']
        code=Code.query.filter_by(email=email).first()
        if code:
            if code.expire >datetime.datetime.now():
                if str(code.number)==str(form.number.data).strip():
                    user=User.query.filter_by(email=email).first()
                    login_user(user)
                    current_user.login_attempt=0
                    db.session.commit()
                    name=current_user.username if current_user.username else current_user.email
                    flash(f'{name} Welcome','success')
                    return redirect(url_for('home'))
                else:
                    flash(f'{form.number.data} is incorect,try agin','danger')
            else:
                flash('The verification code is expire, try agin ','warning')
                return redirect(url_for('/users.login'))
            

    return render_template('users/verify.html',form=form)



 






@blueprint.route('/verify_login',methods=['POST','GET'])
def verify_login():
    form=ValidateForm()
    if form.validate_on_submit():
        phone=session['login_phone']
        code=Code.query.filter_by(phone=phone).first()
        if code:
            if code.expire >datetime.datetime.now():
                if str(code.number)==str(form.number.data).strip():
                    user=User.query.filter_by(phone=phone).first()
                    login_user(user)
                    current_user.login_attempt=0
                    db.session.commit()
                    name=current_user.username if current_user.username else current_user.phone
                    flash(f'{name} Welcome','success')
                    return redirect(url_for('home'))
                else:
                    flash(f'{form.number.data} is incorect,try agin','danger')
            else:
                flash('The verification code is expire, try agin ','warning')
                return redirect(url_for('/users.login'))
            

    return render_template('users/verify.html',form=form)


@blueprint.route('/logout',methods=['POST','GET'])
@login_required
def logout():
    name=current_user.username if current_user.username else current_user.phone
    logout_user()
    flash(f'{name} logout successfully','info')
    return redirect(url_for('home'))

@blueprint.route('/settings',methods=['POST','GET'])
@login_required
def settings():
    username_form=UpdateProfileForm()
    access_form=AccessForm()
    phone_form=PhoneUpdateForm()
    email_form=EmailUpdateForm()

    if email_form.validate_on_submit():
        if current_user.phone:
            verify_code=random.randint(100000,999999)
            expire=datetime.datetime.now()+datetime.timedelta(minutes=10)

            session['update_email']=email_form.email.data

            title='noreplay@reza.com'
            body=f'your verification code is   {verify_code}'
            phone=current_user.phone
           
            # send_message(message=verify_code,phone=current_user.phone)
        
            code=Code(number=verify_code,email=email_form.email.data, expire=expire,user_id=current_user.id)

            db.session.add(code)
            db.session.commit()

                                
            expire=code.expire.strftime('%H:%M:%S')
            flash(f' Code sent to your phone  {current_user.phone}, Its will be expired after 10 minutes on {expire}','info')
            flash(f'due to Message API charge me for every message I deactived this service / your code is  {verify_code}','primary')
            return redirect('/update_email')
        else:
            flash('Before change your email address you have to set phone number','danger')


    if phone_form.validate_on_submit():
        if current_user.email:
            verify_code=random.randint(100000,999999)
            expire=datetime.datetime.now()+datetime.timedelta(minutes=10)

            session['update_phone']=phone_form.phone.data

            title='noreplay@reza.com'
            body=f'your verification code is   {verify_code}'
            email=current_user.email
            # send_email(title=title,body=body,email=email)
            code=Code(number=verify_code,email=email, expire=expire,user_id=current_user.id)

            db.session.add(code)
            db.session.commit()

                                
            expire=code.expire.strftime('%H:%M:%S')
            flash(f' Code sent to your email  {current_user.email}, Its will be expired after 10 minutes on {expire}','info')
            flash(f'due to Message API charge me for every message I deactived this service / your code is  {verify_code}','primary')
            return redirect('/update_phone')
        else:
            flash('Before change your phone nubmer you have to set Email','danger')



    if username_form.validate_on_submit() :
                  verify_code=random.randint(100000,999999)
                  expire=datetime.datetime.now()+datetime.timedelta(minutes=10)

                  session['username']=username_form.username.data
                  hashed_password=bcrypt.generate_password_hash(username_form.password.data)
                  session['hashed_pass']=hashed_password

                  
                  if current_user.email:  
                   
                    title='noreplay@reza.com'
                    body=f'your verification code is   {verify_code}'
                    email=current_user.email
                    # send_email(title=title,body=body,email=email)
                    code=Code(number=verify_code,email=email, expire=expire,user_id=current_user.id)
        
                    db.session.add(code)
                    db.session.commit()

                                       
                    expire=code.expire.strftime('%H:%M:%S')
                    flash(f' Code sent to your email  {current_user.email}, Its will be expired after 10 minutes on {expire}','info')
                    flash(f'due to Message API charge me for every message I deactived this service / your code is  {verify_code}','primary')
                    return redirect('/update_username')
                  elif current_user.phone:
                    # send_message(message=verify_code,phone=current_user.phone)
                                       
                    code=Code(phone=current_user.phone,number=verify_code,expire=expire,user_id=current_user.id)
                    db.session.add(code)
                    db.session.commit()
                   
                    expire=expire.strftime('%H:%M:%S')
                    flash(f' Code sent to your phone  {current_user.phone}, Its will be expired after 10 minutes on {expire}','info')
                    flash(f'due to Message API charge me for every message I deactived this service / your code is  {verify_code}','primary')
                    return redirect('/update_username')
                  else:
                      flash('For update/set username & password you must set email or phone','danger')
       
           
    
    access_form.private.data=current_user.private
    access_form.phone_show.data=current_user.phone_show
    username_form.username.data=current_user.username
    phone_form.phone.data=current_user.phone
    email_form.email.data=current_user.email

    return render_template('users/settings.html',username_form=username_form,access_form=access_form,phone_form=phone_form,email_form=email_form)

@blueprint.route('/update_username',methods=['GET','POST'])
@login_required
def update_username():
    form=ValidateForm()
    if form.validate_on_submit():
        # email=session['email_update']
        code=Code.query.filter_by(user_id=current_user.id).first()
        print(code)
        if code:
            if code.expire>datetime.datetime.now():
                if str(code.number)==str(form.number.data):
                    current_user.username=session['username']
                    current_user.password=session['hashed_pass']
                    db.session.commit()
                    flash(f'{current_user.username}  your profile updated successfuly ','success')
                    return redirect(url_for('/users.settings'))
                else:
                    flash('This code is wrong, try agin','danger')
            else:
                flash('Sorry your code is expire, try agin','info')
                return redirect(url_for('/users.settings'))
        else:
            flash('Something worng happend!!! try Agin','info')
            return redirect(url_for('/users.settings'))



    return render_template('users/verify.html',form=form)

@blueprint.route('/update_phone',methods=['GET','POST'])
@login_required
def update_phone():
    form=ValidateForm()
    if form.validate_on_submit():
        code=Code.query.filter_by(user_id=current_user.id).first()
        if code:
            if code.expire>datetime.datetime.now():
                if str(code.number)==str(form.number.data):
                    phone=session['update_phone']
                    current_user.phone=phone
                    db.session.commit()
                    flash(f'{current_user.phone}  updated successfuly','success')
                    return redirect(url_for('/users.settings'))
                else:
                    flash('Your varification code is wrong, try again','danger')
            else:
                flash('Your varification code expired, try agin','info')
                return redirect(url_for('/users.settings'))
        else:
            flash('Something wrong happend Try agin','warning')
            return redirect(url_for('/users.settings'))


    return render_template('users/verify.html',form=form)


@blueprint.route('/update_email',methods=['GET','POST'])
@login_required
def update_email():
    form=ValidateForm()
    if form.validate_on_submit():
        code=Code.query.filter_by(user_id=current_user.id).first()
        if code:
            if code.expire>datetime.datetime.now():
                if str(code.number)==str(form.number.data):
                    email=code.email
                    current_user.email=email
                    db.session.commit()
                    flash(f'{current_user.email}  updated successfuly','success')
                    return redirect(url_for('/users.settings'))
                else:
                    flash('Your varification code is wrong, try again','danger')
            else:
                flash('Your varification code expired, try agin','info')
                return redirect(url_for('/users.settings'))
        else:
            flash('Something wrong happend Try agin','warning')
            return redirect(url_for('/users.settings'))


    return render_template('users/verify.html',form=form)


@blueprint.route('/access_control',methods=['POST','GET'])
@login_required
def access_control():
        form=AccessForm()
        if form.validate_on_submit():
            current_user.private=form.private.data
            current_user.phone_show=form.phone_show.data
            db.session.commit()
            flash(f'Your access control apdated successfully ','info')
            return redirect(url_for('/users.settings'))
        else:
            flash('What you want to do ','danger')
            return redirect(url_for('home'))
    

@blueprint.route('/user/<int:id>',methods=['POST','GET'])
def user(id):
    user=User.query.get_or_404(id)
    follow=False
    access=False
    form=FolowForm()

    if current_user.is_authenticated and user:
        relation=Follow.query.filter_by(follower=current_user.id,followed=user.id).first()
        if relation:
            follow=True

            if relation.accept and user.private:
                access=True

    posts=Post.query.filter_by(user_id=id).all()

    


    return render_template('users/user.html',user=user,follow=follow,form=form,access=access,posts=posts)

@blueprint.route('/follow/<int:user_id>',methods=['POST'])
@login_required
def follow(user_id):
    user=User.query.filter_by(id=user_id).first()
    if user:
        if user !=current_user:
            relation=Follow.query.filter_by(follower=current_user.id,followed=user.id).first()
            if relation:
                db.session.delete(relation)
                db.session.commit()
            
            relation=Follow(follower=current_user.id,followed=user.id)
            db.session.add(relation)
            db.session.commit()
            flash(f'following request Sent ...','info')
            return redirect(url_for('/users.user',id=user_id))
        else:
            flash('You cannt follow yourself ','warning')
            return redirect(url_for('home'))
    else:
        flash('Sorry somthing is worng  ','danger')
        return redirect(url_for('home'))
    
@blueprint.route('/unfollow/<int:user_id>',methods=['POST'])
@login_required
def unfollow(user_id):
    user=User.query.filter_by(id=user_id).first()
    if user:
        if user!=current_user:
            relation=Follow.query.filter_by(follower=current_user.id,followed=user.id).first()
            if relation:
                db.session.delete(relation)
                db.session.commit()
                flash('You unfollowed successfully','success')
            return redirect(url_for('/users.user',id=user_id))

        else:
            flash('You cannt unfollow yourself','danger')
    else:
        flash('Sorry somthing is wrong','danger')
        return redirect(url_for('home'))









@blueprint.route('/requests/<int:id>',methods=['GET','POST'])
@login_required
def requests(id):

    user=User.query.filter_by(id=id).first()
    requests=None
    if user:
         if current_user==user:
            # ids=[x.follower for x in Follow.query.filter_by(followed=user.id).all()]
            # all_ids=[x.id for x in Follow.query.filter_by(followed=user.id).all()]
            # ids=[x.follower for x in ]
            # requests=User.query.where(User.id.in_(ids)).all()
            # requests=Follow.select().where(followed=user.id and_ accept=False)

            ids=[x.follower for x in Follow.query.filter_by(followed=user.id , accept=False).all()]
            print(ids)
            requests=User.query.where(User.id.in_(ids))
            

         else:
             flash('what you want to do','danger')
             return redirect(url_for('home'))


    else:
        flash('something wrong happend','danger')
        return redirect(url_for('home'))
  
    return render_template('users/requests.html',requests=requests)


@blueprint.route('/follow_accept/<int:id>',methods=['POST','GET'])
@login_required
def follow_accept(id):
    user=User.query.filter_by(id=id).first()
    if user:
        follow=Follow.query.filter_by(follower=user.id,followed=current_user.id).first()
        follow.accept=True
        db.session.add(follow)
        db.session.commit()
        return redirect(url_for('/users.requests',id=current_user.id))

    

@blueprint.route('/follow_reject/<int:id>',methods=['POST','GET'])
@login_required
def follow_reject(id):
    user=User.query.filter_by(id=id).first()
    if user:
        follow=Follow.query.filter_by(follower=user.id,followed=current_user.id).first()
        db.session.delete(follow)
        db.session.commit()
        return redirect(url_for('/users.requests',id=current_user.id))
    
@blueprint.route('/followers',methods=['POST','GET'])
@login_required
def followers():
    ids=[x.follower for x in  Follow.query.filter_by(followed=current_user.id,accept=True)]
    users=User.query.where(User.id.in_(ids)).all()
    print(ids)
    print(users)
    
    return render_template('users/follower.html',users=users)

@blueprint.route('/followed',methods=['GET','POST'])
@login_required
def followed():
    ids=[x.followed for x in  Follow.query.filter_by(follower=current_user.id,accept=True)]
    users=User.query.where(User.id.in_(ids)).all()
    
    return render_template('users/followed.html',users=users)    


