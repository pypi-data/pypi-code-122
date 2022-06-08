# -- coding: utf-8 --
def fetch_data(host, database, username, password):
    print("fetch data from database with params:")
    print("host : %s, database: %s, username: %s, password: %s" % (host, database, username, password))
    data = {'data': "something"}
    return data
 
 
def do_something(data):
    print("do something with data : s" % data)
    return "success"