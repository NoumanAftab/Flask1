from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



# initializing flask
app = Flask(__name__)

# initializing database
# see sqlite   https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mydbs/employee.db"
# following is to suppress warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# to create database do following:
# 1. stop app if already running
# 2. just write python on command line to run python.exe in command line
# 3. write import command as:   from app import db   then press enter
# 4. write database creation command as:  db.create_all()   database will be created at location
#    given in SQLALCHEMY_DATABASE_URI config
# 5. write exit()
# 6. goto sqlite viewer to see the database insight at https://inloop.github.io/sqlite-viewer/
# 7. drag and drop the database to this website
# 8. goto quick start https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
# 



# 1. Install jinja2 snippet kit from extensions at left
# 2.  
# 3. 
# 4. 
# 5. python .\app.py
# 6. 

class myDatabaseClass(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(20), nullable = False)
    lastname = db.Column(db.String(20), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    datecreated = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.firstname} - {self.lastname}'





@app.route("/", methods=['GET', 'POST'])
def hello_world():
    
    if request.method=='POST':
        print('Hello')
        print(request.form['first_name'])
        
        firstname = request.form['first_name']
        lastname = request.form['last_name']
        age = request.form['age']

        if firstname != '' and lastname!='' and age != '':        
            myReceivedData = myDatabaseClass(firstname = firstname, lastname = lastname, age = age)
            db.session.add(myReceivedData)
            db.session.commit()
    alldata = myDatabaseClass.query.all()
    
    return render_template('index.html', alldata=alldata)
    #return "<p>Hello, World!</p>"

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    
    # When app will shift to update endpoint/website it will get current data to fill the
    # fields in update form
    # and when update button is pressed it will post the data and data will get updated
    updateData = myDatabaseClass.query.filter_by(sno=sno).first()

    if request.method == 'POST':
        firstname = request.form['first_name']
        lastname = request.form['last_name']
        age = request.form['age']

        if firstname != '' and lastname!='' and age != '':        
            
            updateData.firstname = firstname
            updateData.lastname = lastname
            updateData.age = age
            db.session.add(updateData)
            db.session.commit()
            return redirect("/")

    return render_template('update.html', currdata=updateData)

@app.route("/delete/<int:sno>")
def delete(sno):
    delData = myDatabaseClass.query.filter_by(sno=sno).first()
    db.session.delete(delData)
    db.session.commit()
    alldata = myDatabaseClass.query.all()

    return render_template('index.html', alldata=alldata)



if __name__ == "__main__":
    app.run(debug=True, port=8000)

