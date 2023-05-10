from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField,PasswordField,BooleanField,SubmitField,EmailField,TextAreaField
from wtforms.validators import Email,EqualTo,ValidationError,DataRequired,Length
from app.users.models import User,Code
from app import db
from flask_login import current_user



class RegistrationForm(FlaskForm):

    phone=StringField('Phone Number',validators=[DataRequired(),
                                                 Length(min=10,max=13,message='phone format : +441234567890,441234567890, 01234567890, 1234567890')])
    
    def validate_phone(self,phone):
        phone='+44'+phone.data.strip()[-10:]
        codes=Code.query.filter_by(phone=phone)
        if codes:
            Code.query.filter_by(phone=phone).delete()
            db.session.commit()

        user=User.query.filter_by(phone=phone).first()
        if user:
          raise ValidationError(f'{phone} , This phone number already registered ')
        

class EmailForm(FlaskForm):
     email=EmailField('Email',validators=[DataRequired(),Email()])

     def validate_email(self,email):
          codes=Code.query.filter_by(email=email.data)
          if codes:
               Code.query.filter_by(email=email.data).delete()
               db.session.commit()

          user=User.query.filter_by(email=email.data).first()
          if user:
               raise ValidationError(f'{email} , This email already registered' )
          
class EmailLoginForm(FlaskForm):
     email=EmailField('Email',validators=[DataRequired(),Email()])

     def validate_email(self,email):
          codes=Code.query.filter_by(email=email.data)
          if codes:
               Code.query.filter_by(email=email.data).delete()
               db.session.commit()

     

class ValidateForm(FlaskForm):
     number=IntegerField('Validation Code')





class LoginPhoneForm(FlaskForm):
      phone=StringField('Phone Number',validators=[DataRequired(),
                                                 Length(min=10,max=13,message='phone format : +441234567890,441234567890, 01234567890, 1234567890')])
      def validate_phone(self,phone):
            phone='+44'+phone.data.strip()[-10:]
            codes=Code.query.filter_by(phone=phone)
            if codes:
                Code.query.filter_by(phone=phone).delete()
                db.session.commit()

class LoginUsernameForm(FlaskForm):
   
    username=StringField('User Name',validators=[DataRequired(),Length(min=4,max=20)])
    password=PasswordField('PassWord ',validators=[DataRequired()])
    remember=BooleanField('Remmember Me')



    def validate_username(self,username):
         user=User.query.filter_by(username=username.data).first()
         if user:
              if user.login_attempt >=3:
                   raise ValidationError('Due to some security issues, you can only login with your phone number ')

class UpdateProfileForm(FlaskForm):
     username=StringField('User Name ',validators=[DataRequired(),Length(min=4,max=30)])
     password=PasswordField('Password',validators=[DataRequired(),Length(min=4,max=30),EqualTo('verify_pass',message='Passwords must be match')])
     verify_pass=PasswordField('Verify Password')
    
     def validate_username(self,username):
          codes=Code.query.filter_by(phone=current_user.phone)
          if codes:
               Code.query.filter_by(phone=current_user.phone).delete()
               db.session.commit()
          
          codes=Code.query.filter_by(email=current_user.email)
          if codes:
               Code.query.filter_by(email=current_user.email).delete()
               db.session.commit()

          codes=Code.query.filter_by(user_id=current_user.id)
          if codes:
               Code.query.filter_by(user_id=current_user.id).delete()
               db.session.commit()

          user=User.query.filter_by(username=username.data).first()
          if user:
            if user !=current_user :
               raise ValidationError('This username already exist ')
            
class EmailUpdateForm(FlaskForm):
     email=EmailField('Email',validators=[DataRequired(),Email()])
    
     def validate_email(self,email):
          codes=Code.query.filter_by(phone=current_user.phone)
          if codes:
               Code.query.filter_by(phone=current_user.phone).delete()
               db.session.commit()
          code=Code.query.filter_by(user_id=current_user.id).first()
          if code:
               Code.query.filter_by(user_id=current_user.id).delete()
               db.session.commit()

          user=User.query.filter_by(email=email.data).first()
          if user and user!=current_user:
               raise ValidationError(f'{email.data} , This email already registered' )
          
class PhoneUpdateForm(FlaskForm):
     phone=StringField('Phone Number',validators=[DataRequired(),
                                                 Length(min=10,max=13,message='phone format : +441234567890,441234567890, 01234567890, 1234567890')])
    


     def validate_phone(self,phone):
          phone='+44'+phone.data.strip()[-10:]
          codes=Code.query.filter_by(email=current_user.email)
          if codes:
               Code.query.filter_by(email=current_user.email).delete()
               db.session.commit()

          code=Code.query.filter_by(user_id=current_user.id).first()
          if code:
               Code.query.filter_by(user_id=current_user.id).delete()
               db.session.commit()

          user=User.query.filter_by(phone=phone).first()
          if user and user!=current_user:
               raise ValidationError(f'{phone} , This phone number already registered ')
    


class AccessForm(FlaskForm):

     private=BooleanField('Private')
     phone_show=BooleanField('Show My phone')

class FolowForm(FlaskForm):

     submit=SubmitField('Submin')



class ContactMeForm(FlaskForm):
    
    email=EmailField('Email',validators=[DataRequired(),Email()])
    name=StringField('Your name/organization (optinal)')
    title=StringField('title',validators=[DataRequired()])
    message=TextAreaField('Message')
