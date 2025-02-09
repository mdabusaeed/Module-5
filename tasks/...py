
@login_required
@permission_required('tasks.change_task', login_url='no-permission')
def update_task(request,id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance = task)
    
    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details)    

    if request.method == 'POST':
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetailModelForm(request.POST, instance=task.details)
        if task_form.is_valid() and task_detail_form.is_valid():

            ''' For Model Form Data '''
            task_form = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task  = task
            task_detail_form.save()

            messages.success(request, "Task Updated Successfully")
            return redirect('update-task', id)

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request,"task_form.html",context)


class CreateTask(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'tasks.add_task'
    login_url = 'sign-in'

    template_name = 'task_form.html'

    def get(self, request, *args, **kwargs):
        task_form = TaskModelForm()
        task_detail_form = TaskDetailModelForm()

        context = {"task_form": task_form, "task_detail_form": task_detail_form}
        return render(request,self.template_name,context)

    def post(self, request, *args, **kwargs):
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)

        if task_form.is_valid() and task_detail_form.is_valid():

            ''' For Model Form Data '''
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task  = task
            task_detail.save()

            messages.success(request, "Task Created Successfully")
            return redirect('create-task')