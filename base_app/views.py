from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from datetime import datetime,date
from django.db.models import Sum
from django.core.mail import send_mail


from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User, auth


def base(request):
	return render(request, 'base.html')

def index(request):
	return render(request, 'index.html')

def login(request):
	return render(request, 'login.html')

def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if staff_registration.objects.filter(email=request.POST['username'], password=request.POST['password']):
                
            member=staff_registration.objects.get(email=request.POST['username'], password=request.POST['password'])
            request.session['stf_id'] = member.id 
            mem1=staff_registration.objects.filter(id= member.id)
                
            return render(request,'Staff_dashboard.html',{'mem1':mem1})
        user = auth.authenticate(username=username, password=password)
        if user.is_superuser:
            request.session['Ad_id']=user.id
            auth.login(request, user)
            return redirect('Admin_index')
        elif user is not None:
            request.session['usr_id']=user.id
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Invalid Username or Password. Try Again.')
            return redirect('loginpage')
    else:
        messages.info(request, 'Oops, Something went wrong.')
        return redirect('signup')		

def signup(request):
	return render(request, 'signup.html')

def signuppage(request):
	if request.method == 'POST':
		firstname = request.POST['first_name']
		lastname = request.POST['last_name']
		username = request.POST['username']
		password = request.POST['password']
		cpassword = request.POST['cpassword']
		
		
		if password == cpassword:
			if User.objects.filter(username=username):
				messages.info(request, 'This username already exists. Sign up again')
				return redirect('signup')
			else:
				user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, password=password)
				user.save()
				print('hello')
				return redirect('login')
		else:
			messages.info(request, 'Password doesnt match. Signup Again')
			return redirect('signup')
	else:
		messages.info(request, 'Oops....Something went wrong.')
		return redirect('signup')

def logout(request):
    auth.logout(request)
    return redirect('index')

def staff_logout(request):
    if 'stf_id' in request.session:  
        request.session.flush()
        return redirect('/')
    else:
        return redirect('/')


def aboutus(request):
	return render(request, 'about.html')

def services(request):
	return render(request, 'services.html')

def contact(request):
	return render(request, 'contact.html')

def sendmail(request):
    if request.method == 'POST':
        message_name = request.POST['message_name']
        message_email = request.POST['message_email']
        message = request.POST['message']
        print(message_name, message_email, message)
        send_mail(
            message_name, #subject
            message, #message
            message_email, #from email
            ['demo@gmail.com'] #to emails
        )
        return redirect('contact')
    else:
        return redirect('contact')

def requests(request):
	if 'usr_id' in request.session:
		if request.session.has_key('usr_id'):
			usr_id = request.session['usr_id']
		else:
			variable = "dummy"
		pro = User.objects.filter(id=usr_id)
		return render(request, 'request.html',{'pro':pro})
	else:
		return redirect('/')

def requests_send(request):
	if 'usr_id' in request.session:
		if request.session.has_key('usr_id'):
			usr_id = request.session['usr_id']
		else:
			variable = "dummy"
		pro = User.objects.filter(id=usr_id)
		if request.method == 'POST':
			req = order_request()
			req.firstname = request.POST.get('fname')
			req.lastname = request.POST.get('lname')
			req.email = request.POST.get('email')
			req.companyname = request.POST.get('cname')
			req.producttype = request.POST.get('ptype')
			req.timetocontact = request.POST.get('ctime')
			req.tranporttype = request.POST.get('ttype')
			req.quantity = request.POST.get('qty')
			req.shipmentdate = request.POST.get('sdate')
			req.from_place = request.POST.get('from')
			req.to_place = request.POST.get('to')
			req.messege = request.POST.get('msg')
			req.user_id = usr_id
			req.status = 'pending'
			req.save()
		return redirect( 'requests' )	
	else:
		return redirect('/')
		
	
	
def status(request):
	if 'usr_id' in request.session:
		if request.session.has_key('usr_id'):
			usr_id = request.session['usr_id']
		else:
			variable = "dummy"
		pro = User.objects.filter(id=usr_id)
		req = order_request.objects.filter(user_id=usr_id).order_by('-id')
		return render(request, 'status.html',{'pro':pro,'req':req})
	else:
		return redirect('/')	

def order_confirmation(request,id):
	req = order_request.objects.get(id=id)
	return render(request, 'order_confirmation.html',{'req':req})

def confirm_order(request,id):
	if request.method == 'POST':            
		req = order_request.objects.get(id=id)
		req.status='confirmed'
		req.save()
		pay = payment()
		pay.bank = request.POST.get('bankname')
		pay.accountnumber = request.POST.get('accnumber')
		pay.ifse = request.POST.get('ifsecode')
		pay.payment = req.rate
		pay.order_id = id
		pay.user_id = req.user_id
		pay.date = datetime.now()
		pay.save()	
	return redirect('status')

def orders(request):
	if 'usr_id' in request.session:
		if request.session.has_key('usr_id'):
			usr_id = request.session['usr_id']
		else:
			variable = "dummy"
		pro = User.objects.filter(id=usr_id)
		req = order_request.objects.filter(user_id=usr_id).order_by('-id')
		return render(request, 'orders.html',{'pro':pro,'req':req})
	else:
		return redirect('/')

def Air_service(request):
	return render(request, 'Air_service.html')

def Ship_service(request):
	return render(request, 'Ship_service.html')

def Ground_service(request):
	return render(request, 'Ground_service.html')

def Warehousing(request):
	return render(request, 'Warehousing.html')


#############   Admin module ################

def Admin_index(request):
	return render(request, 'Admin_index.html')

def Admin_dashboard(request):
	ncount = order_request.objects.filter(status = 'confirmed').count()
	anum = order_request.objects.filter(status = 'assigned').count()
	rnum = order_request.objects.filter(status = 'rejected').count()
	return render(request, 'Admin_dashboard.html',{'anum':anum, 'ncount':ncount, 'rnum':rnum})

def Admin_requests(request):
	req =order_request.objects.filter(status='pending').order_by('-id')
	return render(request, 'Admin_requests.html',{'req':req})

def request_accept(request,id):
	req = order_request.objects.get(id=id)
	if request.method == 'POST':
		req.status = "accepted"
		req.rate = request.POST.get('rate')
		req.save()
	return redirect('Admin_requests')

def request_reject(request,id):
	if request.method == 'POST':            
		req = order_request.objects.get(id=id)
		req.reject_reason=request.POST.get('reply')
		req.status='rejected'
		req.save()
	return redirect('Admin_requests')

def Admin_neworder_dptcard(request):
	anum = order_request.objects.filter(tranporttype ='Air Freight').filter(status = 'confirmed').filter(staff__isnull=True).count()
	snum = order_request.objects.filter(tranporttype ='Ocean Freight').filter(status = 'confirmed').filter(staff__isnull=True).count()
	gnum = order_request.objects.filter(tranporttype ='Ground shipment').filter(status = 'confirmed').filter(staff__isnull=True).count()
	return render(request, 'Admin_neworder_dptcard.html',{'anum':anum,'snum':snum, 'gnum':gnum})

def Admin_air_new_orders(request):
	req = order_request.objects.filter(tranporttype ='Air Freight').filter(status = 'confirmed').filter(staff__isnull=True)
	staff = staff_registration.objects.all()
	return render(request, 'Admin_air_new_orders.html',{'req':req,'staff':staff})

def staff_assign_air(request,id):
	if request.method == 'POST':            
		req = order_request.objects.get(id=id)
		req.staff_id=request.POST.get('staff')
		req.status = 'assigned'
		req.shipment_status = 'pending'
		req.save()
	return redirect('Admin_air_new_orders')

def Admin_ship_new_orders(request):
	req = order_request.objects.filter(tranporttype ='Ocean Freight').filter(status = 'confirmed').filter(staff__isnull=True)
	staff = staff_registration.objects.all()
	return render(request, 'Admin_ship_new_orders.html',{'req':req,'staff':staff})

def staff_assign_ship(request,id):
	if request.method == 'POST':            
		req = order_request.objects.get(id=id)
		req.staff_id=request.POST.get('staff')
		req.status = 'assigned'
		req.shipment_status = 'pending'
		req.save()
	return redirect('Admin_ship_new_orders')

def Admin_ground_new_orders(request):
	req = order_request.objects.filter(tranporttype ='Ground shipment').filter(status = 'confirmed').filter(staff__isnull=True)
	staff = staff_registration.objects.all()
	return render(request, 'Admin_ground_new_orders.html',{'req':req,'staff':staff})

def staff_assign_ground(request,id):
	if request.method == 'POST':            
		req = order_request.objects.get(id=id)
		req.staff_id=request.POST.get('staff')
		req.status = 'assigned'
		req.shipment_status = 'pending'
		req.save()
	return redirect('Admin_ground_new_orders')

def Admin_statics(request):
	torder = order_request.objects.filter(status = 'assigned').count()
	tpay = payment.objects.aggregate(Sum('payment'))['payment__sum']
	tuser = User.objects.all().count()
	return render(request, 'Admin_statics.html',{'torder':torder,'tpay':tpay, 'tuser':tuser})

def Admin_accepted_orders(request):
	req = order_request.objects.filter(status = 'assigned')
	return render(request, 'Admin_accepted_orders.html',{'req':req})

def Admin_rejected_orders(request):
	req = order_request.objects.filter(status = 'rejected')
	return render(request, 'Admin_rejected_orders.html',{'req':req})

def Admin_Staffs(request):
	snum = staff_registration.objects.all().count()
	return render(request, 'Admin_Staffs.html',{'snum':snum})

def Admin_addstaff(request):
	dep = department.objects.all()
	return render(request, 'Admin_addstaff.html',{'dep':dep})

def add_staff_save(request):
	if request.method == 'POST':
		req = staff_registration()
		req.fullname = request.POST.get('fname')
		req.email = request.POST.get('email')
		req.salary = request.POST.get('sal')
		req.department_id = request.POST.get('dept')
		req.password = request.POST.get('pass')
		req.status = 'active'
		req.joiningdate = datetime.now()
		req.photo = 'images/blank.jpg'
		req.save()
	return redirect('Admin_Staffs')

def Admin_all_staffs(request):
	staff = staff_registration.objects.all()
	return render(request, 'Admin_all_staffs.html',{'staff':staff})

def staff_delete(request,id):
    staff = staff_registration.objects.get(id=id)
    staff.delete()
    return redirect('Admin_all_staffs')

def Admin_contact(request):
	return render(request, 'Admin_contact.html')

def Admin_departments(request):
	dpt = department.objects.all()
	return render(request, 'Admin_departments.html',{'dpt':dpt})

def Admin_create_departments(request):
	return render(request, 'Admin_create_dpt.html')

def dpt_save(request):
	if request.method == 'POST':
		dpt = department()
		dpt.department_name = request.POST.get('dname')
		dpt.save()
	return redirect('Admin_departments')

#############   Admin module ################

##### staff module #####

def Staff_index(request):
	if 'stf_id' in request.session:
		if request.session.has_key('stf_id'):
			stf_id = request.session['stf_id']
		else:
			variable = "dummy"
		mem1 = staff_registration.objects.filter(id = stf_id)
		return render(request, 'Staff_index.html',{'mem1':mem1})
	else:
		return redirect('login')

def Staff_account_settings(request):
	if 'stf_id' in request.session:
		if request.session.has_key('stf_id'):
			stf_id = request.session['stf_id']
		else:
			variable = "dummy"
		mem1 = staff_registration.objects.filter(id = stf_id)
		return render(request, 'Staff_account_settings.html',{'mem1':mem1})
	else:
		return redirect('login')

def staff_acc_save(request, id):
	if request.method == 'POST':
		stf = staff_registration.objects.get(id=id)
		stf.fullname = request.POST.get('fname')
		stf.dateofbirth = request.POST.get('dob')
		stf.email = request.POST.get('email')
		stf.mobile = request.POST.get('contact')
		stf.address1 = request.POST.get('ad1')
		stf.address2 = request.POST.get('ad2')
		stf.State = request.POST.get('state')
		stf.pincode = request.POST.get('pcode')
		stf.district = request.POST.get('city')
		try:
			stf.photo = request.FILES['pic']
		except:
			pass
		stf.save()
	return redirect('Staff_account_settings')


def Staff_dashboard(request):
	if 'stf_id' in request.session:
		if request.session.has_key('stf_id'):
			stf_id = request.session['stf_id']
		else:
			variable = "dummy"
		mem1 = staff_registration.objects.filter(id = stf_id)
		num = order_request.objects.filter(staff_id = stf_id).filter(shipment_status = 'pending').count()
		cnum = order_request.objects.filter(staff_id = stf_id).filter(shipment_status = 'success').count()
		return render(request, 'Staff_dashboard.html',{'mem1':mem1,'num':num,'cnum':cnum})
	else:
		return redirect('login')	


def Staff_orders(request):
	if 'stf_id' in request.session:
		if request.session.has_key('stf_id'):
			stf_id = request.session['stf_id']
		else:
			variable = "dummy"
		mem1 = staff_registration.objects.filter(id = stf_id)
		req = order_request.objects.filter(staff_id = stf_id).filter(shipment_status = 'pending').order_by('-id')
		return render(request, 'Staff_orders.html',{ 'mem1':mem1, 'req':req })
	else:
		return redirect('login')

def Staff_completed_orders(request):
	if 'stf_id' in request.session:
		if request.session.has_key('stf_id'):
			stf_id = request.session['stf_id']
		else:
			variable = "dummy"
		mem1 = staff_registration.objects.filter(id = stf_id)
		req = order_request.objects.filter(staff_id = stf_id).filter(shipment_status = 'success').order_by('-id')
		return render(request, 'Staff_completed_orders.html',{ 'mem1':mem1, 'req':req })
	else:
		return redirect('login')

def Staff_tracking_update(request,id):
	req = order_request.objects.get(id = id)
	return render(request, 'Staff_tracking_update.html',{'req':req})

def Staff_tracking_update_save(request,id):
	if request.method == 'POST':
		req = order_request.objects.get(id = id)
		req.shipment_status = request.POST.get('sta')
		req.tracking_status = request.POST.get('Tdetails')
		req.save()
	return redirect('Staff_orders')





