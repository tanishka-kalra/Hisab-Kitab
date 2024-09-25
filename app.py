from flask import *
from sql import *
import random
import string
import yagmail
#vvpw ejel uzns ggxq
from flask_session import Session
app=Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False 
Session(app)

def generate_random_string(length=4):
    letters = string.ascii_letters 
    return ''.join(random.choice(letters) for i in range(length))


encoded_dictionary={}
for i in range(0,10):
    encoded_dictionary[str(i)]=generate_random_string()


def send_email(user,subj,bdy,file=None):
	yag = yagmail.SMTP('', '')
	recipient = user
	subject = subj
	body = bdy
	if file is not None: 
		yag.send(to=recipient,subject=subject,contents=body)
	else:
		yag.send(to=recipient,subject=subject,contents=body)



@app.route('/login',methods=['POST','GET'])
def login_page():
	if session.get('name')!=None:
		return redirect('/')
	return render_template('login.html')

@app.route('/logout',methods=['POST' ,'GET'])
def logout_page():
	print("logout func")
	print(session.get('name'))
	session['name']=None
	print(session.get('name'))
	return redirect('/')

@app.route('/register',methods=['POST','GET'])
def register_page():
	if request.method=='POST':
		firstname=request.form.get('firstname')
		email=request.form.get('email')
		if find_a_email(email):
			return '-1'
		otp=str(random.randint(100000,999999))
		print(otp)
		body=f"Hy {firstname},<br><br>Your OTP for verification is: <b>{otp}</b><br><br>Best Regards,<br><b>Debt Tracker</b>"
		send_email(email,'OTP Verification',body)
		i=0
		encoded_otp=''
		while i<len(otp):
			encoded_otp+=encoded_dictionary[otp[i:i+1]]
			i+=1
		return encoded_otp
		
		
	return render_template('register.html')
@app.route('/verifyotp',methods=['POST'])
def verify_otp():
	firstname=request.form.get('firstname')
	lastname=request.form.get('lastname')
	email=request.form.get('email')
	password=request.form.get('password')
	otp=request.form.get('otp')
	user_otp=request.form.get('user_otp')
	decoded_otp=''
	for i in user_otp:
		decoded_otp+=encoded_dictionary[i]
	print("encoded")
	print(otp)
	print(decoded_otp)
	if(decoded_otp==otp):
		return registerUser([firstname,lastname,email,password])
	else:
		return "Invalid OTP. Please Try Again Later!"
@app.route('/',methods=['POST','GET'])
def index_page():
	if (session.get('name'))== None:
		return redirect('/login')
	return render_template("index.html")

@app.route('/auth',methods=['POST'])
def authenticate_cred():
	email=request.form.get('email')
	password=request.form.get('password')
	ans = find_a_email(email)
	if (ans):
		answer = authenticate([email,password])
		print("the check for cred" ,answer)
		if (answer):
			
			session['name']=email
			print("hello")
			print(session.get('name'))
			return "True"
		else :
			return "Please Check Your Credentials"

	else:
		return "User Does not exists"
		

@app.route('/create')
def create_page():
	names=getAllNames()
	return render_template('create.html',names=names)

@app.route('/new-user',methods=['POST'])
def newUser():
	name = request.form.get('name')
	mobile=request.form.get('mobile')
	ans = find_a_record(name)
	if(ans):
		return add_record([name,mobile])
	else :
		return "User already exists"

@app.route('/update_data',methods=['POST'])
def updateInDb():
	trans_id=int(request.form.get('trans_id'))
	new_notes=request.form.get('new_notes')
	new_status=request.form.get('new_status')
	data=[new_notes,new_status,trans_id]
	return updateInDbsql(data)
	
@app.route('/existing-user', methods=['POST'])
def existingUser(): 
	name=int(request.form.get('name'))
	amount=int(request.form.get('amount'))
	Location=request.form.get('location')
	Date = request.form.get('date')
	Notes=request.form.get('notes')
	status = request.form.get('status')
	dataList=[name,amount,Location,Date,Notes,status]
	return addinTransaction(dataList)

@app.route('/view-all',methods=['POST','GET'])
def viewData():

	names=getAllNames()
    
	return render_template('view.html',names=names)
    # upper=request.args.get('upper')
	# lower=request.args.get('lower')
	# print(upper)
	# print(lower)
	
	# print("para")
	# data = getAllData([upper,lower])
	
	# # id=request.args.get('id')
	# # if id!=None:
	# # 	id=id.split(',')
	# # 	upper=request.form.get('upper')
	# # 	lower=request.form.get('lower')
	# # 	return
	# # data = getAllData(lower,upper)
	# # names=getAllNames()
	

@app.route('/view',methods=['POST'])
def show_data():
	upper=request.form.get('upper')
	lower=request.form.get('lower')
	print(upper)
	print(lower)
	data=getAllData([lower,upper])
	return data
@app.route('/edit_data',methods=['POST'])
def editData():
	id=int(request.form.get('id'))
	print(id)
	data=dataforedit(id)
	return data

@app.route('/updateTransaction' , methods=['POST'])
def updateTrans():
	id=request.json.get('id')
	date=request.json.get('date')
	updated_notes=request.json.get('updated_notes')
	updated_status=request.json.get('updated_status')
	data=[updated_notes,updated_status,id,date]
	return "Data Inserted succssfully"
	
@app.route('/getDateData' , methods=['POST'])
def filteronDate():
	date=request.form.get('date')
	data=getDateData(date)
	return data
    
@app.route('/viewonfilter',methods=['POST'])
def view():
	lower=request.form.get('lower')
	upper=request.form.get('upper')
	id=request.form.get("dt[name]")
	date=request.form.get("dt[date]")
	status=request.form.get("dt[status]")
	data={
		'id':id,
		'date':date,
		'status':status,
		'lower':lower,
		'upper':upper
	}
	return viewOnFilter(data)
	


	
'''
SELECT * , row_number() OVER (ORDER BY DATE DESC) AS ROW_NUM FROM TRANSACTION

'''