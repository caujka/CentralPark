from bottle import route, run, get, post, request
import json, sqlite3

#define databases fields and basic values
keys =   ["id","number","time","position","name", "value"]
db_field=["text","text","text","text","text", "number"]
values = ["1","lk 890","time","5","Asa", "22"] 
key_val = dict(zip(keys,values))
DATABASE_NAME = "test.db"
TABLE_NAME = "parking_new"

@route('/')
def go():
    body =  '''
                <form action= '/' method = 'post' enctype='application/json'>
                    <input type = 'text' name = 'edit_text' size = '200' value = '%s'>
                    <p>
                    <input type = "submit" name = "onsubmit" >
                </form>
            ''' % unicode(key_val).replace("'",'"')
    return body 

@post ('/')
def onsubmit():
#obtain the string result from the form
    result_get = request.forms.get('edit_text')
# convert from string to json
    json_values = json.loads(result_get) 

# all values for the insertion into the table (no keys)
    db_insert = "("
    i = 0
    for key in keys:
        db_insert = db_insert + "'"+str(json_values[keys[i]])+"'"+","
        i = i+1
    db_insert = db_insert[:len(db_insert)-1]+")" 
# keys and fields for the creation the table
    db_create = "("    
    i = 0
    for elem in keys:
        db_create = db_create + keys[i]+" "+ db_field[i]+","
        i = i+1
    db_create = db_create[:len(db_create)-1]+")"

# working with database create and insert
    conn = sqlite3.connect(DATABASE_NAME) ##db connect
    c = conn.cursor()   ##set up cursor
    c.execute("CREATE TABLE IF NOT EXISTS %s " % TABLE_NAME + db_create )
    c.execute("INSERT INTO %s VALUES " % TABLE_NAME + db_insert) # Insert a row of data
# Save (commit) the changes
    conn.commit()
# Show the result into the page
    str_result = ""
    select_execute = c.execute("SELECT * FROM %s" % TABLE_NAME) 
    for row in select_execute:
        str_result = str_result+"<p>"+ str(row)      
    conn.close()
    return str_result +"<p>" + str(key_val) +go()

run(host='localhost', port=8080, debug=True)
