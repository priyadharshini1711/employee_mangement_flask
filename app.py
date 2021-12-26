from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/employee_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db =SQLAlchemy(app)

class EmployeeDetails(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    address = db.Column(db.String(255))

    def __init__(self,name,email,phone,address):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address


@app.route('/')
def index():
    all_data = EmployeeDetails.query.all()
    return render_template('index.html',employees = all_data)

@app.route('/insert',methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        my_data = EmployeeDetails(name, email, phone, address)
        db.session.add(my_data)
        db.session.commit()

        flash("Employee Inserted Successfully")

        return redirect(url_for('index'))

@app.route('/update', methods=['GET','POST'])
def update():
    if request.method == 'POST':
        my_data = EmployeeDetails.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        my_data.address = request.form['address']
        db.session.commit()

        flash("Employee updates successfully")

        return redirect(url_for('index'))

@app.route('/delete/<id>',methods = ['GET','POST'])
def delete(id):
    my_data = EmployeeDetails.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    flash("Employee Deleted Successfully")

    return redirect(url_for('index'))

@app.route('/delete_all',methods = ['GET','POST'])
def delete_all():
    db.session.query(EmployeeDetails).delete()
    db.session.commit()

    flash("All Employees Deleted Successfully")

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)