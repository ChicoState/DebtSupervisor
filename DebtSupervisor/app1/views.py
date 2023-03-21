from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from app1.forms import JoinForm, LoginForm,debtForm
from app1.models import Debtentry
from django.contrib.auth.models import User



# Create your views here.

@login_required
def home (request):
    if request.user.is_authenticated:
        if Debtentry.objects.filter(user=request.user).count() > 0:
            table_data = Debtentry.objects.filter(user=request.user).order_by('-transactionDate')
            total_balance = 0
            for items in table_data:
                total_balance = items.currBalance + total_balance
            
            context={
                "table_data":table_data,
                "total_balance":total_balance
            }

            return render (request, 'app1/home.html',context)
        else:
            return render (request, 'app1/home.html')

    else:
        return render (request, 'app1/home.html')
        

def join(request):
    if (request.method == "POST"):
        join_form = JoinForm(request.POST)
        if (join_form.is_valid()):
            # Save form data to DB
            user = join_form.save()
            # Encrypt the password 
            user.set_password(user.password)
            # Save encrypted password to DB 
            user.save()
            # Success! Redirect to home page.
            return redirect("/")
        else:
            # Form invalid, print errors to console
            page_data = { "join_form": join_form }
            return render(request, 'app1/join.html', page_data)
    else:
        join_form = JoinForm()
        page_data = { "join_form": join_form }
        return render(request, 'app1/join.html', page_data)

def user_login(request):
    if (request.method == 'POST'):
        login_form = LoginForm(request.POST) 
        if login_form.is_valid():
            # First get the username and password supplied 
            username = login_form.cleaned_data["username"] 
            password = login_form.cleaned_data["password"] 
            # Django's built-in authentication function:
            user = authenticate(username=username, password=password) 
        # If we have a user
        if user:
            #Check it the account is active 
            if user.is_active:
                # Log the user in. 
                login(request,user)
                # Send the user back to homepage 
                return redirect("/")
            else:
            # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password)) 
            return render(request, 'app1/login.html', {"login_form": LoginForm})
    else:
        #Nothing has been provided for username or password.
        return render(request, 'app1/login.html', {"login_form": LoginForm})
    
def user_logout(request): 
    # Log out the user. 
    logout(request)
    # Return to homepage. 
    return redirect("/")

def afford (request):
    return render (request, 'app1/Afford.html')

def result(request):
    return render (request, 'app1/result.html')


def calculate_affordability(request):
    if request.method == 'POST':
        # Get the form data from the request
        monthly_income = float(request.POST.get('monthly_income'))
        monthly_expenses = float(request.POST.get('monthly_expenses'))
        cost_of_purchase = float(request.POST.get('cost_of_purchase'))

        # Calculate affordability
        affordability = monthly_income - monthly_expenses - cost_of_purchase
        
        # Calculate dispoable_income
        disposable_income = monthly_income -  monthly_expenses


        # Create a dictionary of data to pass to the template
        context = {
            'monthly_income': monthly_income,
            'monthly_expenses': monthly_expenses,
            'cost_of_purchase': cost_of_purchase,
            'affordability': affordability,
            'disposable_income': disposable_income,
            'can_afford': affordability >= 0
        }

        # Render the template with the data
        return render(request, 'app1/result.html', context)

@login_required
def addDebt(request):
    if(request.method == "POST"):
        add_form = debtForm(request.POST)
        if(add_form.is_valid()):
            currBalance = add_form.cleaned_data["currBalance"]
            minimumPayment = add_form.cleaned_data["minimumPayment"]
            TotalBalance = add_form.cleaned_data["TotalBalance"]
            Name = add_form.cleaned_data["Name"]
            AprRate = add_form.cleaned_data["AprRate"]
            transactionDate = add_form.cleaned_data["transactionDate"]

            user = User.objects.get(id=request.user.id)

            Debtentry(user=user, currBalance = currBalance,minimumPayment = minimumPayment, TotalBalance=TotalBalance, Name=Name,AprRate=AprRate,transactionDate=transactionDate).save()
            return redirect("/")
        else:
            context={
                "form_data": add_form
            }
    else:
        context = {
            "form_data":debtForm()
        }
        return render(request,'app1/addDebtform.html',context)
    return render(request,'app1/addDebtform.html',context)

@login_required(login_url ='/login/')
def edit(request,id):
    if(request.method == "GET"):
        debtentry = Debtentry.objects.get(id=id)
        form = debtForm(instance = debtentry)
        context={"form_data":form}
        return render(request,'app1/editDebt.html',context)
    elif(request.method == "POST"):
        if("edit" in request.POST):
            form = debtForm(request.POST)
            if(form.is_valid()):
                debtentry = form.save(commit=False)
                debtentry.user = request.user
                debtentry.id =id
                debtentry.save()
                return redirect("/home/")
            else:
                context = {
                    "form_data":form
                }
                return render(request,'app1/home.html',context)

        else:
            return redirect("/home/")