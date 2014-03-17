from bottle import route, run, get, post, request
import json, sqlite3

@route('/')
def go():
    body =   """
                <form action= "/result" method = "post" enctype="application/json">
                    <input type = "text" name = "edit_text" size = "200" value = '{"key1":"val1", "key2":"val2"}'>
                    <p>
                    <input type = "submit" name = "onsubmit" >
                </form>
            """
    return body 

@post ('/result')
def onsubmit():
    result_get = request.forms.get('edit_text')
    json_values = json.loads(result_get) # convert from string to json

    db_insert = [json_values['key1'], json_values['key2']] # for the insertion into the table

## working with database
    conn = sqlite3.connect('test.db') ##db connect
    c = conn.cursor()   ##set up cursor
    c.execute('''CREATE TABLE IF NOT EXISTS parking
             (key1 text, key2 text)''')
    c.execute("INSERT INTO parking VALUES (?, ?)", db_insert)# Insert a row of data
# Save (commit) the changes
    conn.commit()
# Show the result into the page
    str_result = ""
    select_execute = c.execute('SELECT * FROM parking')
    for row in select_execute:
        str_result = str_result+"<p>"+ unicode(row)      
    conn.close()
    return str_result +"<p>" +go() #"result:"+json.dumps(c) +"<p>" +go()

run(host='localhost', port=8080, debug=True)
