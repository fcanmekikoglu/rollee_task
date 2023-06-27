from rest_framework import serializers

from .models import Experience, Freelancer, Skill, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'freelancer', 'created_at', 'updated_at']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['skill_id', 'name']


class ExperienceSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Experience
        fields = ['experience_id', 'start_date', 'end_date',
                  'company_name', 'description', 'location', 'skills']


class FreelancerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freelancer
        fields = ['freelancer_id', 'email', 'first_name', 'last_name', 'full_name', 'job_title', 'picture', 'phone_number',
                  'slack_username', 'linkedin_url', 'kaggle_url', 'github_url', 'iban', 'biography', 'experience_in_years', 'created_at', 'updated_at']


class FreelancerDetailSerializer(serializers.ModelSerializer):
    experiences = ExperienceSerializer(many=True, read_only=True)

    class Meta:
        model = Freelancer
        fields = ['freelancer_id', 'email', 'first_name', 'last_name', 'full_name', 'job_title', 'biography',
                  'picture', 'phone_number', 'slack_username', 'linkedin_url', 'kaggle_url', 'github_url', 'iban', 'experience_in_years', 'experiences', 'created_at', 'updated_at']
