from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from addTransaction.models import expenseCategory, expenseEntry
from addTransaction.forms import expenseEntryForm
# Create your views here.



@login_required(login_url ='/login/')
def edit(request,id):
    if(request.method == "GET"):
        expenseentry = expenseEntry.objects.get(id=id)
        form = expenseEntryForm(instance = expenseentry)
        context={"form_data":form}
        return render(request,'addTransaction/edit.html',context)
    elif(request.method == "POST"):
        if("edit" in request.POST):
            form = expenseEntryForm(request.POST)
            if(form.is_valid()):
                expenseentry = form.save(commit=False)
                expenseentry.user = request.user
                expenseentry.id =id
                expenseentry.save()
                return redirect("/transaction/")
            else:
                context = {
                    "form_data":form
                }
                return render(request,'transaction/add.html',context)

        else:
            return redirect("/transaction/")


@login_required(login_url ='/login/')
def transactions(request):
    if(request.method == "GET" and "delete" in request.GET):
        id= request.GET["delete"]
        expenseEntry.objects.filter(id=id).delete()
        return redirect("/transaction/")
    else:
        table_data = expenseEntry.objects.filter(user=request.user).order_by('-transactionDate')
        context={
            "table_data":table_data
        }
    return render(request,'addTransaction/view.html',context)

@login_required(login_url ='/login/')
def add(request):
    if(expenseCategory.objects.count() == 0):
                expenseCategory(category="Bills & Utilites").save()
                expenseCategory(category="Food & Drink").save()
                expenseCategory(category="Cash out").save()
                expenseCategory(category="Gas").save()
                expenseCategory(category="Shopping").save()
                expenseCategory(category="Personal").save()
                expenseCategory(category="Entertainment").save()
                expenseCategory(category="Other").save()
    if(request.method == "POST"):
        if("add" in request.POST):
            add_form= expenseEntryForm(request.POST)
            if(add_form.is_valid()):
                transactionAmount = add_form.cleaned_data["transactionAmount"]
                description = add_form.cleaned_data["description"]
                category = add_form.cleaned_data["category"]
                transactionDate = add_form.cleaned_data["transactionDate"]
                user = User.objects.get(id=request.user.id)

                expenseEntry(user=user, transactionAmount = transactionAmount, description=description, category=category,transactionDate=transactionDate).save()
                return redirect("/transaction/")
            else:
                context={
                    "form_data":add_form
                }
                return render(request,'addTransaction/add.html',context)
        else:
            return redirect("/transaction/")
    else:
        context = {
            "form_data":expenseEntryForm()
        }
        return render(request,'addTransaction/add.html',context)
