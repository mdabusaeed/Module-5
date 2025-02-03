from django import forms
from tasks.models import Task, TaskDetails

# Django Form

class TaskForm(forms.Form):
    title = forms.CharField(max_length=250,label='Task Titile')
    description = forms.CharField(widget=forms.Textarea,label='Task description')
    due_date = forms.DateField(widget=forms.SelectDateWidget,label='Due Date')
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[],label='Assigned To')

    def __init__(self, *args, **kwargs):
        employees = kwargs.pop("employees", [])
        # print(employees)  
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [
            (emp.id,emp.name) for emp in employees]
        
# django Model Form
 
class StyleForMixin:
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_style_widged()
        
    default_classes = "border-2 border-blue-300 w-full px-4 py-2 rounded-lg shadow-md bg-gradient-to-r from-blue-100 to-blue-200 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500 transition duration-300"
    def apply_style_widged(self):
        for field_name,field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder':f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder':f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': "border-2 border-green-300 px-4 py-2 rounded-lg shadow-md bg-gradient-to-r from-green-100 to-green-200 focus:outline-none focus:border-green-500 focus:ring-2 focus:ring-green-500 transition duration-300"
                })

            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "space-y-2 border-2 border-pink-300 rounded-lg shadow-md bg-pink-100 focus:outline-none focus:ring-2 focus:ring-pink-500"
                })
            else:

                field.widget.attrs.update({
                    'class': self.default_classes
                })

class TaskModelForm(StyleForMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date','assigned_to'] 
        widgets = {
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_style_widged()

class TaskDetailModelForm(StyleForMixin,forms.ModelForm):
    class Meta:
        model = TaskDetails
        fields = ['priority','notes', 'asset']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_style_widged()