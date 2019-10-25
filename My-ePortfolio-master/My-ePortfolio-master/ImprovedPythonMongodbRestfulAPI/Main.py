#!/usr/bin/python
import pymongo
from pymongo import MongoClient
from bson import json_util
import json
import bson
from bson import json_util
import datetime
import bottle
from bottle import route, run, request, abort, post
import pprint

#=========================PREDEFINED DOCUMENTS=====================================#
myDocument ={ "Ticker":"BALI", "Profit Margin" : 0.060, "Institutional Ownership" : 0.66 , "EPS growth past 5 years" : 0.094, "Total Debt/Equity": 0.90, "Current Ratio" : 0.9, "Return on Asset   s": 0.029, "sector" : "Inventory", "P/S" : 1.49, "Change from Open" : 0.005, "Performace (YTD)" : 0.0950, "Performance (Week)": -0.0310, "Quick Ratio" : 0.7, "Insider Transactions": 0.0335, "P/B" : 3.18, "EPS growth quarter over quarter" : 0.153, "Payout Ratio" : 1.369, "Performance (Quarter)": 0.0355, "Forward P/E" : 13.15, "P/E" : 25.90, "200-Day Simple Moving Average" : 0.0077, "Shares Outstanding" : 5519, "Earnings Date" : ("ISOdate:" "2018-05-31T25:39:00Z"), "52-Week High" : -0.0869, "P/Cash" : 165.98, "Change" : 0.005, "Analyst Recom" : 3.9, "Volatility (Week)" : 0.0245, "Country" : "USA", "Return on Equity" : 0.095, "50-Day Low" : 0.0819, "Price" : 45.16, "50-Day High" : -0.0551, "Return on Investment" : 0.072, "Shares Float" : 6353.61, "Dividend Yield" : 0.0615, "EPS growth next 5 years" : 0.0759, "Industry" : "Computer Sales Inventory - Domestic", "Beta" : 0.62, "Sales growth quarter over quarter": 0.033, "Operating Margin" : 0.204, "EPS (ttm)" : 1.51, "PEG" : 3.95, "Float Short" : 0.0342, "52-Week Low" : 0.1402, "Average True Range" : 0.62, "EPS growth next year" : 0.0908, "Sales growth past 5 years" : 0.024, "Company" : "Bestbuy", "Gap" : 0, "Relative Volume" : 0.49, "Volatility (Month)" : 0.0148, "Market Cap" : 196498.10, "Volume" : 9599690, "Gross Margin" : 0.59, "Short Ratio" : 5.33, "Performance (Half Year)" : -0.0472, "Relative Strength Index (14)" : 51.61, "Insider Ownership" : 0.0005, "20-Day Simple Moving Average" : -0.009, "P/Free Cash Flow" : 40.36, "Institutional Transactions" : -0.007, "Performance (Year)" : 0.0968, "LT Debt/Equity" : 0.9, "Average Volume" : 25427.90, "EPS growth this year" : 0.899, "50-Day Simple Moving Average" : 0.0317}

myDocument2 ={"Ticker" : "A", "Profit Margin" : 0.137, "Institutional Ownership" : 0.847, "EPS growth past 5 years" : 0.158, "Total Debt/Equity" : 0.56, "Current Ratio" : 3,
"Return on Assets" : 0.089, "Sector" : "Healthcare", "P/S" : 2.54, "Change from Open" : -0.0148, "Performance (YTD)" : 0.2605, "Performance (Week)" : 0.0031, "Quick Ratio" : 2.3, "Insider Transactions" : -0.1352, "P/B" : 3.63, "EPS growth quarter over quarter" : -0.29, "Payout Ratio" : 0.162, "Performance (Quarter)" : 0.0928, "Forward P/E" : 16.11,
"P/E" : 19.1, "200-Day Simple Moving Average" : 0.1062, "Shares Outstanding" : 339, "Earnings Date" : ("ISOdate:" "2013-11-14T21:30:00Z"), "52-Week High" : -0.0544, "P/Cash" : 7.45,"Change" : -0.0148, "Analyst Recom" : 1.6, "Volatility (Week)" : 0.0177, "Country" : "USA", "Return on Equity" : 0.182, "50-Day Low" : 0.0728, "Price" : 50.44, "50-Day High" : -0.0544, "Return on Investment" : 0.163, "Shares Float" : 330.21, "Dividend Yield" : 0.0094, "EPS growth next 5 years" : 0.0843, "Industry" : "Medical Laboratories & Research",
"Beta" : 1.5, "Sales growth quarter over quarter" : -0.041, "Operating Margin" : 0.187, "EPS (ttm)" : 2.68, "PEG" : 2.27, "Float Short" : 0.008, "52-Week Low" : 0.4378, "Average True Range" : 0.86, "EPS growth next year" : 0.1194, "Sales growth past 5 years" : 0.048, "Company" : "Agilent Technologies Inc.", "Gap" : 0, "Relative Volume" : 0.79, "Volatility (Month)" : 0.0168, "Market Cap" : 17356.8, "Volume" : 1847978, "Gross Margin" : 0.512, "Short Ratio" : 1.03, "Performance (Half Year)" : 0.1439, "Relative Strength Index (14)" : 46.51, "Insider Ownership" : 0.001, "20-Day Simple Moving Average" : -0.0172, "Performance (Month)" : 0.0063, "P/Free Cash Flow" : 19.63, "Institutional #Transactions" : -0.0074,
"Performance (Year)" : 0.4242, "LT Debt/Equity" : 0.56, "Average Volume" : 2569.36, "EPS growth this year" : 0.147, "50-Day Simple Moving Average" : -0.0055}

myDocument3 = { "Ticker" : "BRLI", "Profit Margin" : 0.081, "Institutional Ownership" : 0.957, "EPS growth past 5 years" : 0.247, "Total Debt/Equity" : 0.14, "Current Ratio" : 2.6, "Return on Assets" : 0.164, "Sector" : "Healthcare", "P/S" : 1.42, "Change from Open" : -0.0128, "Performance (YTD)" : 0.2553, "Performance (Week)" : 0.0825, "Quick Ratio" : 2.4, "Insider Transactions" : -0.077, "P/B" : 3.82, "EPS growth quarter over quarter" : 0.178, "Payout Ratio" : 0, "Performance (Quarter)" : 0.3238, "Forward P/E" : 17.32, "P/E" : 21.02, "200-Day Simple Moving Average" : 0.2557, "Shares Outstanding" : 27.67, "Earnings Date" : ("ISODate" "2013-12-02T05:00:00Z"), "52-Week High" : -0.0167, "P/Cash" : 34.77, "Change" : -0.0156, "Analyst Recom" : 2.2, "Volatility (Week)" : 0.0307, "Country" : "USA"}

myDocument4 ={ "Ticker":"YODIA", "Profit Margin" : 0.060, "Institutional Ownership" : 0.66 , "EPS growth past 5 years" : 0.094, "Total Debt/Equity": 0.90, "Current Ratio" : 0.9, "Return on Asset   s": 0.029, "sector" : "Inventory", "P/S" : 1.49, "Change from Open" : 0.005, "Performace (YTD)" : 0.0950, "Performance (Week)": -0.0310, "Quick Ratio" : 0.7, "Insider Transactions": 0.0335, "P/B" : 3.18, "EPS growth quarter over quarter" : 0.153, "Payout Ratio" : 1.369, "Performance (Quarter)": 0.0355, "Forward P/E" : 13.15, "P/E" : 25.90, "200-Day Simple Moving Average" : 0.0077, "Shares Outstanding" : 5519, "Earnings Date" : ("ISOdate:" "2018-05-31T25:39:00Z"), "52-Week High" : -0.0869, "P/Cash" : 165.98, "Change" : 0.005, "Analyst Recom" : 3.9, "Volatility (Week)" : 0.0245, "Country" : "USA", "Return on Equity" : 0.095, "50-Day Low" : 0.0819, "Price" : 45.16, "50-Day High" : -0.0551, "Return on Investment" : 0.072, "Shares Float" : 6353.61, "Dividend Yield" : 0.0615, "EPS growth next 5 years" : 0.0759, "Industry" : "Computer Sales Inventory - Domestic", "Beta" : 0.62, "Sales growth quarter over quarter": 0.033, "Operating Margin" : 0.204, "EPS (ttm)" : 1.51, "PEG" : 3.95, "Float Short" : 0.0342, "52-Week Low" : 0.1402, "Average True Range" : 0.62, "EPS growth next year" : 0.0908, "Sales growth past 5 years" : 0.024, "Company" : "Star Wars Ent.", "Gap" : 0, "Relative Volume" : 0.49, "Volatility (Month)" : 0.0148, "Market Cap" : 196498.10, "Volume" : 9599690, "Gross Margin" : 0.59, "Short Ratio" : 5.33, "Performance (Half Year)" : -0.0472, "Relative Strength Index (14)" : 51.61, "Insider Ownership" : 0.0005, "20-Day Simple Moving Average" : -0.009, "P/Free Cash Flow" : 40.36, "Institutional Transactions" : -0.007, "Performance (Year)" : 0.0968, "LT Debt/Equity" : 0.9, "Average Volume" : 25427.90, "EPS growth this year" : 0.899, "50-Day Simple Moving Average" : 0.0317}

myDocument5 ={ "Ticker":"DUNDRM", "Profit Margin" : 0.060, "Institutional Ownership" : 0.66 , "EPS growth past 5 years" : 0.094, "Total Debt/Equity": 0.90, "Current Ratio" : 0.9, "Return on Asset   s": 0.029, "sector" : "Inventory", "P/S" : 1.49, "Change from Open" : 0.005, "Performace (YTD)" : 0.0950, "Performance (Week)": -0.0310, "Quick Ratio" : 0.7, "Insider Transactions": 0.0335, "P/B" : 3.18, "EPS growth quarter over quarter" : 0.153, "Payout Ratio" : 1.369, "Performance (Quarter)": 0.0355, "Forward P/E" : 13.15, "P/E" : 25.90, "200-Day Simple Moving Average" : 0.0077, "Shares Outstanding" : 5519, "Earnings Date" : ("ISOdate:" "2018-05-31T25:39:00Z"), "52-Week High" : -0.0869, "P/Cash" : 165.98, "Change" : 0.005, "Analyst Recom" : 3.9, "Volatility (Week)" : 0.0245, "Country" : "USA", "Return on Equity" : 0.095, "50-Day Low" : 0.0819, "Price" : 45.16, "50-Day High" : -0.0551, "Return on Investment" : 0.072, "Shares Float" : 6353.61, "Dividend Yield" : 0.0615, "EPS growth next 5 years" : 0.0759, "Industry" : "Computer Sales Inventory - Domestic", "Beta" : 0.62, "Sales growth quarter over quarter": 0.033, "Operating Margin" : 0.204, "EPS (ttm)" : 1.51, "PEG" : 3.95, "Float Short" : 0.0342, "52-Week Low" : 0.1402, "Average True Range" : 0.62, "EPS growth next year" : 0.0908, "Sales growth past 5 years" : 0.024, "Company" : "Dunder Mifflin", "Gap" : 0, "Relative Volume" : 0.49, "Volatility (Month)" : 0.0148, "Market Cap" : 196498.10, "Volume" : 9599690, "Gross Margin" : 0.59, "Short Ratio" : 5.33, "Performance (Half Year)" : -0.0472, "Relative Strength Index (14)" : 51.61, "Insider Ownership" : 0.0005, "20-Day Simple Moving Average" : -0.009, "P/Free Cash Flow" : 40.36, "Institutional Transactions" : -0.007, "Performance (Year)" : 0.0968, "LT Debt/Equity" : 0.9, "Average Volume" : 25427.90, "EPS growth this year" : 0.899, "50-Day Simple Moving Average" : 0.0317}

myDocument6 ={ "Ticker":"STUSWAP", "Profit Margin" : 0.060, "Institutional Ownership" : 0.66 , "EPS growth past 5 years" : 0.094, "Total Debt/Equity": 0.90, "Current Ratio" : 0.9, "Return on Asset   s": 0.029, "sector" : "Inventory", "P/S" : 1.49, "Change from Open" : 0.005, "Performace (YTD)" : 0.0950, "Performance (Week)": -0.0310, "Quick Ratio" : 0.7, "Insider Transactions": 0.0335, "P/B" : 3.18, "EPS growth quarter over quarter" : 0.153, "Payout Ratio" : 1.369, "Performance (Quarter)": 0.0355, "Forward P/E" : 13.15, "P/E" : 25.90, "200-Day Simple Moving Average" : 0.0077, "Shares Outstanding" : 5519, "Earnings Date" : ("ISOdate:" "2018-05-31T25:39:00Z"), "52-Week High" : -0.0869, "P/Cash" : 165.98, "Change" : 0.005, "Analyst Recom" : 3.9, "Volatility (Week)" : 0.0245, "Country" : "USA", "Return on Equity" : 0.095, "50-Day Low" : 0.0819, "Price" : 45.16, "50-Day High" : -0.0551, "Return on Investment" : 0.072, "Shares Float" : 6353.61, "Dividend Yield" : 0.0615, "EPS growth next 5 years" : 0.0759, "Industry" : "Computer Software", "Beta" : 0.62, "Sales growth quarter over quarter": 0.033, "Operating Margin" : 0.204, "EPS (ttm)" : 1.51, "PEG" : 3.95, "Float Short" : 0.0342, "52-Week Low" : 0.1402, "Average True Range" : 0.62, "EPS growth next year" : 0.0908, "Sales growth past 5 years" : 0.024, "Company" : "Study Swap", "Gap" : 0, "Relative Volume" : 0.49, "Volatility (Month)" : 0.0148, "Market Cap" : 9996498.10, "Volume" : 999599690, "Gross Margin" : 0.59, "Short Ratio" : 5.33, "Performance (Half Year)" : -0.0472, "Relative Strength Index (14)" : 51.61, "Insider Ownership" : 0.0005, "20-Day Simple Moving Average" : -0.009, "P/Free Cash Flow" : 40.36, "Institutional Transactions" : -0.007, "Performance (Year)" : 0.0968, "LT Debt/Equity" : 0.9, "Average Volume" : 9995427.90, "EPS growth this year" : 0.899, "50-Day Simple Moving Average" : 0.0317}
#=========================PREDEFINED DOCUMENTS=====================================#

#----------BEGIN AUTHENTICATION-----------#
#Getting the username to after logging in to the server
def get_user(username):
    try:
        connection = pymongo.MongoClient('localhost', 27017)
        mydb =  connection["market"]
        mycol = mydb["users"]
        x = mycol.find_one({"username":username})
        if(not x):
            return False
        return x["password"]
    except:
        return False
#Signing up the username and password
def signup_user(username, password):
    try:
        connection = pymongo.MongoClient('localhost', 27017)
        mydb =  connection["market"]
        mycol = mydb["users"]
        myDocument = {"username":username, "password":password}
        x = mycol.insert_one(myDocument)
        return True
    except:
        return False
#Logging in the username and password that was just been created    
def login(username, password):
    user = get_user(username)
    if(user == False):
        print("The user does not exist")
        return False
    elif(user == password):
        return True
    else:
        print("Invalid password")
        return False
#Getting an error message stating that the user with that username already exists    
def signup(username, password):
    user = get_user(username)
    if(user == False):
        return signup_user(username, password)
    else:
        print("A user with that username already exists")
        return False
#Welcoming a new user to the database connection with a welcome screen appears   
def welcome_menu():
    r = "1. Signup\n"
    r = r + "2. Login\n"
    r = r + "3. Quit\nChoice: "
    return r
def welcome():
    result = False
    while(True):
        welcome_menu()
        choice = int(raw_input(welcome_menu()))
        if(choice == 1):
            print("signup")
            result = signup(str(raw_input("username: ")), str(raw_input("password: ")))
            if(result):
                print("Welcome!")
                break
        elif(choice == 2):
            print("login")
            result = login(str(raw_input("username: ")), str(raw_input("password: ")))
            if(result):
                print("Welcome!")
                break
        elif(choice == 3):
            print("Goodbye!")
            break
        else:
            print("Invalid menu option")
    return result

#-----------END AUTHENTICATION------------#

#a function for inserting a document into the database
def insert_document(myDocument):
  
  try:
#open a connection to the database
    connection = pymongo.MongoClient('localhost', 27017)
#open a connection to stocks table of the market db
    mydb =  connection["market"]
    mycol = mydb["stocks"]
#call the mongo insert one document function on the document.
    x = mycol.insert_one(myDocument)
    print(x)
  
  except  pymongo.errors.ValidationErrors as ve:
#if there is a connection/db runtime error abort the function.
    abort(400, str(ve))
#return the value of the inserted document
  return x
#Retriving the document 
def get_document(key,value):
    
    try:
#Repeating the steps from step one
      connection = pymongo.MongoClient('localhost', 27017)
      mydb =  connection["market"]
      mycol = mydb["stocks"]
      x = mycol.find_one({key:value})
      print(x)
  
      
    except  pymongo.errors.ValidationErrors as ve:
      print("not exited")
      abort(400, str(ve))
    return x
#Updating document from the database
def update_document(key,value,document):
  try:
    connection = pymongo.MongoClient('localhost', 27017)
    mydb = connection["market"]
    mycol = mydb["stocks"]
#Setting the updated data to the new document from the old document
    updateData = ({"$set":document})
    ud = { "Ticker" : "AM", "Volume" : 2876542, "Relative Volume": 2.79}
    x = mycol.update_one({key:value},{'$set':document})
    print(x)

  except  pymongo.errors.ValidationErrors as ve:
      abort(400, str(ve))
  return x
#Deleting the document from the database connection
def delete_document(key,value):
  try:
    connection = pymongo.MongoClient('localhost', 27017)
    mydb = connection["market"]
    mycol = mydb["stocks"]
    
    
    x = mycol.delete_one({key:value})
    print(x)
   
  except  pymongo.errors.ValidationErrors as ve:
      abort(400, str(ve))
  return x

connection = MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']


#function to find the number of documents in the low to high ranges of quick ratio values
def find_quickratio(low, high):
  query = {'50-Day Simple Moving Average': {'$lt': high, '$gt': low}}
  result = collection.find(query).count()
  return result

#Getting the industries ticker values
def get_industry(industry):
#ru a find on that industry
    result = collection.find({"Industry" : industry})
    for i in result:
#iterate over the results and print every ticker
        print(i["Ticker"])

#Getting the aggregate sector value 
def get_sector(value):
    document = collection.aggregate([{"$match": { "Sector":value }},{"$group": {"_id":"Industry" , "total":{ "$sum": "$Shares Outstanding"}}}])
    return document


#Main testing
def main():
    myUpdate = { "Volume" : 2876542, "Relative Volume": 2.79}
    insert_document(myDocument)
    get_document("Ticker","BALI")
    update_document("Ticker", "A", myUpdate)
    get_document("Ticker","AM")
    delete_document("Ticker", "BRLI")
    print(find_quickratio(1, 3))
    result = get_sector("Healthcare")
    for docs in result:
        print(docs)
    result = get_sector("Basic Materials")
    for docs in result:
        print(docs)
    print ("Not a valid data")
    
    #NEW INSERTS
    print("inserting Star Wars Ent.")
    insert_document(myDocument4)
    print("inserting Dunder Mifflin.")
    insert_document(myDocument5)
    print("inserting Study Swap.")
    insert_document(myDocument6)
      
if __name__ == "__main__":
    if(welcome()):
        main()
        ind = str(raw_input("Enter an Industry: "))
        get_industry(ind)#call the get_industry function
    else:
        print("Unable to authenticate")
