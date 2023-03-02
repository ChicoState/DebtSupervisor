from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from app1.forms import JoinForm, LoginForm


# Create your views here.
def home (request):
    return render (request, 'app1/home.html')
    return HttpResponse("Hello world!")

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