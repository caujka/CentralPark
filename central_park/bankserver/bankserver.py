import os, requests, json, time
from flask import Flask, request, render_template, jsonify, redirect
import httplib, urllib


# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'central_park.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
    
app.config.from_envvar('APP_SETTINGS', silent=True)

def check_card_number():
	return True


def send_data(data):
	data_json = json.dumps(data)
	payload = {'json_payload': data_json}
	url = "http://localhost:5002/server_url"
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	r = requests.post(url, data=json.dumps(data), headers=headers)


@app.route('/transaction', methods=['POST'])
def pay():
	if check_card_number(): 
		info = {}
		info['amt'] = request.form.get('amt')
		info['ccy'] = request.form.get('ccy')
		info['merchant'] = request.form.get('merchant')
		info['order'] = request.form.get('order')
		info['details'] = request.form.get('details')
		info['ext_details'] = request.form.get('ext_details')
		info['pay_way'] = request.form.get('pay_way')
		info['server_url'] = request.form.get('server_url')
		info['return_url'] = request.form.get('return_url')
		send_data(info)
		return redirect(info['return_url'], code=302)


@app.route('/payment', methods=['POST'])
def testpay():
	info = {}
	info['amt'] = request.form.get('amt')
	info['ccy'] = request.form.get('ccy')
	info['merchant'] = request.form.get('merchant')
	info['order'] = request.form.get('order')
	info['details'] = request.form.get('details')
	info['ext_details'] = request.form.get('ext_details')
	info['pay_way'] = request.form.get('pay_way')
	info['server_url'] = request.form.get('server_url')
	info['return_url'] = request.form.get('return_url')
	return render_template('bankpayment.html', info=info)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port = 5001)
    