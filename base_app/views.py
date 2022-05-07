from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from datetime import datetime,date
from django.db.models import Sum
from django.core.mail import send_mail
from warehouse.settings import EMAIL_HOST_USER
from django.db.models import Q
import random



from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User, auth


def base(request):
	return render(request, 'base.html')

def index(request):
	return render(request, 'index.html')

def Change_password(request):
	if 'usr_id' in request.session:
		if request.session.has_key('usr_id'):
			usr_id = request.session['usr_id']
		users = User.objects.filter(id=usr_id)
		if request.method == 'POST':

			newPassword = request.POST.get('newPassword')
			confirmPassword = request.POST.get('confirmPassword')

			user = User.objects.get(id=usr_id)
			if newPassword == confirmPassword:
				user.set_password(newPassword)
				user.save()
				msg_success = "Password has been changed successfully"
				return render(request, 'Change_password.html', {'msg_success': msg_success})
			else:
				msg_error = "Password does not match"
				return render(request, 'Change_password.html', {'msg_error': msg_error})
		return render(request, 'Change_password.html', {'users': users})
	else:
		return redirect('/')

def forgot_password(request):
	if request.method == "POST":
		email_id = request.POST.get('email')
		access_staff_data = staff_registration.objects.filter(email=email_id).exists()
		if access_staff_data:
			_staff = staff_registration.objects.filter(email=email_id)
			password = random.SystemRandom().randint(100000, 999999)
			print(password)
			_staff.update(password = password)
			subject =' your authentication data updated'
			message = 'Password Reset Successfully\n\nYour login details are below\n\nUsername : ' + str(email_id) + '\n\nPassword : ' + str(password) + \
                '\n\nYou can login this details\n\nNote: This is a system generated email, do not reply to this email id'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [email_id, ]
			send_mail(subject, message, email_from,
                      recipient_list, fail_silently=True)
            # _user.save()
			msg_success = "Password Reset successfully check your mail new password"
			return render(request, 'forgot_password.html', {'msg_success': msg_success})
		else:
			msg_error = "This email does not exist  "
			return render(request, 'forgot_password.html', {'msg_error': msg_error})
	return render(request, 'forgot_password.html')

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
            return redirect('Admin_dashboard')
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
		email = request.POST['email']
		
		
		if password == cpassword:
			if User.objects.filter(username=username):
				messages.info(request, 'This username already exists. Sign up again')
				return redirect('signup')
			else:
				user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, password=password, email=email)
				user.save()
				print('hello')
				return redirect('login')
		else:
			messages.info(request, 'Password doesnt match. Signup Again')
			return redirect('signup')
	else:
		messages.info(request, 'Oops....Something went wrong.')
		return redirect('signup')

def Admin_logout(request):
	if 'Ad_id' in request.session:
		auth.logout(request)
		return redirect('login')

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

def contactus_save(request):
	if 'usr_id' in request.session:
		if request.session.has_key('usr_id'):
			usr_id = request.session['usr_id']
		else:
			variable = "dummy"
		pro = User.objects.filter(id=usr_id)
		if request.method == 'POST':
			cou = contact_us()
			cou.firstname = request.POST.get('fname')
			cou.lastname = request.POST.get('lname')
			cou.email = request.POST.get('email')
			cou.subject = request.POST.get('sub')
			cou.message = request.POST.get('msg')
			cou.user_id = usr_id
			cou.replay_status = 0
			cou.save()	
			messages.success(request, 'Success')
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
			req.messege = request.POST.get('msg')
			req.user_id = usr_id
			req.status = 'pending'
			req.save()
			messages.success(request, 'Success')
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
	if 'usr_id' in request.session:
		if request.session.has_key('usr_id'):
			usr_id = request.session['usr_id']
		else:
			variable = "dummy"
		pro = User.objects.filter(id=usr_id)
		req = order_request.objects.get(id=id)
		return render(request, 'order_confirmation.html',{'req':req,'pro':pro})
	else:
		return redirect('/')	

def confirm_order(request,id):
	if request.method == 'POST':            
		req = order_request.objects.get(id=id)
		req.status='confirmed'
		req.shipment_status = 'pending'
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
		req = order_request.objects.filter(Q(user_id=usr_id) | Q(status='confirmed')).order_by('-id')
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
	if 'Ad_id' in request.session:
		if request.session.has_key('Ad_id'):
			Ad_id = request.session['Ad_id']
		else:
			variable = "dummy"
		pro = User.objects.filter(id=Ad_id)
		return render(request, 'Admin_index.html',{'pro':pro})
	else:
		return redirect('login')

def Admin_changepassword(request):
	if 'Ad_id' in request.session:
		if request.session.has_key('Ad_id'):
			Ad_id = request.session['Ad_id']
		else:
			variable = "dummy"
		pro = User.objects.filter(id=Ad_id)
		return render(request,'Admin_changepassword.html',{'pro':pro})
	else:
		return redirect('login')

def Admin_changepwd_save(request):
	if request.method == 'POST':
		newPassword = request.POST.get('newPassword')
		confirmPassword = request.POST.get('confirmPassword')

		user = User.objects.get(is_superuser=True)
		if newPassword == confirmPassword:
			user.set_password(newPassword)
			user.save()
			msg_success = "Password has been changed successfully"
			return render(request, 'Admin_dashboard.html', {'msg_success': msg_success})
		else:
			msg_error = "Password does not match"
			return render(request, 'Admin_changepassword.html', {'msg_error': msg_error})
	return render(request,'Admin_changepassword.html')

def Admin_dashboard(request):
	if 'Ad_id' in request.session:
		if request.session.has_key('Ad_id'):
			Ad_id = request.session['Ad_id']
		else:
			variable = "dummy"
		pro = User.objects.filter(id=Ad_id)
		anum = order_request.objects.filter(status = 'confirmed').count()
		rnum = order_request.objects.filter(status = 'rejected').count()
		return render(request, 'Admin_dashboard.html',{'anum':anum, 'rnum':rnum,'pro':pro})
	else:
		return redirect('login')

def Admin_neworder_dptcard(request):
	if 'Ad_id' in request.session:
		if request.session.has_key('Ad_id'):
			Ad_id = request.session['Ad_id']
		else:
			variable = "dummy"
		pro = User.objects.filter(id=Ad_id)
		anum = order_request.objects.filter(tranporttype ='Air Freight').filter(status = 'pending').count()
		snum = order_request.objects.filter(tranporttype ='Ocean Freight').filter(status = 'pending').count()
		gnum = order_request.objects.filter(tranporttype ='Ground shipment').filter(status = 'pending').count()
		return render(request, 'Admin_neworder_dptcard.html',{'anum':anum,'snum':snum, 'gnum':gnum,'pro':pro})
	else:
		return redirect('login')

def Admin_air_new_orders(request):
	if 'Ad_id' in request.session:
		if request.session.has_key('Ad_id'):
			Ad_id = request.session['Ad_id']
		else:
			variable = "dummy"
		pro = User.objects.filter(id=Ad_id)
		req = order_request.objects.filter(tranporttype ='Air Freight').filter(status = 'pending')
		staff = staff_registration.objects.all()
		return render(request, 'Admin_air_new_orders.html',{'req':req,'staff':staff,'pro':pro})
	else:
		return redirect('login')

def staff_assign_air(request,id):
	if request.method == 'POST':            
		req = order_request.objects.get(id=id)
		req.staff_id=request.POST.get('staff')
		req.status = 'assigned'
		req.save()
		messages.success(request, 'order assigned to the staff successfully')
	return redirect('Admin_air_new_orders')

def Admin_ship_new_orders(request):
	if 'Ad_id' in request.session:
		if request.session.has_key('Ad_id'):
			Ad_id = request.session['Ad_id']
		else:
			variable = "dummy"
		pro = User.objects.filter(id=Ad_id)
		req = order_request.objects.filter(tranporttype ='Ocean Freight').filter(status = 'pending')
		staff = staff_registration.objects.all()
		return render(request, 'Admin_ship_new_orders.html',{'req':req,'staff':staff,'pro':pro})
	else:
		return redirect('login')

def staff_assign_ship(request,id):
	if request.method == 'POST':            
		req = order_request.objects.get(id=id)
		req.staff_id=request.POST.get('staff')
		req.status = 'assigned'
		req.save()
		messages.success(request, 'order assigned to the staff successfully')
	return redirect('Admin_ship_new_orders')

def Admin_ground_new_orders(request):
	if 'Ad_id' in request.session:
		if request.session.has_key('Ad_id'):
			Ad_id = request.session['Ad_id']
		else:
			variable = "dummy"
		pro = User.objects.filter(id=Ad_id)
		req = order_request.objects.filter(tranporttype ='Ground shipment').filter(status = 'pending')
		staff = staff_registration.objects.all()
		return render(request, 'Admin_ground_new_orders.html',{'req':req,'staff':staff,'pro':pro})
	else:
		return redirect('login')

def staff_assign_ground(request,id):
	if request.method == 'POST':            
		req = order_request.objects.get(id=id)
		req.staff_id=request.POST.get('staff')
		req.status = 'assigned'
		req.save()
		messages.success(request, 'order assigned to the staff successfully')
	return redirect('Admin_ground_new_orders')

def Admin_statics(request):
	if 'Ad_id' in request.session:
		if request.session.has_key('Ad_id'):
			Ad_id = request.session['Ad_id']
		else:
			variable = "dummy"
		pro = User.objects.filter(id=Ad_id)
		torder = order_request.objects.filter(status = 'confirmed').count()
		tpay = payment.objects.aggregate(Sum('payment'))['payment__sum']
		tuser = User.objects.all().count()
		str = storage.objects.all()
		tq = order_request.objects.filter(Q(shipment_status='pending') | Q(shipment_status='Success')).aggregate(Sum('quantity'))['quantity__sum']
		return render(request, 'Admin_statics.html',{'torder':torder,'tpay':tpay, 'tuser':tuser,'str':str,'tq':tq,'pro':pro})
	else:
		return redirect('login')

def Admin_accepted_orders(request):
	if 'Ad_id' in request.session:
		if request.session.has_key('Ad_id'):
			Ad_id = request.session['Ad_id']
		else:
			variable = "dummy"
		pro = User.objects.filter(id=Ad_id)
		req = order_request.objects.filter(status = 'confirmed').order_by('-id')
		return render(request, 'Admin_accepted_orders.html',{'req':req,'pro':pro})
	else:
		return redirect('login')

def Admin_rejected_orders(request):
	if 'Ad_id' in request.session:
		if request.session.has_key('Ad_id'):
			Ad_id = request.session['Ad_id']
		else:
			variable = "dummy"
		pro = User.objects.filter(id=Ad_id)
		req = order_request.objects.filter(status = 'rejected')
		return render(request, 'Admin_rejected_orders.html',{'req':req,'pro':pro})
	else:
		return redirect('login')

def Admin_Staffs(request):
	if 'Ad_id' in request.session:
		if request.session.has_key('Ad_id'):
			Ad_id = request.session['Ad_id']
		else:
			variable = "dummy"
		pro = User.objects.filter(id=Ad_id)
		snum = staff_registration.objects.all().count()
		return render(request, 'Admin_Staffs.html',{'snum':snum,'pro':pro})
	else:
		return redirect('login')

def Admin_addstaff(request):
	if 'Ad_id' in request.session:
		if request.session.has_key('Ad_id'):
			Ad_id = request.session['Ad_id']
		else:
			variable = "dummy"
		pro = User.objects.filter(id=Ad_id)
		dep = department.objects.all()
		return render(request, 'Admin_addstaff.html',{'dep':dep,'pro':pro})
	else:
		return redirect('login')

def add_staff_save(request):
	if request.method == 'POST':
		req = staff_registration()
		req.fullname = request.POST.get('fname')
		req.email = request.POST.get('email')
		req.salary = request.POST.get('sal')
		req.department_id = request.POST.get('dept')
		req.password = random.randint(10000, 99999)
		req.status = 'active'
		req.joiningdate = datetime.now()
		req.photo = 'images/blank.jpg'
		req.save()
		subject = 'Welcome warehouse'
		message = 'Congratulations,\n' \
        'You have successfully registered with our website.\n' \
        'username :'+str(req.email)+'\n' 'password :'+str(req.password) + \
        '\n' 'WELCOME '
		recepient = str(req.email)
		send_mail(subject, message, EMAIL_HOST_USER,
                [recepient], fail_silently=False)
		messages.success(request, 'success')
	return redirect('Admin_addstaff')

def Admin_all_staffs(request):
	if 'Ad_id' in request.session:
		if request.session.has_key('Ad_id'):
			Ad_id = request.session['Ad_id']
		else:
			variable = "dummy"
		pro = User.objects.filter(id=Ad_id)
		staff = staff_registration.objects.all()
		return render(request, 'Admin_all_staffs.html',{'staff':staff,'pro':pro})
	else:
		return redirect('login')

def staff_delete(request,id):
	staff = staff_registration.objects.get(id=id)
	staff.delete()
	messages.success(request, 'deleted')
	return redirect('Admin_all_staffs')

def Admin_contact(request):
	if 'Ad_id' in request.session:
		if request.session.has_key('Ad_id'):
			Ad_id = request.session['Ad_id']
		else:
			variable = "dummy"
		pro = User.objects.filter(id=Ad_id)
		cou = contact_us.objects.filter( replay_status = 0 )
		return render(request, 'Admin_contact.html',{'pro':pro,'cou':cou})
	else:
		return redirect('login')

def contactus_replay(request,id):
	if request.method == 'POST':            
		cou = contact_us.objects.get(id=id)
		cou.replay=request.POST.get('rep')
		cou.replay_status = 1
		cou.save()
		subject = 'Greetings from warehouse'
		message =  str(cou.replay)
		recepient = str(cou.email)
		send_mail(subject, message, EMAIL_HOST_USER,
                  [recepient], fail_silently=False)
	return redirect('Admin_contact')

def Admin_departments(request):
	if 'Ad_id' in request.session:
		if request.session.has_key('Ad_id'):
			Ad_id = request.session['Ad_id']
		else:
			variable = "dummy"
		pro = User.objects.filter(id=Ad_id)
		dpt = department.objects.all()
		return render(request, 'Admin_departments.html',{'dpt':dpt,'pro':pro})
	else:
		return redirect('login')

def Admin_create_departments(request):
	if 'Ad_id' in request.session:
		if request.session.has_key('Ad_id'):
			Ad_id = request.session['Ad_id']
		else:
			variable = "dummy"
		pro = User.objects.filter(id=Ad_id)
		return render(request, 'Admin_create_dpt.html',{'pro':pro})
	else:
		return redirect('login')

def dpt_save(request):
	if request.method == 'POST':
		dpt = department()
		dpt.department_name = request.POST.get('dname')
		dpt.save()
	return redirect('Admin_departments')

# def Admin_storage(request):
# 	str = storage.objects.all()
# 	return render(request, 'Admin_storage.html',{'str':str})

# def Admin_create_storage(request):
# 	return render(request, 'Admin_create_storage.html')

# def storage_save(request):
# 	if request.method == 'POST':
# 		str = storage()
# 		str.storage_type = request.POST.get('stype')
# 		str.space = request.POST.get('tspace')
# 		str.save()
# 	return redirect('Admin_storage')

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

def Staff_change_password(request):
	if 'stf_id' in request.session:
		if request.session.has_key('stf_id'):
			stf_id = request.session['stf_id']
		else:
			variable = "dummy"
		mem1 = staff_registration.objects.filter(id = stf_id)
		return render(request, 'Staff_change_password.html', {'mem1': mem1})
	else:
		return redirect('/')

def Staff_changepwd_save(request):
	if 'stf_id' in request.session:
		if request.session.has_key('stf_id'):
			stf_id = request.session['stf_id']
		else:
			variable = "dummy"
		mem1 = staff_registration.objects.filter(id = stf_id)
		if request.method == 'POST':
			abc = staff_registration.objects.get(id=stf_id)
    
			oldps = request.POST['currentPassword']
			newps = request.POST['newPassword']
			cmps = request.POST.get('confirmPassword')
			if oldps != newps:
				if newps == cmps:
					abc.password = request.POST.get('confirmPassword')
					abc.save()
					return redirect('Staff_dashboard')
    
			elif oldps == newps:
				messages.add_message(request, messages.INFO, 'Current and New password same')
			else:
				messages.info(request, 'Incorrect password same')
    
			return redirect('Staff_change_password')
		return redirect('Staff_change_password')


def Admin_requests(request):
	if 'stf_id' in request.session:
		if request.session.has_key('stf_id'):
			stf_id = request.session['stf_id']
		else:
			variable = "dummy"
		mem1 = staff_registration.objects.filter(id = stf_id)
		req =order_request.objects.filter(staff_id=stf_id).filter(status='assigned').order_by('-id')
		return render(request, 'Admin_requests.html',{ 'mem1':mem1, 'req':req })
	else:
		return redirect('login')

def request_accept(request,id):
	req = order_request.objects.get(id=id)
	if request.method == 'POST':
		req.status = "accepted"
		req.rate = request.POST.get('rate')
		str = storage.objects.aggregate(Sum('space'))['space__sum']
		tq = order_request.objects.filter(Q(shipment_status='pending') | Q(shipment_status='Success')).aggregate(Sum('quantity'))['quantity__sum']
		cq = order_request.objects.filter(id=id).aggregate(Sum('quantity'))['quantity__sum']
		gt = (tq + cq)
		if ( str > gt):
			req.save()
		else:
			messages.success(request, 'warehouse does not have the requested storage available')
	return redirect( 'Admin_requests')

def request_reject(request,id):
	if request.method == 'POST':            
		req = order_request.objects.get(id=id)
		req.reject_reason=request.POST.get('reply')
		req.status='rejected'
		req.save()
	return redirect('Admin_requests')

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
		messages.success(request, 'updated successfully')
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
	if 'stf_id' in request.session:
		if request.session.has_key('stf_id'):
			stf_id = request.session['stf_id']
		else:
			variable = "dummy"
		mem1 = staff_registration.objects.filter(id = stf_id)
		req = order_request.objects.get(id = id)
		return render(request, 'Staff_tracking_update.html',{'req':req,'mem1':mem1})
	else:
		return redirect('login')

def Staff_tracking_update_save(request,id):
	if request.method == 'POST':
		req = order_request.objects.get(id = id)
		req.shipment_status = request.POST.get('sta')
		req.tracking_status = request.POST.get('Tdetails')
		req.save()
	return redirect('Staff_orders')


def Staff_statics(request):
	if 'stf_id' in request.session:
		if request.session.has_key('stf_id'):
			stf_id = request.session['stf_id']
		else:
			variable = "dummy"
		mem1 = staff_registration.objects.filter(id = stf_id)
		str = storage.objects.all()
		tq = order_request.objects.filter(Q(shipment_status='pending') | Q(shipment_status='Success')).aggregate(Sum('quantity'))['quantity__sum']
		return render(request, 'Staff_statics.html',{'str':str,'tq':tq,'mem1':mem1})
	else:
		return redirect('login')




