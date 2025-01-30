from django.db import models
from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name #Dunder Method

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()

    def __str__(self):
        return self.name

# Create your models here.
class Task(models.Model):
    STATUS_CHOICES=[
        ('PENDING','Pending'),
        ('IN_PROGRESS','In Progress'),
        ('COMPLETED','Completed')
    ]

    project = models.ForeignKey(
        'Project', 
        on_delete=models.CASCADE,
        default=1
        ) 

    assigned_to = models.ManyToManyField(Employee)
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='PENDING')
    is_completed = models.BooleanField(default=False) 
    created_task = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    


class TaskDetails(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'

    PRIORITY_OPTIONS = (
        (HIGH , 'High'),
        (MEDIUM , 'Medium'),
        (LOW , 'Low')
    )

    task = models.OneToOneField(
        Task, 
        # on_delete=models.CASCADE,
        on_delete=models.DO_NOTHING,
        related_name='details',
        )
    # assigned_to = models.CharField(max_length=100)
    priority = models.CharField(
        max_length=1, choices=PRIORITY_OPTIONS, default = LOW
        ) 
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Details for Task {self.task.title}"


# Notify the user when a new task is created
@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_employees_task_creation(sender, instance, action, **kwargs):
    print(f"🔥 Signal Triggered! Action: {action}")  # Debugging output

    if action == "post_add":
        assigned_employees = [emp.email for emp in instance.assigned_to.all() if emp.email]

        print(f"📨 Assigned Employees: {assigned_employees}")  # Debugging output

        if assigned_employees:
            print("🚀 Sending Email...")
            send_mail(
                "New Task Created",
                f"A new task '{instance.title}' has been created and assigned to you.",
                "abu.saeed.nicl@gmail.com",
                assigned_employees,
                fail_silently=False,  # Ensure errors are not ignored
            )
            print("✅ Email Sent!")



@receiver(post_delete, sender=Task)
def employees_task_deletion(sender, instance, **kwargs):
    if instance.details:
        instance.details.delete()
        print("🗑 Task Details Deleted!")
