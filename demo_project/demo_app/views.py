from django.shortcuts import render
from django.http import HttpResponse
from demo_app.models import Department,Employee
from . import forms
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def index2(request):
    my_dict = {'data_var':'Here i am going to display !'}
    return render(request,'demo_app/hello_world.html',context=my_dict)

def index_car(request):
    return render(request,'demo_app/car_intro.html')

def index_nav(request):
    return render(request,'demo_app/index.html')

def index_other(request):
    return render(request,'demo_app/other.html')

def register_user(request):
    registered = False
    if request.method == 'POST':
        user_form = forms.UserForm(data=request.POST)
        profile_form = forms.UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password) # Hashing the password
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            print(request.FILES)
            if 'picture' in request.FILES:
                print(request.FILES['picture'])
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = forms.UserForm()
        profile_form = forms.UserProfileInfoForm()

    return render(request,'demo_app/registeration.html',
                  {'user_form':user_form,
                   'profile_form':profile_form,
                   'registered':registered})

def index_employee(request):
    list_emp = Employee.objects.order_by('ename')
    dict_emp = {'emp_records':list_emp}
    return render(request,'demo_app/employee_info.html',context=dict_emp)

def index_form(request):
    form_emp = forms.EmployeeForm()
    dict_form = {'form_emp': form_emp}

    if request.method == 'POST':
        form_emp = forms.EmployeeForm(request.POST)
        if form_emp.is_valid():
            print('Validation Succeed')
            print('Name' + form_emp.cleaned_data['name'])
            print('Designation' + form_emp.cleaned_data['desig'])
            print('Salary' + str(form_emp.cleaned_data['salary']))
            print('Joining Date' + str(form_emp.cleaned_data['doj']))

    return render(request,'demo_app/form_emp.html',context=dict_form)

def index_welcome(request):
    return render(request, 'demo_app/emp_welcome.html')

def index_form_submit(request):
    form_emp = forms.EmployeeForm()
    dict_form = {'form_emp': form_emp}

    if request.method == 'POST':
        form_emp = forms.EmployeeForm(request.POST)
        if form_emp.is_valid():
            form_emp.save(commit=True)
            return index_welcome(request)
        else:
            print('Invalid Entry!!')

    return render(request, 'demo_app/form_emp.html', context=dict_form)

def login_user(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        print('Debug ******')
        print(user)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('demo_app:index_navigation'))
            else:
                return HttpResponse('Account not Active!!')
        else:
            print('Login failed!!')
            return HttpResponse('Invalid login details entered!')
    else:
        return render(request, 'demo_app/login.html',{})

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('demo_app:index_navigation'))

@login_required
def special(request):
    return HttpResponse('You are logged in, Nice!')