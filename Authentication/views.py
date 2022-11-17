# By Praful Shrivastava !
import code
from django.shortcuts import render, redirect
from django.http import HttpResponse
import hashlib
from . models import images_uploader,Sliced_image,User_Ceren
import random
from random import randint
from django.db.utils import IntegrityError
from django.contrib.auth import  logout as auth_logout
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django_random_queryset import RandomManager
#------------------------------------------------------------------------

def home(request):
    return render(request,'index.html')

def sign(request):
    if request.method == 'GET':
        mail = request.GET.get("email")
        lmail = request.GET.get("logemail")
        name = request.GET.get("nm")
        print('login mail yaha anna chahiye',lmail)
        if mail and name :
            request.session['rmail']=mail
            request.session['name']=name
            print(mail)
            print(name)
            img = images_uploader.objects.all()
            return render(request,'login.html',{'data':img})
        if lmail:
            request.session['lmail']=lmail
            img = list(images_uploader.objects.all())
            random.shuffle(img)
            return render(request,'login.html',{'data':img})
        return render(request,'login.html')

def Encrypt(img,k,request):
    img_fl = open(img,'rb')
    #read image give in byte format
    img = img_fl.read()
    img_fl.close()
    img_bt = bytearray(img)
    for x,y in enumerate(img_bt):
        img_bt[x] = y^k
    x =  request.session.get('e_src')
    uni_name = 'D:/data/G_Encrypter/assets/media/static/Encrypted/'+x+'.jpg'
    print('this is unique name',uni_name)
    file=open(uni_name,'wb')
    file.write(img_bt)
    file.close()
    return uni_name

def hash_find(filename):
    h = hashlib.sha384()
    with open(filename,'rb') as file:
        i = 0
        while i!=b'':
            i = file.read(1024)
            h.update(i)
        return h.hexdigest()

    
def identity(data,request):
    key = ''
    pas_hash = ''
    for x in data:
        data = Sliced_image.objects.filter(Unique_Token=x)
        print(data,'sliced img')
        for y in data:
            if key == '':
                key = 255
            print(key,'this key ----------')
            request.session['e_src']=x
            img_src = 'D:/data/G_Encrypter/assets/media/'+str(y.Images)
            print(img_src)
            print(type(img_src))
            print('ye key hona chahiye',key)
            en = Encrypt(img_src,key,request)
            print('this is encrypt',en)
            hash = hash_find(en)
            ky = hash.split('f')
            kl = len(ky)
            key=kl
            pas_hash = hash
    print('the password hash is',pas_hash)    
    return pas_hash

def password_redirect(request):
    try:
        ls = []
        lmail = request.session.get('lmail')
        fname = request.GET.get('code')
        print(fname)
        if request.method == 'GET':
            if fname and lmail:
                data = list(Sliced_image.objects.filter(Family_name=fname))
                random.shuffle(data)
                print(data)
                return render(request,'login.html',{'slice':data})
            elif fname:
                data = Sliced_image.objects.filter(Family_name=fname)
                print(data)
                return render(request,'login.html',{'slice':data})
            else:
                return redirect('/')
        else:
            data=request.POST['unique']
            lmail = request.session.get('lmail')
            #if lmail session me milla to compare password
            if data and lmail:
                ls = data.split(',')
                hash = identity(ls,request)
                U_info = User_Ceren.objects.filter(Email=lmail,Password=hash)
                if U_info:
                    for x in U_info:
                        print(x)
                        return render(request,'index.html',{'info':x})
                else:
                    msg = "Incorrect User or Password ! Select Valid Image"
                    return render(request,'login.html',{'msg':msg})
            elif data :
                ls = data.split(',')
                request.session['unique']=ls   
                le = len(ls)
                rmail = request.session.get('rmail')
                name = request.session.get('name')
                return render(request,'password.html',{'mail':rmail,'len':le,'name':name})
            else:
                msg = 'Select Valid Image as Your Password'
                return render(request,'login.html',{'msg':msg})
    except Exception as e:
        print(e)
        return redirect('/')    

def generater(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def sendmail(email,name,otp):
    try:
        message = ("""
<html lang="en">

<head>
    <title>G-EncrY official | by Master Industries</title>
    <style>
        h1 {
            text-decoration: none;
            align-items: center;
            color: red;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .card {
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
            transition: 0.3s;
            width: 100%;
            position: fixed;
            align-items: center;
            border-radius: 12px;
        }
        
        .card:hover {
            box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
        }
        
        .container {
            padding: 2px 16px;
        }
    </style>
</head>

<body>
    <h1>G-EncrY Official <br>
        <hr>
    </h1>
    <div class="card">
        <div class="container">
            <h3>Hi &nbsp;"""+str(name)+"""</h3>
            <h4><b>Your One Time Password =</b>
                <font color="blue">"""+str(otp)+"""</font>
            </h4>
            <p>Please Don't Share this 'OTP' to anyone</p>
            <h4>
                <font color="red">Thank You For Become a part of our Family</font><br> If you did have Any Query Contact
                <font color="Blue"> G-EncrY@official</font> or
                <font color="Blue"> Master-Industries</font><br><br> Support : https://Support.G-EncrY@officialbyMaster-Industries.com
                <font color="Blue"> Master-Industries</font><br><br> By Praful Shrivastava
            </h4>
        </div>
    </div>
</body>

</html>""")
        smtp = smtplib.SMTP(host='smtp.gmail.com',port=587)
        smtp.starttls()
        #search on youtube how to create smtp password after two step authenticatiion ! other-wise drop a message in comment  
        # I will provide you a "complete solution" !
        smtp.login("Your Mail Id","Your smtp password of this mail") #provide mail id under double or single codes
        msg  = MIMEMultipart()
        msg['From']  = "Your Mail Id" #provide mail id under double or single codes
        msg['To'] = email
        msg['Subject'] = "G-EncrY official Verification OTP"
        msg.attach(MIMEText(message,'html'))
        smtp.send_message(msg)
        smtp.quit()
        print("Mail sent successfully ____!")
        return True
    except Exception as e:
        print("During Mail Error:",e)
        return False

def sendotp(request):
    try:
        email = request.session.get('rmail')
        name = request.session.get('name')
        otp = generater(5)
        check = sendmail(email,name,otp)
        if check:
            request.session['register_otp'] = otp
            return HttpResponse("<h6 class='alert alert-success'>OTP Send Successfully</h6>")
        else:
            return HttpResponse("<h6 class='alert alert-danger'>OTP Send Failure</h6>")
    except Exception as ex:
        print(ex)
        return HttpResponse("Server Busy !",ex)

def register(request):
    code = request.GET.get('err')
    msg = ""
    if code == '0':
        msg = 'Registered Successfully !'
        return render(request,'login.html',{'msg':msg})
    if code == '1':
        msg = 'Email is already registered !'
    if code == '3':
        msg = ' Registration Failed, Please try again !'
    return render(request,'login.html',{'msg':msg})

def save_user_cre(request):
    code = 0
    try:
        otp = request.POST.get('otp')
        print(type(otp))
        reg_otp = request.session.get('register_otp')
        print(type(reg_otp))
        ls = request.session.get('unique')
        rmail = request.session.get('rmail')
        name = request.session.get('name')
        if reg_otp==int(otp):
            #identity provide img src and password of selected image by user
            pas_hash=identity(ls,request)
            #-----------------------------
            data = User_Ceren()
            data.Name = name
            data.Email = rmail
            data.Password = pas_hash
            data.save()
    except IntegrityError as ex:
        print("User will be already exist")
        code = 1
    except Exception as ex:
        print("this is the error comes out :",ex)
        code = 2
    return redirect("/register?err="+str(code))

def logout(request):
    auth_logout(request)
    return redirect('/')