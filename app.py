from flask import Flask, render_template, request, url_for, send_file, session, redirect, escape
import mysql.connector
from werkzeug.utils import secure_filename
import os
import sys

mydb = mysql.connector.connect(host="localhost", user="grafana_script", password="grafana_script", database = "grafana")
cur = mydb.cursor()

app = Flask(__name__)

@app.route('/index')
def main():
	return render_template(('index.html'))


@app.route('/visualize', methods = ['GET', 'POST'])
def visualize():

	if request.method == 'POST':
		if 'file' not in request.files:
			error = 'Error : No file chosen'
			return render_template(('index.html'), error = error)
		file = request.files['file']
		if file.filename == '':
			error = 'Error: No selected file'
			return render_template(('index.html'), error = error)
		else:
			filename = secure_filename(file.filename)
			file.save(os.path.join('/var/lib/mysql-files', filename))
			print('file saved')
			query = r"LOAD DATA INFILE '/var/lib/mysql-files/" + str(filename) + "' into table dynamic fields terminated by  ',' enclosed by '\"'" + r" lines terminated by '\n' ignore 1 rows (date, weight, calories);"
			print(query)
			cur.execute(query)
			cur.execute("UPDATE dynamic SET ts = UNIX_TIMESTAMP(date);")
			mydb.commit()
			return redirect('http://localhost:3000/d/k-Zi__9Wz/myfitnesspal?panelId=2&fullscreen&orgId=1')

	error = 'File upload unsuccessfull'
	return render_template('index.html', error=error)

if __name__ == '__main__':
	app.run(debug=True, port=8080)
