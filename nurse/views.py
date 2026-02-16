from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from smart_hospital.permissions import group_required
from .models import Nurse
from .forms import NurseForm


def index(request):
    nurses = Nurse.objects.all()
    return render(request, 'nurse/index.html', {'nurses': nurses})


@login_required
@group_required('Admin')
def create(request):
    if request.method == 'POST':
        form = NurseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nurse:index')
    else:
        form = NurseForm()
    return render(request, 'nurse/form.html', {'form': form, 'title': 'Add Nurse'})


@login_required
@group_required('Admin')
def update(request, pk):
    obj = get_object_or_404(Nurse, pk=pk)
    if request.method == 'POST':
        form = NurseForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('nurse:index')
    else:
        form = NurseForm(instance=obj)
    return render(request, 'nurse/form.html', {'form': form, 'title': 'Edit Nurse'})


@login_required
@group_required('Admin')
def delete(request, pk):
    obj = get_object_or_404(Nurse, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('nurse:index')
    return render(request, 'nurse/confirm_delete.html', {'object': obj, 'title': 'Delete Nurse'})
