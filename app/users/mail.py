
from app import mail
from flask_mail import Message


def send_email(title,body,email):

        msg=Message(title,recipients=[email],sender='noreply@app.com')
        msg.body=body
        mail.send(msg)


# @app.route('/contact',methods=['GET','POST'])
# def contact():
   
#     if request.method=='POST':
#             print('2--------------------------------------------')
#             msg=Message('Hello reza this is flask test',sender='noreply@reza.com',recipients=['rezadarehshoori@outlook.com'])
#             msg.body='reza darehshoori safarkhanni'
#             mail.send(msg)
#             return 'send email'
           

#     return render_template('contact.html')

