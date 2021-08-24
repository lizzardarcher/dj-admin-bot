from django.shortcuts import render, redirect
from slivki_bot.forms import EmployeeForm, UsersForm, MessagesForm
from slivki_bot.models import Employee, Users, Messages


# Create your views here.
def emp(request):
    if request.method == "POST":
        form = MessagesForm(request.POST)
        if form.is_valid():
            print('------form is valid------')
            try:
                form.save()
                return redirect('/show')
            except:
                pass
    else:
        print('------form is invalid------')
        form = MessagesForm()
    return render(request, 'index.html', {'form': form})


def show(request):
    messages = Messages.objects.all()
    return render(request, "show.html",
                  {'messages': messages})


def edit(request, id):
    messages = Messages.objects.get(msg_id=id)
    return render(request, 'edit.html',
                  {'messages': messages})


def update(request, id):
    messages = Messages.objects.get(msg_id=id)
    form = MessagesForm(request.POST, instance=messages)
    print('Form is valid'+form.is_valid())
    if form.is_valid():
        form.save()
        return redirect("/show")
    return render(request, 'edit.html',
                  {'messages': messages})


def destroy(request, id):
    messages = Messages.objects.get(msg_id=id)
    messages.delete()
    return redirect("/show")
