from bottle import route, run, get, post, request
import json, sqlite3

keys =   ["id","number","time","position","name"]
db_field=["text","text","text","text","text"]
values = ["1","lk 890","time","5","Asa"] 
key_val = dict(zip(keys,values))
@route('/')
def go():
    body =   """
                <form action= "/" method = "post" enctype="application/json">
                    <input type = "text" name = "edit_text" size = "200" value =" """+ str(key_val) +""" ">
                    <p>
                    <input type = "submit" name = "onsubmit" >
                </form>
            """ 
    return body 
'{"key1":"val1", "key2":"val2"}'

@post ('/')
def onsubmit():
    result_get = request.forms.get('edit_text')
    json_values = json.loads(result_get) # convert from string to json
 
    db_insert = "("
    i = 0
    for key in keys
        db_insert = db_insert + str(json_values[keys[i]])+","
        i = i+1
    db_insert = db_insert[:len(db_insert)-1]+")" 
    # for the insertion into the table
    
    db_create = "("    
    i = 0
    for elem in keys
        db_create = db_create + keys[i]+" "+ db_field[i]+","
        i = i+1
    db_create = db_create[:len(db_create)-1]+")"
## working with database
    conn = sqlite3.connect('test.db') ##db connect
    c = conn.cursor()   ##set up cursor
    c.execute("""CREATE TABLE IF NOT EXISTS parking1
             """ + db_create )
    c.execute("INSERT INTO parking VALUES " + db_insert)# Insert a row of data
# Save (commit) the changes
    conn.commit()
# Show the result into the page
    str_result = ""
    select_execute = c.execute('SELECT * FROM parking')
    for row in select_execute:
        str_result = str_result+"<p>"+ unicode(row)      
    conn.close()
    return str_result +"<p>" + str(key_val) +go() #"result:"+json.dumps(c) +"<p>" +go()

run(host='localhost', port=8080, debug=True)
