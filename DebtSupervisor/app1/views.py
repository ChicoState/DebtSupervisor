from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from app1.forms import JoinForm, LoginForm,debtForm
from app1.models import Debtentry,debt_Strategies
from django.contrib.auth.models import User
from math import ceil
import datetime
from dateutil.relativedelta import *
from app1.models import UserProfile
from app1.forms import UserProfileForm
from app1.forms import Affordability

# Create your views here.
@login_required(login_url='/login/')
def home (request):

    if request.user.is_authenticated:
        if Debtentry.objects.filter(user=request.user).count() > 0:
            table_data = Debtentry.objects.filter(user=request.user).order_by('-dueDate')
            debt_summary = Debtentry.objects.filter(user=request.user).values('type').annotate(total_curr_balance=Sum('currBalance'))
            card_balance = 0
            total_balance = 0
            credit_limit = 0
            # variables needed for the donut
            credit_card = 0
            auto_loan = 0
            personal_loan = 0
            student_loan = 0
            morgage_loan = 0
            medical_loan = 0
            taxes = 0
            other = 0
            debt_category = []
            label_category = []
            data = list(debt_summary)

            for items in table_data:
                if items.type == Debtentry.CREDIT_CARD:
                    credit_card += items.currBalance
                    debt_category.append(credit_card)
                    label_category.append("Credit Card")
                elif items.type == Debtentry.AUTO_LOAN:
                    auto_loan += items.currBalance
                    debt_category.append(auto_loan)
                    label_category.append("Auto Loan")
                elif items.type == Debtentry.PERSONAL_LOAN:
                    personal_loan += items.currBalance
                    debt_category.append(personal_loan)
                    label_category.append("Personal Loan")
                elif items.type == Debtentry.STUDENT_LOAN:
                    student_loan += items.currBalance
                    debt_category.append(student_loan)
                    label_category.append("Student Loan")
                elif items.type == Debtentry.MORTGAGE:
                    morgage_loan += items.currBalance
                    debt_category.append(morgage_loan)
                    label_category.append("Morgage")
                elif items.type == Debtentry.MEDICAL_LOAN:
                    medical_loan += items.currBalance
                    debt_category.append(medical_loan)
                    label_category.append("Medical Loan")
                elif items.type == Debtentry.TAXES:
                    taxes += Debtentry.currBalance
                    debt_category.append(taxes)
                    label_category.append("Taxes")
                elif items.type == Debtentry.OTHER:
                    other += Debtentry.currBalance
                    debt_category.append(other)
                    label_category.append("Other")


            #checks if due date is passed
            for items in table_data:
                if items.dueDate < datetime.date.today():
                    items.dueDate = items.dueDate+relativedelta(months=+1)
                    items.save()
                    
            for items in table_data:
                if items.type == Debtentry.CREDIT_CARD:
                    credit_limit += items.TotalBalance
                    card_balance += items.currBalance  
                total_balance += items.currBalance + total_balance
            cru = (card_balance/credit_limit)
            
            context={
                "table_data":table_data,
                "total_balance":total_balance,
                "credit_limit": credit_limit,
                "card_balance":card_balance,
                "cru":cru,
                "label_category":label_category,
                "debt_category":debt_category,
                "data":data
            }
    
            return render (request, 'app1/home.html',context)
        else:
            return render (request, 'app1/home.html')

    else:
        return render (request, 'app1/home.html')

@login_required(login_url='/login/')
def updateProfilePic(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # create a new UserProfile object for the user if one doesn't exist yet
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = UserProfileForm(instance=user_profile)
    context = {
        'form': form,
    }
    return render(request, 'app1/updateProfilePic.html', context)

@login_required(login_url='/login/')
def addDebt(request):
    if(request.method == "POST"):
        add_form = debtForm(request.POST)
        if(add_form.is_valid()):
            user = User.objects.get(id=request.user.id)
            type = add_form.cleaned_data["type"]
            name = add_form.cleaned_data["name"]
            currBalance = add_form.cleaned_data["currBalance"]
            TotalBalance = add_form.cleaned_data["TotalBalance"]
            apr = add_form.cleaned_data["apr"]
            minPayment = add_form.cleaned_data["minPayment"]
            dueDate = add_form.cleaned_data["dueDate"]

            Debtentry(user=user, type=type, name=name, currBalance=currBalance, TotalBalance=TotalBalance, apr=apr, minPayment=minPayment, dueDate=dueDate).save()
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

@login_required(login_url='/login/')
def afford (request):
    return render (request, 'app1/Afford.html')

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
            '''return render(login_url='/login/')(request, 'app1/join.html', page_data)'''
            return render(request, 'app1/join.html', page_data)
    else:
        join_form = JoinForm()
        ##join_form.fields["username"].help_text = ""
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

def result(request):
    return render (request, 'app1/result.html')

def my_view(request):
    if request.method == 'POST':
        form = Affordability(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        form = Affordability()
    return render(request, 'app1/Afford.html', {'form': form})

def calculate_affordability(request):
    if request.method == 'POST':
        form = Affordability(request.POST)
        if form.is_valid():
            # Get the form data from the request
            monthly_income = float(request.POST.get('monthly_income'))
            monthly_expenses = float(request.POST.get('monthly_expenses'))
            cost_of_purchase = float(request.POST.get('cost_of_purchase'))
            monthly_savings = float(request.POST.get('monthly_savings'))

            # Calculate affordability
            affordability = monthly_income - monthly_expenses - cost_of_purchase - monthly_savings

            # Calculate dispoable_income
            disposable_income = monthly_income -  monthly_expenses - monthly_savings

            # (NEW!) calculate the expenses percentage and savings percentage
            expenses_percentage = monthly_expenses / monthly_income * 100
            savings_percentage = monthly_savings / monthly_income * 100

            #Check conditions if they can afford something
            high_expenses = expenses_percentage > 50
            low_savings = savings_percentage < 20
            cost_too_high = cost_of_purchase > 0.3 * monthly_income

            #Caluclate the savings on needs to pay the cost of purchase within 6 months
            saving_per_month = cost_of_purchase / 6
            savings_per_month = cost_of_purchase / 12


            # Create a dictionary of data to pass to the template
            context = {
                'monthly_income': monthly_income,
                'monthly_expenses': monthly_expenses,
                'monthly_savings': monthly_savings,
                'cost_of_purchase': cost_of_purchase,
                'affordability': affordability,
                'disposable_income': disposable_income,
                'can_afford': affordability >= 0,
                'expenses_percentage': expenses_percentage,
                'savings_percentage': savings_percentage,
                'high_expenses': high_expenses,
                'low_savings': low_savings,
                'cost_too_high': cost_too_high,
                'saving_per_month': saving_per_month,
                'savings_per_month': savings_per_month,
            }

            # Render the template with the data
            return render(request, 'app1/result.html', context)
        else:
            return render(request, 'app1/afford.html', {'form': form})

@login_required(login_url ='/login/')
def edit(request,id):
    if(request.method == "GET"):
        debtentry = Debtentry.objects.get(id=id)
        name = debtentry.name
        form = debtForm(instance = debtentry)
        context={"form_data":form,
                 "name":name,}
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




def debtStrageties(request):
    if debt_Strategies.objects.count() <= 0:
        snowflake = debt_Strategies.objects.create(name="Snowball Method", description="Pay off the smallest debt first, then use the money you would have used to pay off the smallest debt to pay off the next smallest debt, and so on.", url="https://www.debt.org/advice/debt-snowball-method-how-it-works/")
        avalanche = debt_Strategies.objects.create(name="Avalanche Method", description="Prioritize and pay off high-interest debt first, then use the freed-up funds to pay off other debts in descending order of interest rates.", url="https://www.debt.org/advice/debt-avalanche/")
        consolidation = debt_Strategies.objects.create(name="Debt Consolidation", description="Learn more ways to pay off debts", url="https://www.debt.org/consolidation/")

        snowflake.save()
        avalanche.save()
        consolidation.save()

    
    context = {
        "strategies": debt_Strategies.objects.all()
    }

    return render(request, 'app1/debtStrageties.html', context)


