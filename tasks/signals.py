from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Task, TaskDetails


@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_employees_task_creation(sender, instance, action, **kwargs):

    if action == "post_add":
        assigned_employees = [emp.email for emp in instance.assigned_to.all() if emp.email]

        if assigned_employees:

            send_mail(
                "New Task Created",
                f"A new task '{instance.title}' has been created and assigned to you.",
                "abu.saeed.nicl@gmail.com",
                assigned_employees,
                fail_silently=False, 
            )



@receiver(post_delete, sender=Task)
def employees_task_deletion(sender, instance, **kwargs):
    if instance.details:
        instance.details.delete()
        print("🗑 Task Details Deleted!")
