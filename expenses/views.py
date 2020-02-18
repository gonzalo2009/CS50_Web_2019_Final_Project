from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Expense_Type, Expense, Date
from django.db.models import Sum, Count
from datetime import timedelta, date, datetime
from django.db.models.functions import TruncDay, TruncYear, TruncWeek, TruncMonth, TruncQuarter, ExtractDay, ExtractWeek, ExtractMonth,ExtractYear
from django.utils import timezone
import pytz
import numpy as np
from sklearn.linear_model import LinearRegression
import random


date1 = timezone.now() - timezone.timedelta(days = 49)
start = datetime(year = date1.year, month = date1.month, day = date1.day).strftime("%Y-%m-%d")
date2 = timezone.now()
end = datetime(year = date2.year, month = date2.month, day = date2.day).strftime("%Y-%m-%d")


# Create your views here.


def home_view(request):
    if not request.user.is_authenticated:
        return render(request, "expenses/login.html")
    context = {
        "start": start, "end": end
    }
    return render(request, "expenses/home.html", context)


def forecast_view(request):
    if not request.user.is_authenticated:
        return render(request, "expenses/login.html")
    context = {
        "start": start, "end": end
    }
    return render(request, "expenses/forecast.html", context)



def expenses_view(request):
    if not request.user.is_authenticated:
        return render(request, "expenses/login.html")

    message = None
    expense_types = request.user.expense_types.all()
        
    if request.POST:
        if request.POST["form"] == "expense_type":
            if not request.POST["expense_type"]:
                message = "To add a new expense type, be sure to specify the name."

            else:
                for i in expense_types:
                    if str(i) == str(request.POST["expense_type"]):
                        message = "that expense type has already been added."

            if message is None:
                expense_type = Expense_Type(name = request.POST["expense_type"], user = request.user)
                expense_type.save()
            
        elif request.POST["form"] == "expense":
            if not request.POST["expense_id"] or not request.POST["amount"]:
                message = "To add a new expense, be sure to select the expense type and specify the amount."
               
            if message is None:
                expense_type = Expense_Type.objects.get(pk=request.POST["expense_id"])
                expense = Expense(expense_type = expense_type, user = request.user, amount = request.POST["amount"])
                expense.save()

        elif request.POST["form"] == "delete_expense_type":
            if not request.POST["expense_type_id"]:
                message = "To delete an expense, be sure to select it from the drop-down list."
               
            if message is None:
                Expense_Type.objects.get(pk=request.POST["expense_type_id"]).delete()
                

    expense_types = request.user.expense_types.all()
    expenses = request.user.expenses.all().order_by('-date')

    context = {
        "expense_types": expense_types, "expenses": expenses,"message": message
    }
    return render(request, "expenses/data.html", context)

def forecast_data(x, y, x_pred):
  
    

    x = list(map(lambda i: datetime.strptime(i, "%Y-%m-%d").toordinal(), x))

   
    x = np.array(x).reshape((-1, 1))
    y = np.array(y)

    model = LinearRegression().fit(x, y)

    r_sq = model.score(x, y)
   
    x_pred = list(map(lambda i: datetime.strptime(i, "%Y-%m-%d").toordinal(), x_pred))
    x_pred = np.array(x_pred).reshape((-1, 1))
    y_pred = model.predict(x_pred)
    y_pred = list(map(lambda i: round(i, 4), y_pred))

    return y_pred, r_sq 

def get_data_view(request):
    try:
        datetime.strptime(request.POST["start"], "%Y-%m-%d")
    except ValueError:
         return JsonResponse({"error": "The start date is not valid."})
    
    try:
        datetime.strptime(request.POST["end"], "%Y-%m-%d")
    except ValueError:
        return JsonResponse({"error": "The end date is not valid."})

    start = datetime.strptime(request.POST["start"], "%Y-%m-%d")
    end = datetime.strptime(request.POST["end"], "%Y-%m-%d")
    
    date_list = list(Date.objects.filter(date__range=[start, end]).annotate(range = TruncDay("date")).values("range").annotate(
        count = Count("id")).order_by("range"))

    detail_list = request.user.expenses.filter(date__range=[start, end]).annotate(range = TruncDay("date")).values(
        "range").annotate(count = Count("id")).annotate(amount_sum = Sum("amount")).order_by("range")

    x = Date.objects.filter(date__range=[start, timezone.now()]).annotate(range = TruncDay("date")).values("range").annotate(
        count = Count("id")).order_by("range")

    x = list(map(lambda i: i["range"].strftime("%Y-%m-%d"), x))

    chart1_data1 = []
    j = 0
    for i in range(len(date_list)):
        if date_list[i]["range"] > timezone.now():
            break
        if j <= len(detail_list) - 1 and detail_list[j]["range"] ==  date_list[i]["range"]:
            chart1_data1.append(detail_list[j]["amount_sum"])
            j+=1
        else:
            chart1_data1.append(0) 

    date_list_labels = list(map(lambda i: i["range"].strftime("%Y-%m-%d") ,date_list))

    chart1 = {}
    chart1["type"] = "line"
    chart1["data"]  =  {
                "labels": date_list_labels,
                "datasets": [{
                    "label": "Sum Amount dy Date",
                    "backgroundColor": "rgba(0, 73, 153)",
                    "borderColor": "rgba(0, 73, 153)",
                    "data": chart1_data1,
                    "pointRadius" : 0,
                    "fill": "false",
                    "lineTension": 0,
                }]
            }

    chart1["options"] = {
        "scales": {
            "xAxes": [{
                "type": "time",
                "ticks": {
                     "maxTicksLimit": 15
                }
            }],
            "yAxes": [{
                "ticks": {
                    "min": 0
                }
            }]
        }
    }

    chart3 = {}
    chart3["type"] = "line"
    chart3["data"]  =  {
                "labels": date_list_labels,
                "datasets": [{
                    "label": "Sum Amount dy Date",
                    "backgroundColor": "rgba(0, 73, 153)",
                    "borderColor": "rgba(0, 73, 153)",
                    "data": chart1_data1,
                    "pointRadius" : 0,
                    "fill": "false",
                    "lineTension": 0,
                    "borderWidth": 1 
                }]
            }

    chart3["options"] = {
        "legend": {
            "labels": {
                "fontSize": 10
            }
        },
        "scales": {
            "xAxes": [{
                "type": "time",
                
                "ticks": {
                    "fontSize": 10,
                     "maxTicksLimit": 10
                }
            }],
            "yAxes": [{
                "ticks": {
                    "fontSize": 10,
                    "maxTicksLimit": 8,
                    "min": 0
                }
            }]
        }
    }

    chart2 = {}
    chart4 = {}
    if request.POST["page"] == "Home":
        group_type_expense = request.user.expenses.filter(date__range = [start, end]).values("expense_type").annotate(
        count = Count("id")).annotate(amount_sum = Sum("amount")).order_by("expense_type")

        expense_type_labels = [] 
        chart2_data = []

        for i in group_type_expense:
            expense_type_labels.append(Expense_Type.objects.get(pk = i["expense_type"]).name)
            chart2_data.append(i["amount_sum"])

        expense_type_labels = list(map(lambda i: Expense_Type.objects.get(pk = i["expense_type"]).name, group_type_expense))
        chart2_data = list(map(lambda i: i["amount_sum"], group_type_expense))

        chart2["type"] = "bar"
        chart2["data"]  =  {
                    "labels": expense_type_labels,
                    "datasets": [{
                        "label": "Sum Amount by Expense Type",
                        "backgroundColor": "rgba(70, 255, 255)",
                        "borderColor": "rgba(70, 255, 255)",
                        "data": chart2_data,
                        "fill": "false"
                    }]
                }

        chart4["type"] = "bar"
        chart4["data"]  =  {
                    "labels": expense_type_labels,
                    "datasets": [{
                        "label": "Sum Amount by Expense Type",
                        "backgroundColor": "rgba(70, 255, 255)",
                        "borderColor": "rgba(70, 255, 255)",
                        "data": chart2_data,
                        "fill": "false",
                        "borderWidth": 1 
                    }]
                }

        chart4["options"] = {
            "legend": {
                "labels": {
                    "fontSize": 10
                }
            },
            "scales": {
                "xAxes": [{
                    "ticks": {
                        "fontSize": 10
                    }
                }],
                "yAxes": [{
                    "ticks": {
                        "fontSize": 10,
                        "maxTicksLimit": 8,
                        "min": 0
                    }
                }]
            }
        }    

    l = None
    if request.POST["page"] == "Forecast":
        y_pred, r_sq = forecast_data(x, chart1_data1, date_list_labels)

        chart1["data"]["datasets"].append({
            "label": "linear regression",
            "backgroundColor": "rgba(153, 255, 51)",
            "borderColor": "rgba(153, 255, 51)",
            "data": y_pred,
            "pointRadius" : 0,
            "fill": "false"
        })

        chart3["data"]["datasets"].append({
            "label": "linear regression",
            "backgroundColor": "rgba(153, 255, 51)",
            "borderColor": "rgba(153, 255, 51)",
            "data": y_pred,
            "pointRadius" : 0,
            "fill": "false",
            "borderWidth": 1 
        })

        l = round(r_sq, 8)

    charts = [chart1, chart2, chart3, chart4]
    detail = {"charts": charts}
    if l:
        detail["r_sq"] = l
    return JsonResponse(detail)


def delete_expense_view(request, expense_id):
    expense = Expense.objects.get(pk=expense_id)
    expense.delete()
    return HttpResponse('')

def login_view(request):
    context = None
    if request.POST:
        empty_fields = []

        for x in dict(request.POST).keys():
            if not request.POST[x]:
                empty_fields.append(x)

        if len(empty_fields) > 0:
            context = {"message": "Complete all the fields"}
                       
        else:
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is None:
                context = {"message": "Username or password are incorrect."}

        if context is None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))

    return render(request, "expenses/login.html", context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register_view(request):
    context = None
    if request.POST:
        empty_fields=[]

        for x  in dict(request.POST).keys():
            if not request.POST[x]:
                empty_fields.append(x)

        if len(empty_fields)>0:
            context = {"message": "Complete all the fields."}

        elif User.objects.filter(email=request.POST["email"]).exists():
            context = {"message": "The email already exists."}

        elif User.objects.filter(username =  request.POST["username"]).exists():
            context = {"message": "The username already exists."}
            
        elif request.POST["password"] != request.POST["password_confirmation"]:
            context = {"message": "Passwords do not match."}
           
        if context is None:
            username = request.POST["username"]
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            password = request.POST["password"]
            user = User.objects.create_user(username = username, first_name = first_name, last_name = last_name, email = email, password = password)
            login(request, user)
            return HttpResponseRedirect(reverse("home"))  
    return render(request, "expenses/register.html", context)






