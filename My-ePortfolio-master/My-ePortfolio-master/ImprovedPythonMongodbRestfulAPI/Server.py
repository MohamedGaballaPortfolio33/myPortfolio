#!/usr/bin/python
#begin imports
import pymongo
from pymongo import MongoClient
from bson import json_util
import json
import bson
from bson import json_util
import datetime
import bottle
from bottle import route, run, request, abort, post
#end imports

#function for formatting a document.
def format_document(myDocument):
    #this is the formatting string.
    output = ""
    #for every key value in the document
    for k in myDocument:
        #add it with it's corresponding value and a new line
        output = output + str(k) + " : " + str(myDocument[k]) + "\n"
    #return the formatted string.
    return output
    
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


# function for getting a single document with a value for a given key
def get_document(key,value):
    try:
      connection = pymongo.MongoClient('localhost', 27017)
      mydb =  connection["market"]
      mycol = mydb["stocks"]
      #just calls mongo's built in find_one function
      x = mycol.find_one({key:value})
      print(format_document(x)) 
    except  pymongo.errors.ValidationErrors as ve:
      print("not exited")
      abort(400, str(ve))
    return x

#a function for updating a document with a given ticker to be in a sector called newSector
def update_document(ticker,newSector):
  try:
    connection = pymongo.MongoClient('localhost', 27017)
    mydb = connection["market"]
    mycol = mydb["stocks"]
    #calls mongo's key value based update function
    x = mycol.update_one({"Ticker":ticker},{'$set':{"Sector" : newSector}})
    print(x)
  except  pymongo.errors.ValidationErrors as ve:
      abort(400, str(ve))
  return x

#deletes a document who has a specific value for the given key
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
    
#this is a global id function for assigning id's to users
id = 0
#MileStone Two

#defines the greeting route for the flask server
@route('/greeting', method= ['POST', 'GET'])
def get_greeting():
    #increment the global id variable
    global id
    id = id + 1
    try:
        #sets the name variable equal to the name variable from the query string
        request.query.name
        name=request.query.name
        #there was a name variable in the query string
        if name: 
          #make calls to database from here
               string="{ \"id\": "+str(id)+", \"content\": \"Hello, \""+request.query.name+"\"}"
        #there was not a name in the query string
        else:
               string="{ \"id\": "+str(id)+", \"content\": \"Hello, World!\"}"
    except NameError:
        abort(404, 'No parameter for id %s' % id)
  # set up URI paths for REST service 

#a route for getting the currentTime
@route('/currentTime', method='GET')
def get_currentTime(): 
    #gets the current date, and tthe current time and returns the jsonified text
    dateString=datetime.datetime.now().strftime("%Y-%m-%d")                      
    timeString=datetime.datetime.now().strftime("%H:%M:%S") 
    string="{\"date\":"+dateString+",\"time\":"+timeString+"}"       
    return json.loads(json.dumps(string, indent=4, default=json_util.default)) 
  
#Setting up Hello World route
@route('/hello', method='GET')
def get_hello():
    try:
        #checks if there was a name in the query string
        request.query.name
        name=request.query.name
        if name: 
          #says hello to the user
          #make calls to database from here
               string="{ hello: \""+request.query.name+"\"}"
        else:#generic message
               string="{ \"content\": \"Hello, World!\"}"
    except NameError:
        abort(404, 'No parameter for id %s' % id)
    if not string:
        abort(404, 'No id %s' % id)
    return json.loads(json.dumps(string, indent=4, default=json_util.default))
  
#a specific post only function for the flask server.
@post('/strings')
def strings():
    print("called")
    if(request.method=="POST"):
        #gets all the post paramaters and decodes it into a string
        r = request.body.read().decode()
        #uses eval to turn it into a dictionary
        r = eval(str(r))
        #if string1 is a key in this dicttionary
        if("string1" in r):
            #return this string
            string = "{ first : \""+ r["string1"]+"\", second : \"" + r["string2"]+"\"}"
            if not string:
                abort(404, 'The post failed to respond a return for the two strings')
            else:
                return json.loads(json.dumps(string, indent=4, default=json_util.default))
              
#the flask route for creating documents.
@route('/create', method='POST') 
def put_document():
    #get all the possible paramaters that accompanied the post/get requests
    print(request.body.read().strip())
    #evals it into a dictionary/document.
    myDocument = eval(request.body.read().strip())
    print(myDocument)
    if not myDocument:
        abort(400, 'There is no data recieved') 
    entity = myDocument
    if entity.get('Ticker') == None:
        abort(404, 'No such document has been found with the Ticker %s' % d["Ticker"])
    try:
        #attempts to insert that document into the database.
        insert_document(entity)
        return json.dumps("The document was inserted successful")
    except pyMongo.ValidationError as ve:
        abort(400, str(ve))
        
#route for getting a document by the company's name
@route('/read', methods=['POST', 'GET'])
def read():
    #only works with get requests
    if(request.method=="GET"):
        #replaces all % in the business name with spaces.
        newName = request.query.business_name.replace("%", " ")
        print(newName)
        #attempts to retrieve the document from the database for that company
        entity = get_document("Company", newName)
        if not entity:
           return json.dumps("Not a valid document")
        #return json.dumps(str(entity))
        #if it was able to it returns the formatted document.
        return str(format_document(entity))

#the route for updating a document
@route('/update', methods=['POST', 'GET'])
def update():
    #only works with get requests
    if(request.method=="GET"):
        #gets the ticker/sector from the query string
        print("Ticker:" + request.query.Ticker)
        print("Sector:" + request.query.Sector)
        print(request.body.read())
        #calls the update_document funciton to update the Sector of the document with that ticker in that database
        entity = update_document(request.query.Ticker,request.query.Sector)
        if not entity:
            return json.dumps("Not a valid document")
        print(entity)
        return json.dumps("The document was updated successfully") 

#route for deleting a document.
@route('/delete', methods=['POST', 'GET'])
def delete():
    #only defined for get requests
    if(request.method=="GET"):
        print(request.query.Ticker)
        #gets the ticker from the query string and deletes the document with that Ticler.
        entity = delete_document("Ticker", request.query.Ticker)
        if not entity:
            return json.dumps("Not a valid document") 
        return json.dumps("The document was successfully deleted") 
#the path for taking a list of tickers and outputting a summary
@route('/listTickers', methods=['POST', 'GET'])
def listTickers():
    if(request.method=="GET"):
        #query paramter is tickerslist
        print(request.query.tickerslist)
        tickerslist = request.query.tickerslist
        #they are seperated by commas, so split them by commas into a list
        l = tickerslist.split(",")
        #this is where all our results will be stored
        dic = {}
        #iterate over the tickers list
        for i in l:
            #if the ticker is not an empty string
            if(len(i) > 0):
                #get the document for that ticker
                #add it to our final output
                dic[i] = get_document("Ticker", i)
        #return oru final output
        return json.dumps(str(dic))
    
#this is the bestStock route
@route('/bestStock', methods=['POST', 'GET'])
def bestStock():
    if(request.method=="GET"):
        print(request.query.Industry)
        #gets the industry from the query string.
        ind = request.query.Industry
        ind = ind.replace("%", " ")
        #calls the ordered_industry function and returns the results jsonified
        results = ordered_industry(ind)
        return json.dumps(results)
    
#function for sorting a list of all the stocks of a given industry by their Volume.
def ordered_industry(industry):
    #makes a connection to the db.
    connection = pymongo.MongoClient('localhost', 27017)
    mydb =  connection["market"]
    mycol = mydb["stocks"]
    #get all the stocks from the db that have that industry
    print("Industry: " + industry)
    x = mycol.find({"Industry":industry})
    l = []
    for i in x:
        #for every document, add thte company, symbol, and volume to l.
        l.append({"Company" : i["Company"], "Symbol" : i["Ticker"], "Volume" : i["Volume"]})
    #define custom sort function for l
    def func(e):
        try:
            return e["Volume"]
        except:
            return 0
    #sort by volume
    l.sort(key=func)
    #make descending
    l.reverse()
    #return first 5 vals
    return l[0:5]

if __name__ == '__main__': #declare instance of request
  #app.run(debug=True)
  run(host='localhost', port=8080) 
    
    
#================================SAMPLE TEST CALLS==================================#


#CREATE A STOCK
#curl -H "Content-Type: application/json" -X POST -d '{"Ticker":"TARE", "Profit Margin" : 0.060, "Institutional Ownership" : 0.66 , "EPS growth past 5 years" : 0.094, "Total Debt/Equity": 0.94, "Current Ratio" : 0.10, "Return on Asset   s": 0.030, "sector" : "Technology", "P/S" : 1.49, "Change from Open" : 0.005, "Performace (YTD)" : 0.0950, "Performance (Week)": -0.0789, "Quick Ratio" : 0.4, "Insider Transactions": 0.0335, "P/B" : 3.18, "EPS growth quarter over quarter" : 0.153, "Payout Ratio" : 1.369, "Performance (Quarter)": 0.0355, "Forward P/E" : 13.15, "P/E" : 25.90, "200-Day Simple Moving Average" : 0.0079, "Shares Outstanding" : 5529, "Earnings Date" : ("ISOdate:" "2018-05-31T25:39:00Z"), "52-Week High" : -0.0870, "P/Cash" : 165.98, "Change" : 0.007, "Analyst Recom" : 3.9, "Volatility (Week)" : 0.0245, "Country" : "USA", "Return on Equity" : 0.094, "50-Day Low" : 0.0819, "Price" : 45.16, "50-Day High" : -0.0551, "Return on Investment" : 0.072, "Shares Float" : 6353.61, "Dividend Yield" : 0.0615, "EPS growth next 5 years" : 0.0759, "Industry" : "Computer Sales Inventory - Domestic", "Beta" : 0.62, "Sales growth quarter over quarter": 0.033, "Operating Margin" : 0.204, "EPS (ttm)" : 1.51, "PEG" : 3.95, "Float Short" : 0.0342, "52-Week Low" : 0.1402, "Average True Range" : 0.62, "EPS growth next year" : 0.0908, "Sales growth past 5 years" : 0.024, "Company" : "Target", "Gap" : 0, "Relative Volume" : 0.49, "Volatility (Month)" : 0.0148, "Market Cap" : 196498.10, "Volume" : 9599785, "Gross Margin" : 0.61, "Short Ratio" : 5.33, "Performance (Half Year)" : -0.0472, "Relative Strength Index (14)" : 51.61, "Insider Ownership" : 0.0005, "20-Day Simple Moving Average" : -0.010, "P/Free Cash Flow" : 45.36, "Institutional Transactions" : -0.009, "Performance (Year)" : 0.0978, "LT Debt/Equity" : 0.10, "Average Volume" : 25527.90, "EPS growth this year" : 0.899, "50-Day Simple Moving Average" : 0.0317}' http://localhost:8080/create

##This is just a extra one that I created to make sure it will work with two documents inserted 

##curl -H "Content-Type: application/json" -X POST -d '{"id" : "10011-2017-TEST","certificate_number" : 9278833, "Company" : "ACME TEST INC.","date" : "Feb 20 2017","result" : "No Violation Issued","sector" : "Test Retail Dealer - 101", "Ticker" : "ACMETI"}' http://localhost:8080/create

#GET A STOCK
#The first three was just extras but it can be used to get the stock. 
#curl http://localhost:8080/read?business_name="iShares%MSCI%World"
#curl http://localhost:8080/read?business_name="Fortinet%Inc."
#curl http://localhost:8080/read?business_name="Bestbuy"
#The last two tests will get the document we just inserted
#curl http://localhost:8080/read?business_name="ACME%TEST%INC."
#curl http://localhost:8080/read?business_name="Target"

#UPDATE A STOCK
#The first one is was created to test the update and the second one is the one can be updated so both of them can be use to updated the document. 
#curl http://localhost:8080/update?Ticker=URTH&Sector=Healthcare
#curl http://localhost:8080/update?Ticker=TARE&Sector=Inventory 

#DELETE A STOCK
#The first one can be deleted as well as the others. 
#curl http://localhost:8080/delete?Ticker="YCS"
#curl http://localhost:8080/delete?Ticker="ACMETI"
#curl http://localhost:8080/delete?Ticker="TARE"

#LIST TICKERS
#This will get three tickers list for all the documents in  the stocks collection. 
#curl http://localhost:8080/listTickers?tickerslist="FTNT,CSCO,EXA"
#This will list the both tickers from the documents listed.
#curl http://localhost:8080/listTickers?tickerslist="ACMETI,TARE"

#TOP 5
#This will get the top 5 industries for Application Software.
#curl http://localhost:8080/bestStock?Industry="Application%Software"


#NEW TESTS.

#gets.
#curl http://localhost:8080/read?business_name="Study%Swap"
#curl http://localhost:8080/read?business_name="Dunder%Mifflin"
#curl http://localhost:8080/read?business_name="Star%Wars%Ent."

#deletes
#curl http://localhost:8080/delete?Ticker="YODIA"

#list tickers
#curl http://localhost:8080/listTickers?tickerslist="DUNDRM,STUSWAP"

#update
#curl http://localhost:8080/update?Ticker=STUSWAP&Sector=Technology


#TOP 5
#curl http://localhost:8080/bestStock?Industry="Computer%Software"

