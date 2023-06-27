import uuid
from datetime import datetime, timedelta

from django.db import models


class User(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    email = models.CharField(
        unique=True, max_length=255, null=False, blank=False)
    password = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Freelancer(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='freelancer', null=True)
    freelancer_id = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    full_name = models.CharField(max_length=255, null=True)
    job_title = models.TextField(max_length=500, null=True)
    picture = models.URLField(null=True)
    phone_number = models.CharField(max_length=20, null=True)
    slack_username = models.CharField(max_length=255, null=True)
    linkedin_url = models.URLField(null=True)
    kaggle_url = models.URLField(null=True)
    github_url = models.URLField(null=True)
    iban = models.CharField(max_length=34, null=True)
    experience_in_years = models.FloatField(null=True)
    biography = models.TextField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Experience(models.Model):
    experience_id = models.IntegerField(null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    company_name = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    freelancer = models.ForeignKey(
        Freelancer, on_delete=models.CASCADE, related_name='experiences', null=True)


class Skill(models.Model):
    skill_id = models.IntegerField(null=True)
    name = models.CharField(max_length=255, null=True)
    experience = models.ForeignKey(
        Experience, on_delete=models.CASCADE, related_name='skills', null=True)
