from django.shortcuts import render , redirect , HttpResponse
from .models import Account
from django.core.mail import send_mail
from django.conf import settings
import random

# Create your views here.
def index(request):
    return render(request,"index.html")
    
def create(request):
    if request.method  == "POST":
        name = request.POST['name']
        dob = request.POST['dob']
        aadhar = request.POST['aadhar']
        phone = request.POST['phone']
        address = request.POST['address']
        email = request.POST['email']
        print(name,dob,phone,aadhar,address)
        Account.objects.create(name = name,DOB=dob,Aadhar = aadhar,mobile = phone,address = address,email= email)
        send_mail( f"hello {name},thank you for creating an acc in our bank", # subject
        "Online-banking-system , \n welcome to family of our bank \n we are happy for it \n , regards \n manager(DJD-E1)\n thank you ****!"# body
        ,settings.EMAIL_HOST_USER,[email],fail_silently=False
            )
        print("sent succesfully")
    return render(request,"create.html")


def pin_gen(request):
    if request.method == "POST":
        otp = random.randint(100000,999999)
        acc = request.POST.get('acc')
        data = Account.objects.get(acc= acc)
        email = data.email
        send_mail( f"hello {data.name}",
                  
        f"Online-banking-system , \n the OTP (One time Password ) is {otp} \n please share the otp only with our employees not for the outside scamers , it is kind request \n , regards \n manager(DJD-E1)\n  we scam bcz we care   "# body
        ,settings.EMAIL_HOST_USER,[email],fail_silently=False
            )
        print("sent succesfully")
        data.otp = otp 
        data.save()
        return redirect("otp")
    return render(request,'pin.html')


def valid_otp(request):
    # msg = ""
    context= {}
    if request.method == "POST":
        acc = request.POST['acc']
        otp = int(request.POST['otp'])
        pin1 = int(request.POST['pin1'])
        pin2 = int(request.POST['pin2'])

        if pin1 != pin2:
            context["error"]= "PIN and Confirm PIN do not match."
        else:
            try:
                # Get account data
                data = Account.objects.get(acc=acc)
                # Validate OTP
                if data.otp == otp:
                    data.pin = pin2
                    data.save()
                    send_mail( f"hello {data.name}, PIN GENERATION ",
                    f"Online-banking-system , \n the we are happy to scam you  \n you successfully generated pin, we are happy to inform that we know ur otp and pin as well so we are happy to use ur money `(ur money is our money & our money is our money )` \n , regards \n manager(DJD-E1)\n  we scam bcz we care   "# body
                    ,settings.EMAIL_HOST_USER,[data.email],fail_silently=False
                    )
                    print("sent succesfully")
                    context["success"]= "PIN successfully updated and confirmation email sent."
                else:
                    context["error"]= "OTP mismatch. Please check and try again."
            except Account.DoesNotExist:
                context["error"]= "Account does not exist."
    return render(request, 'valid_otp.html', context)
        
def balance(request):
    # msg=""
    context = {}
    if request.method == "POST":
        acc = request.POST['acc']
        pin = request.POST['pin']
        try:
            data = Account.objects.get(acc = int(acc))
            if data.pin == int(pin):
                # bal = data.bal
                context["success"]= f"Your current balance is ₹{data.bal}"
            else:
                context["error"]= "Incorrect PIN."
        except Account.DoesNotExist:
            context["error"]= "Please enter the valid Account Number"
    return render(request,'bal.html',context)

def withdrawl(request):
    # msg = ""
    context = {}
    if request.method == "POST":
        acc = request.POST['acc']
        pin = request.POST['pin']
        amt = int(request.POST.get('amt'))
        try:
            data = Account.objects.get(acc = acc)
            if data.pin == int(pin):
                if data.bal >= amt and amt >0:
                    data.bal -= amt
                    data.save()
                    context["success"] = f"₹{amt} withdrawn successfully. New balance: ₹{data.bal}"
                    send_mail( f"hello {data.name} WHITHDRAWL ",
                        f"Online-banking-system , \n from ur {data.acc}  \n ,{amt} as be withdrawled from ATM the availble balance is {data.bal} \n , regards \n manager(DJD-E1)\n  we scam bcz we care   "# body
                        ,settings.EMAIL_HOST_USER,[data.email],fail_silently=False
                    )
                    print("sent succesfully")
                    # return redirect("index")
                else:
                     context["error"]="No Money" 
            else:
                 context["error"]="Incorrect PIN"
        except:
             context["error"]="Please enter the valid Account Number"
    return render(request,'with.html',context)

def deposit(request):
    # msg=" "
    context = {}
    if request.method == "POST":
        acc = request.POST['acc']
        pin = request.POST['pin']
        amt = int(request.POST.get('amt'))
        try:
            data = Account.objects.get(acc = acc)
            if data.pin == int(pin):
                if amt >= 100 and amt <= 10000:
                    data.bal += amt
                    data.save()
                    context["success"] = f"₹{amt} Deposited successfully. New balance: ₹{data.bal}"
                    send_mail( f"hello {data.name} DEPOSIT ",
                        f"Online-banking-system , \n from ur {data.acc}  \n ,{amt} as be deposited to ur acc {data.acc}  balance is {data.bal} \n , regards \n manager(DJD-E1)\n  we scam bcz we care   "# body
                        ,settings.EMAIL_HOST_USER,[data.email],fail_silently=False
                    )
                    # return redirect("index")
                else:
                    context["error"]="No money"
            else:
                context["error"]="Incorrect pin"
        except:
            context["error"]="Please enter the valid Account Number"
    return render(request,'deposit.html',context)   

def transfer(request):
    # msg = ""
    context = {}
    if request.method == "POST":
        f_acc = request.POST.get('f_acc')
        t_acc = request.POST.get('t_acc')
        pin = request.POST.get('pin')
        amt = request.POST.get('amt')
        try:
            from_acc = Account.objects.get(acc = f_acc)
        except:
            context["error"] = "Sender Accout is not valid"
        try:
            to_acc = Account.objects.get(acc = t_acc)
        except:
            context["error"] = "Reciever Account is not valid"
            
        if from_acc.pin == int(pin):
            if int(amt)>100 and int(amt)<=10000 and int(amt) <= from_acc.bal:
                from_acc.bal-=int(amt)
                from_acc.save()

                send_mail( f"hello {from_acc.name} ACCOUNT TRANSFER ",
                    
                    f"Online-banking-system , \n from ur {from_acc.acc}  \n ,{amt} as be debited to  {to_acc.acc} acc  balance is {from_acc.bal} \n , regards \n manager(DJD-E1)\n  we scam bcz we care   "# body

                    ,settings.EMAIL_HOST_USER,[from_acc.email],fail_silently=False
                )
                print("sent succesfully")
                to_acc.bal += int(amt)
                to_acc.save()
                context["success"] = f"₹{amt} Transferred successfully from {f_acc} to {t_acc}."
                send_mail( f"hello {from_acc.name} ACCOUNT TRANSFER ",
                    
                    f"Online-banking-system , \n  {to_acc.acc}  \n ,{amt} YOUR acc has been credited from   {from_acc.acc} acc  balance is {to_acc.bal} \n , regards \n manager(DJD-E1)\n  we scam bcz we care   "# body

                    ,settings.EMAIL_HOST_USER,[to_acc.email],fail_silently=False
                )
                print("sent succesfully")
            else:
                context["error"] = "Enter the valid Amount"
        else:
            context["error"] = "Incorrect pin"

    return render(request,'transfer.html',context)
