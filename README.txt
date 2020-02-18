Final Project: Finance

Overview:

This web application helps users manage their expenses. The goal is that the user can view their expenses represented in different chart, and thus have greater control 
over them, and be able to save money if they want.  

To use it you must to register. The application consists mainly of three pages: Expenses, Home and Forecast. 

On the Expenses page, you have to enter the types of expenses that you want to register and then, the next time you have a new expense(groceries for example) you have 
to register it on the web application, by assigning the expense type and the amount of it, the date and time will set automatically and corresponds to the date and time 
you recorded the expense. The registered expenses will be saved in each user's expense set. This expense set will be represented in the charts of Home and Forecast page. 

On the Home page, the first chart it is a line chart that shows the total amount that you have spent over the time(per day or month for example). The second chart it is 
a bar chart that shows the amount of money spent by expense type. To change the range of the dates of the charts, you can do it by changing the inputs dates 
above the charts. 

The Forecast page shows a graph with two lines. The blue line represents the total money spent over the time(as well as the first chart of the "Home" page) and the green 
line represents a simple linear regression, i.e., the straight line which best represents the relationship between the time variable and the amount of money spent 
variable. This chart can help you to predict how much you will spend in the future. For this you must choose a future date in the "end date" input and the green line 
will be displayed until that end date. The precision of the linear regression prediction is measured by the coefficient of determination shown above the chart. The 
coefficient of determination ranges from zero to one. The closer the value is to one, the prediction is more accurate, so you can predict if the coefficient of 
determination is close to one.


Files:

-base.html: This in the main layout of the web application.

-login.html: In this page you have to submit your username a your password to login.

-register.html: This page is to register. To register you have to complete the form that is shown.

-data.html: on this page you can register the types of expenses, by typing them in the input bar that says "add a new expense type" and then clicking on the "Add Type" 
button. To add a new expense, you have to choose the expense type in the drop-down list that says "Expense Type", then you must specify the amount of that expense in 
the input bar that says "amount" and finally click on the "Add Expense" button. Doing this you will create a new expense. If you want to delete an expense type you have 
to choose it in tho drop-down list that says "Delete an expense type" and then click on the "Delete Type" button. The table "Expense History" shows the set of expenses 
with the type, amount and date. If you want to delete an expense you have to click on the button "Delete" at the right side of it.

-home.html: This page shows the line chart and a the bar chart.

-forecast.html:  This page shows the chart with the amount of money spent over the time and the linear regression. 

-views.py: This file contains the code that runs on the server side, and interacts between the user and the database.   

models.py: contains the classes to create the objects for the database.

-scrpts.js: This is the javascipt file that runs on the browser side.

-styles.css: contains the style for html files.

-icon.png: contains the favicon of the web application. Source: https://www.netclipart.com/pp/m/47-471982_profit-png-pic-finance-icon-transparent.png
