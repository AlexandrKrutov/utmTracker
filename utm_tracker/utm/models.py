from django.db import models

# Create your models here.
class UserName(models.Model):
    user_name = models.CharField(max_length=30, unique=True, verbose_name='user_name')

    def __str__(self):
        return self.user_name

class UserProjects(models.Model):
    user_name = models.ForeignKey(UserName, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=30, verbose_name='project_name')

    def __str__(self):
        return self.project_name

class ProjectsUTM(models.Model):
    project_name = models.ForeignKey(UserProjects, on_delete=models.CASCADE)
    utm_campaign = models.CharField(max_length=100, unique=True, verbose_name='utm_campaign')
    utm_source = models.TextField(max_length=250, verbose_name='utm_source')
    utm_medium = models.CharField(max_length=100, verbose_name='utm_medium')

    utm_term = models.CharField(max_length=100, blank=True, default='Not specified', verbose_name='utm_term')
    utm_content = models.CharField(max_length=100, blank=True, default='Not specified', verbose_name='utm_content')

    utm_url = models.URLField(max_length=700, default='url', verbose_name='utm_url')

class UTMTracker(models.Model):
    utm_campaign = models.ForeignKey(ProjectsUTM, on_delete=models.CASCADE)
    event = models.IntegerField(default=1, verbose_name='event')
    date_time = models.DateTimeField(verbose_name='date_time')

