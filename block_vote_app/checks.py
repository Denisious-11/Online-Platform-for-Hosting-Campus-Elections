from .models import *
from django.http import HttpResponse, JsonResponse

def delete_data(request):
	obj1=Requests.objects.all().delete()
	obj2=Users.objects.all().delete()
	obj3=Patient.objects.all().delete()
	obj4=Donators.objects.all().delete()

	return HttpResponse("<script>alert('Data Deleted Successfully');window.location.href='/show_home_admin/'</script>")