from django.shortcuts import render
import threading
import json
import requests
from django.core import serializers
from .models import *
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.db.models import Count
from django.views.decorators.cache import never_cache
from django.core.files.storage import FileSystemStorage
import os
from datetime import date
from datetime import datetime
import re
from .checks import *
# Create your views here.

@never_cache
def display_login(request):
	return render(request, "login_register.html", {})

@never_cache
def check_login(request):
	username = request.POST.get("name")
	password = request.POST.get("pass")
	user_type = request.POST.get("user_type")
	if user_type=="Select User Type":
		return HttpResponse("<script>alert('Please Select User Type');window.location.href='/display_login/';</script>")
	
	else:
		if username == "admin" and password == "admin" and user_type=="Admin":
			request.session['uid'] = "admin"
			return HttpResponse("<script>alert('Login Successful');window.location.href='/show_home_admin/';</script>")
		else:
			if user_type=="Voter":
				obj2=Users.objects.filter(Username=username,Password=password)
				c2=obj2.count()
				if c2==1:
					ob=Users.objects.get(Username=username,Password=password)
					request.session['username'] = username
					request.session['uid'] = ob.S_id
					return HttpResponse("<script>alert('Login Successful');window.location.href='/show_home_voter/';</script>")
				else:
					return HttpResponse("<script>alert('Invalid');window.location.href='/display_login/';</script>")

			elif user_type=="Candidate":
				obj2=Users.objects.filter(Username=username,Password=password)
				c2=obj2.count()
				if c2==1:
					ob=Users.objects.get(Username=username,Password=password)
					request.session['username'] = username
					request.session['uid'] = ob.S_id
					return HttpResponse("<script>alert('Login Successful');window.location.href='/show_home_candidate/';</script>")
				else:
					return HttpResponse("<script>alert('Invalid');window.location.href='/display_login/';</script>")

			elif user_type=="Election Committee":
				obj2=Users.objects.filter(Username=username,Password=password)
				c2=obj2.count()
				if c2==1:
					ob=Users.objects.get(Username=username,Password=password)
					request.session['username'] = username
					request.session['uid'] = ob.S_id
					return HttpResponse("<script>alert('Login Successful');window.location.href='/show_home_election_committee/';</script>")
				else:
					return HttpResponse("<script>alert('Invalid');window.location.href='/display_login/';</script>")
			


				
##########################################################################################
#Admin
@never_cache
def show_home_admin(request):
	if 'uid' in request.session:
		return render(request, 'home_admin.html')
	else:
		return render(request, 'login_register.html')

@never_cache
def show_home_voter(request):
	if 'uid' in request.session:
		username=request.session['username']
		return render(request, 'home_voter.html',{'name':username})
	else:
		return render(request, 'login_register.html')

@never_cache
def show_home_candidate(request):
	if 'uid' in request.session:
		username=request.session['username']
		return render(request, 'home_candidate.html',{'name':username})
	else:
		return render(request, 'login_register.html')

@never_cache
def show_home_election_committee(request):
	if 'uid' in request.session:
		username=request.session['username']
		return render(request, 'home_election_committee.html',{'name':username})
	else:
		return render(request, 'login_register.html')




@never_cache
def display_nomination(request):
	if 'uid' in request.session:
		return render(request, 'display_nomination.html')
	else:
		return render(request, 'login_register.html')

@never_cache
def logout(request):
	if 'uid' in request.session:
		del request.session['uid']
	return render(request, 'login_register.html')

@never_cache
def register(request):
	user_type=request.POST.get("user_type")
	username = request.POST.get("uname")
	email=request.POST.get("email")
	password = request.POST.get("pswd")
	phn = request.POST.get("phone")
	if user_type=="Select User Type":
		return HttpResponse("<script>alert('Please Select User Type');window.location.href='/display_login/';</script>")
	else:
		obj10 = Requests.objects.filter(
			Username=username, Email=email, Password=password,Phone=phn,user_type=user_type)
		co = obj10.count()
		if co == 1:
			return HttpResponse("<script>alert('Request is already sended, please wait for approval');window.location.href='/display_login/'</script>")
		else:
			obj1 = Requests(Username=username,Email=email, Password=password,Phone=phn,user_type=user_type)
			obj1.save()
			return HttpResponse("<script>alert('Registration request sended successfully, please wait for approval');window.location.href='/display_login/'</script>")



from datetime import datetime
from django.utils import timezone
@never_cache
def do_vote(request): 
	candidate_name=request.POST.get("candidate_name")
	u_id = request.session.get('uid')
	vote_time_obj = Vote_Time.objects.first()
	
	if vote_time_obj:
		start_time_str = vote_time_obj.s_time
		end_time_str = vote_time_obj.e_time
		print(start_time_str)
		print(type(start_time_str))

		start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
		end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

		print(start_time)
		print(end_time)

		# Get the current time
		current_time = datetime.now()

		# Format current_time to match start_time and end_time
		current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
		print("*********")
		print(current_time)
		print(type(current_time))


		# Check if the current time is within the voting time range
		if start_time <= current_time <= end_time:
			obj10 = Vote.objects.filter(get_id=u_id)
			co = obj10.count()
			if co == 1:
				return HttpResponse("<script>alert('Already Voted');window.location.href='/show_home_voter/'</script>")
			else:
				obj1 = Vote(candidate_name=candidate_name,get_id=u_id)
				obj1.save()
				return HttpResponse("<script>alert('Voted successfully');window.location.href='/show_home_voter/'</script>")
		else:
			return HttpResponse("<script>alert('Voting time Mismatch');window.location.href='/show_home_voter/'</script>")
	else:
		return HttpResponse("<script>alert('Voting time not set');window.location.href='/show_home_voter/'</script>")

@never_cache
def perform_do_vote(request): 
	candidate_name=request.POST.get("candidate_name")
	u_id = request.session.get('uid')
	vote_time_obj = Vote_Time.objects.first()
	
	if vote_time_obj:
		start_time_str = vote_time_obj.s_time
		end_time_str = vote_time_obj.e_time
		print(start_time_str)
		print(type(start_time_str))

		start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
		end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

		print(start_time)
		print(end_time)

		# Get the current time
		current_time = datetime.now()

		# Format current_time to match start_time and end_time
		current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
		print("*********")
		print(current_time)
		print(type(current_time))


		# Check if the current time is within the voting time range
		if start_time <= current_time <= end_time:
			obj10 = Vote.objects.filter(get_id=u_id)
			co = obj10.count()
			if co == 1:
				return HttpResponse("<script>alert('Already Voted');window.location.href='/show_home_candidate/'</script>")
			else:
				obj1 = Vote(candidate_name=candidate_name,get_id=u_id)
				obj1.save()
				return HttpResponse("<script>alert('Voted successfully');window.location.href='/show_home_candidate/'</script>")
		else:
			return HttpResponse("<script>alert('Voting time Mismatch');window.location.href='/show_home_candidate/'</script>")
	else:
		return HttpResponse("<script>alert('Voting time not set');window.location.href='/show_home_candidate/'</script>")



@never_cache
def submit_vote_time(request):
	s_time_str=request.POST.get("startDateTime")
	print(s_time_str)
	print(type(s_time_str))
	e_time_str = request.POST.get("endDateTime")
	print(e_time_str)
	print(type(e_time_str))

	# Convert string representation to datetime object
	s_time = datetime.strptime(s_time_str, "%Y-%m-%dT%H:%M")
	e_time = datetime.strptime(e_time_str, "%Y-%m-%dT%H:%M")

	print(e_time)
	print(type(e_time))
	obj10 = Vote_Time.objects.all()
	
	if obj10.exists():
		# If a voting time entry already exists, update it
		obj1 = obj10.first()  # Assuming there's only one entry
		obj1.s_time = s_time
		obj1.e_time = e_time
		obj1.save()
		return HttpResponse("<script>alert('Vote Timing Updated Successfully');window.location.href='/render_set_vote_time/'</script>")
	else:
		# If no entry exists, create a new one
		obj1 = Vote_Time(s_time=s_time, e_time=e_time)
		obj1.save()
		return HttpResponse("<script>alert('Vote Timing Set Successfully');window.location.href='/render_set_vote_time/'</script>")


@never_cache
def view_requests(request):
	if 'uid' in request.session:
		mlist=Requests.objects.all()
		return render(request,'vrequest.html',{'req': mlist}) 
	else:
		return render(request,'login_register.html')

@never_cache
def render_set_vote_time(request):
	if 'uid' in request.session:
		return render(request,'render_set_vote_time.html') 
	else:
		return render(request,'login_register.html')

@never_cache
def view_candidates(request):
	if 'uid' in request.session:
		mlist=Nomination.objects.filter(status="Approved")
		return render(request,'view_candidates_ec.html',{'req': mlist}) 
	else:
		return render(request,'login_register.html')


@never_cache
def dis_vote_page_voter(request):
	if 'uid' in request.session:
		# Get the voting time from the Vote_Time table
		vote_time_obj = Vote_Time.objects.first()  # Assuming there is only one entry

		# Check if a voting time entry exists
		if vote_time_obj:
			start_time = vote_time_obj.s_time
			end_time = vote_time_obj.e_time

			mlist = Nomination.objects.filter(status="Approved")
			
			# Add voting time to the dictionary for rendering
			context = {'req': mlist, 'start_time': start_time, 'end_time': end_time}

			return render(request, 'dis_vote_page_voter.html', context)
		else:

			return HttpResponse("<script>alert('Voting time not set. Please wait for it.');window.location.href='/show_home_voter/'</script>")
	else:
		return render(request, 'login_register.html')



@never_cache
def visible_vote_page_candidate(request):
	if 'uid' in request.session:
		# Get the voting time from the Vote_Time table
		vote_time_obj = Vote_Time.objects.first()  # Assuming there is only one entry

		# Check if a voting time entry exists
		if vote_time_obj:
			start_time = vote_time_obj.s_time
			end_time = vote_time_obj.e_time

			mlist = Nomination.objects.filter(status="Approved")
			
			# Add voting time to the dictionary for rendering
			context = {'req': mlist, 'start_time': start_time, 'end_time': end_time}

			return render(request, 'visible_vote_page_candidate.html', context)
		else:

			return HttpResponse("<script>alert('Voting time not set. Please wait for it.');window.location.href='/show_home_candidate/'</script>")
	else:
		return render(request, 'login_register.html')





@never_cache
def show_candidates_list(request):
	if 'uid' in request.session:
		mlist=Nomination.objects.filter(status="Approved")
		return render(request,'view_candidates_admin.html',{'req': mlist}) 
	else:
		return render(request,'login_register.html')

@never_cache
def preview_candidates_list_candidate(request):
	if 'uid' in request.session:
		mlist=Nomination.objects.filter(status="Approved")
		return render(request,'view_candidates_candidate.html',{'req': mlist}) 
	else:
		return render(request,'login_register.html')

@never_cache
def voter_view_candidates(request):
	if 'uid' in request.session:
		mlist=Nomination.objects.filter(status="Approved")
		return render(request,'view_candidates_voter.html',{'req': mlist}) 
	else:
		return render(request,'login_register.html')

@never_cache
def view_vote_result(request):
	if 'uid' in request.session:

		vote_time_obj = Vote_Time.objects.first()  # Assuming there is only one entry

		# Check if a voting time entry exists
		if vote_time_obj:
			start_time = vote_time_obj.s_time
			end_time = vote_time_obj.e_time
			
			# Add voting time to the dictionary for rendering
		return render(request,'view_voting_result_admin.html',{'start_time': start_time, 'end_time': end_time}) 
	else:
		return render(request,'login_register.html')

from django.db.models import Count

def publish_vote_result(request):

	vote_time_obj1 = Vote_Time.objects.first()
	vote_time_obj1.status="Published"
	vote_time_obj1.save()
	vote_time_obj = Vote_Time.objects.first()
	if vote_time_obj:
		end_time_str = vote_time_obj.e_time
		end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

		# Get the current time
		current_time = datetime.now()

		if current_time > end_time:
			# Determine the highest vote count
			vote_counts = Vote.objects.values('candidate_name').annotate(count=Count('candidate_name'))

			max_vote_count = max(vote_counts, key=lambda x: x['count'])['count']

			# Find all candidates with the highest vote count
			winners = [candidate for candidate in vote_counts if candidate['count'] == max_vote_count]
			print('****************')
			print(winners)
			print("^^^^^^^^^^^^^")
			print(vote_counts)
			context = {
				'vote_counts': vote_counts,
				'winners': winners,
			}
			# Voting has ended
			# Query to get the vote count for each candidate
			vote_counts = Vote.objects.values('candidate_name').annotate(count=Count('candidate_name'))

			return render(request, 'vote_result.html', context)
		else:
			return HttpResponse("<script>alert('Voting is still ongoing.');window.location.href='/show_home_admin/'</script>")
	else:
		return HttpResponse("<script>alert('Voting time not set.');window.location.href='/show_home_admin/'</script>")


def get_vote_result(request):

	vote_time_obj1 = Vote_Time.objects.first()
	get_status=vote_time_obj1.status
	if get_status!="Published":
		return HttpResponse("<script>alert('Results not Published');window.location.href='/show_home_election_committee/'</script>")
	else:
		vote_time_obj = Vote_Time.objects.first()
		if vote_time_obj:
			end_time_str = vote_time_obj.e_time
			end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

			# Get the current time
			current_time = datetime.now()

			if current_time > end_time:
				# Determine the highest vote count
				vote_counts = Vote.objects.values('candidate_name').annotate(count=Count('candidate_name'))

				max_vote_count = max(vote_counts, key=lambda x: x['count'])['count']

				# Find all candidates with the highest vote count
				winners = [candidate for candidate in vote_counts if candidate['count'] == max_vote_count]
				print('****************')
				print(winners)
				print("^^^^^^^^^^^^^")
				print(vote_counts)
				context = {
					'vote_counts': vote_counts,
					'winners': winners,
				}
				# Voting has ended
				# Query to get the vote count for each candidate
				vote_counts = Vote.objects.values('candidate_name').annotate(count=Count('candidate_name'))

				return render(request, 'vote_result.html', context)
			else:
				return HttpResponse("<script>alert('Voting is still ongoing.');window.location.href='/show_home_election_committee/'</script>")
		else:
			return HttpResponse("<script>alert('Voting time not set.');window.location.href='/show_home_election_committee/'</script>")



def reveal_result_voter(request):

	vote_time_obj1 = Vote_Time.objects.first()
	get_status=vote_time_obj1.status
	if get_status!="Published":
		return HttpResponse("<script>alert('Results not Published');window.location.href='/show_home_voter/'</script>")
	else:
		vote_time_obj = Vote_Time.objects.first()
		if vote_time_obj:
			end_time_str = vote_time_obj.e_time
			end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

			# Get the current time
			current_time = datetime.now()

			if current_time > end_time:
				# Determine the highest vote count
				vote_counts = Vote.objects.values('candidate_name').annotate(count=Count('candidate_name'))

				max_vote_count = max(vote_counts, key=lambda x: x['count'])['count']

				# Find all candidates with the highest vote count
				winners = [candidate for candidate in vote_counts if candidate['count'] == max_vote_count]
				print('****************')
				print(winners)
				print("^^^^^^^^^^^^^")
				print(vote_counts)
				context = {
					'vote_counts': vote_counts,
					'winners': winners,
				}
				# Voting has ended
				# Query to get the vote count for each candidate
				vote_counts = Vote.objects.values('candidate_name').annotate(count=Count('candidate_name'))

				return render(request, 'vote_result.html', context)
			else:
				return HttpResponse("<script>alert('Voting is still ongoing.');window.location.href='/show_home_voter/'</script>")
		else:
			return HttpResponse("<script>alert('Voting time not set.');window.location.href='/show_home_voter/'</script>")



def exhibit_result_candidate(request):

	vote_time_obj1 = Vote_Time.objects.first()
	get_status=vote_time_obj1.status
	if get_status!="Published":
		return HttpResponse("<script>alert('Results not Published');window.location.href='/show_home_candidate/'</script>")
	else:
		vote_time_obj = Vote_Time.objects.first()
		if vote_time_obj:
			end_time_str = vote_time_obj.e_time
			end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

			# Get the current time
			current_time = datetime.now()

			if current_time > end_time:
				# Determine the highest vote count
				vote_counts = Vote.objects.values('candidate_name').annotate(count=Count('candidate_name'))

				max_vote_count = max(vote_counts, key=lambda x: x['count'])['count']

				# Find all candidates with the highest vote count
				winners = [candidate for candidate in vote_counts if candidate['count'] == max_vote_count]
				print('****************')
				print(winners)
				print("^^^^^^^^^^^^^")
				print(vote_counts)
				context = {
					'vote_counts': vote_counts,
					'winners': winners,
				}
				# Voting has ended
				# Query to get the vote count for each candidate
				vote_counts = Vote.objects.values('candidate_name').annotate(count=Count('candidate_name'))

				return render(request, 'vote_result.html', context)
			else:
				return HttpResponse("<script>alert('Voting is still ongoing.');window.location.href='/show_home_candidate/'</script>")
		else:
			return HttpResponse("<script>alert('Voting time not set.');window.location.href='/show_home_candidate/'</script>")





@never_cache
def view_donation_requests(request):
	if 'uid' in request.session:
		mlist=Donators.objects.filter(status="pending")
		return render(request,'vdrequest.html',{'req': mlist}) 
	else:
		return render(request,'login_register.html')


@never_cache
def accept(request):
	n_id=request.POST.get('n_id')
	obj1=Nomination.objects.get(n_id=int(n_id))
	obj1.status="HOD"
	obj1.save()
	return HttpResponse("<script>alert('Nomination Approved by HOD');window.location.href='/show_first_nomination/'</script>")

@never_cache
def drop(request):
	n_id=request.POST.get('n_id')
	obj1=Nomination.objects.get(n_id=int(n_id))
	obj1.delete()
	return HttpResponse("<script>alert('Nomination Rejected Successfully');window.location.href='/show_first_nomination/'</script>")

@never_cache
def sd_accept(request):
	n_id=request.POST.get('n_id')
	obj1=Nomination.objects.get(n_id=int(n_id))
	obj1.status="SD"
	obj1.save()
	return HttpResponse("<script>alert('Nomination Approved by Student Dean');window.location.href='/view_second_nomination/'</script>")

@never_cache
def sd_drop(request):
	n_id=request.POST.get('n_id')
	obj1=Nomination.objects.get(n_id=int(n_id))
	obj1.delete()
	return HttpResponse("<script>alert('Nomination Rejected Successfully');window.location.href='/view_second_nomination/'</script>")


@never_cache
def eic_accept(request):
	n_id=request.POST.get('n_id')
	obj1=Nomination.objects.get(n_id=int(n_id))
	obj1.status="EIC"
	obj1.save()
	return HttpResponse("<script>alert('Nomination Approved by Election in Charge');window.location.href='/for_third_nomination/'</script>")

@never_cache
def eic_drop(request):
	n_id=request.POST.get('n_id')
	obj1=Nomination.objects.get(n_id=int(n_id))
	obj1.delete()
	return HttpResponse("<script>alert('Nomination Rejected Successfully');window.location.href='/for_third_nomination/'</script>")

@never_cache
def principal_accept(request):
	n_id=request.POST.get('n_id')
	obj1=Nomination.objects.get(n_id=int(n_id))
	obj1.status="Approved"
	obj1.save()
	return HttpResponse("<script>alert('Nomination Approved by Principal');window.location.href='/principal_forth_nomination/'</script>")

@never_cache
def principal_drop(request):
	n_id=request.POST.get('n_id')
	obj1=Nomination.objects.get(n_id=int(n_id))
	obj1.delete()
	return HttpResponse("<script>alert('Nomination Rejected Successfully');window.location.href='/principal_forth_nomination/'</script>")


@never_cache
def show_first_nomination(request):
	if 'uid' in request.session:
		mlist=Nomination.objects.filter(status="Pending")
		return render(request, 'show_first_nomination.html',{'req': mlist})
	else:
		return render(request, 'login_register.html')


@never_cache
def view_second_nomination(request):
	if 'uid' in request.session:
		mlist=Nomination.objects.filter(status="HOD")
		return render(request, 'view_second_nomination.html',{'req': mlist})
	else:
		return render(request, 'login_register.html')

@never_cache
def for_third_nomination(request):
	if 'uid' in request.session:
		mlist=Nomination.objects.filter(status="SD")
		return render(request, 'for_third_nomination.html',{'req': mlist})
	else:
		return render(request, 'login_register.html')

@never_cache
def principal_forth_nomination(request):
	if 'uid' in request.session:
		mlist=Nomination.objects.filter(status="EIC")
		return render(request, 'principal_forth_nomination.html',{'req': mlist})
	else:
		return render(request, 'login_register.html')



@never_cache
def approve1(request):
	S_id=request.POST.get('S_id')
	Username=request.POST.get('Username')
	email=request.POST.get('Email')
	password=request.POST.get('Password')
	phn=request.POST.get('Phone')
	user_type=request.POST.get("user_type")
	obj10 = Users.objects.filter(
			Username=Username, Email=email, Password=password,Phone=phn,user_type=user_type)
	co = obj10.count()
	if co==1:
		obj1=Requests.objects.get(S_id=int(S_id))
		obj1.delete()
		return HttpResponse("<script>alert('User already existed');window.location.href='/view_requests/'</script>")
	else:		
		obj1=Users(
			Username=Username, Email=email, Password=password,Phone=phn,user_type=user_type)
		obj1.save()
		S_id=int(S_id)
		obj3=Requests.objects.get(S_id=int(S_id))
		obj3.delete()
		return HttpResponse("<script>alert('Approved Successfully');window.location.href='/view_requests/'</script>")

@never_cache
def reject1(request):
	S_id=request.POST.get('S_id')
	obj1=Requests.objects.get(S_id=int(S_id))
	obj1.delete()
	return HttpResponse("<script>alert('Rejected Successfully');window.location.href='/view_requests/'</script>")




@never_cache
def nomination_submission(request):
	private_key=request.POST.get('private_key')
	candidate_name=request.POST.get('full_name')
	candidate_dob=request.POST.get('date_of_birth')
	candidate_email=request.POST.get('email')
	candidate_phone=request.POST.get('phone')
	candidate_department=request.POST.get('department')
	candidate_gender=request.POST.get('gender')
	candidate_address=request.POST.get('address')
	statement_of_intent=request.POST.get('statement_of_intent')
	candidate_image=request.FILES["photo"]
	pub_key=request.session["pub_key"]
	file_name=candidate_image.name

	if Nomination.objects.filter(candidate_name=candidate_name).exists():
		return HttpResponse("<script>alert('Nomination already Submitted');window.location.href='/display_nomination/'</script>")

	else:
		folder_path = "block_vote_app/static/candidate_images"
		if not os.path.exists(folder_path):
			os.makedirs(folder_path)
		image_path = os.path.join(folder_path, file_name)
		fs = FileSystemStorage(location=folder_path)
		fs.save(file_name, candidate_image)

		obj4=Nomination(candidate_name=candidate_name,candidate_dob=candidate_dob,candidate_email=candidate_email,
			candidate_phone=candidate_phone,candidate_department=candidate_department,candidate_gender=candidate_gender,
			candidate_address=candidate_address,statement_of_intent=statement_of_intent,candidate_image=file_name)
		obj4.save()

		return HttpResponse("<script>alert('Nomination Submitted Successfully');window.location.href='/display_nomination/'</script>")





###################################################################################################################
###################################################################################################################


