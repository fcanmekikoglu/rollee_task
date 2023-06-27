import json
from datetime import datetime

import requests

from .models import Experience, Freelancer, Skill, User


def login(email, password):
    query = """
        mutation authenticate($email: EmailType!, $password: String!, $signupToken: String) {
            authenticate(email: $email, password: $password, signupToken: $signupToken) {
                id
            }
        }
        """

    variables = {
        "email": email,
        "password": password,
        "signupToken": None
    }

    data = {
        "query": query,
        "variables": variables
    }

    response = requests.post('https://api.comet.co/api/graphql', json=data)

    status_code = response.status_code

    json_response = response.json()

    if status_code != 200 or 'errors' in json_response:
        error_message = json_response['errors'][0]['message']
        return {"error": error_message}

    user_data = json_response['data']['authenticate']
    return user_data

def get_user(email, password):
    query = """
        mutation authenticate($email: EmailType!, $password: String!, $signupToken: String) {
            authenticate(email: $email, password: $password, signupToken: $signupToken) {
                id
                ...User
                __typename
            }
        }

        fragment User on User {
            id
            email
            firstName
            fullName
            jobTitle
            lastName
            pendingActivation
            phoneNumber
            profilePictureUrl
            slackId
            slackUsername
            termsValidated
            termsValidatedAt
            unreadChatMessagesCount
            unseenMentionsCount
            mentionsViewedAt
            corporate {
                id
                comments
                companyId
                role
                token
                missions {
                    id
                    count
                    __typename
                }
                missionPendingRating {
                    id
                    __typename
                }
                company {
                    id
                    skipTermsValidation
                    __typename
                }
                __typename
            }
            freelance {
                id
                preUser
                isInstructor
                flaggedForQualif
                isFrozen
                isQualified
                acquisitionSource
                availabilityDate
                bankName
                bic
                bitbucketUrl
                callAvailability
                gitHubUrl
                gitlabUrl
                iban
                isAvailable
                isBillable
                kaggleUrl
                linkedInUrl
                shouldUpdateAvailability
                maxDistance
                prefContract
                prefEnvironment
                prefMobility
                prefTime
                prefWorkplace
                profileScore
                publicId
                referralCode
                retribution
                retryDate
                stackExchangeUrl
                status
                talentSuccessManagerId
                twitterUrl
                websiteUrl
                slackStatus
                ...LinkedInImport
                __typename
            }
            teamMember {
                id
                accountManager
                freelancerAgent
                ...TeamMemberTip
                __typename
            }
            impersonating {
                id
                email
                firstName
                lastName
                fullName
                teamMember {
                    id
                    __typename
                }
                __typename
            }
            ...FreelancerNavBar
            ...UserFlags
            ...CorporatePermissions
            ...FreelancePermissions
            __typename
        }

        fragment TeamMemberTip on TeamMember {
            id
            tips
            __typename
        }

        fragment UserFlags on User {
            id
            corporate {
                id
                ...CorporateFlags
                __typename
            }
            freelance {
                id
                ...FreelancerFlags
                __typename
            }
            __typename
        }

        fragment CorporateFlags on Corporate {
            id
            flags {
                id
                ...Flag
                __typename
            }
            __typename
        }

        fragment Flag on Flag {
            id
            level
            once
            payload
            permanent
            type
            __typename
        }

        fragment FreelancerFlags on Freelance {
            id
            flags {
                id
                ...Flag
                __typename
            }
            __typename
        }

        fragment FreelancerNavBar on User {
            id
            slackId
            profilePictureUrl
            unreadChatMessagesCount
            freelance {
                id
                status
                __typename
            }
            __typename
        }

        fragment CorporatePermissions on User {
            id
            permissions {
                id
                showProfile
                showMissions
                showAdministration
                showCommunity
                showCrew
                __typename
            }
            __typename
        }

        fragment FreelancePermissions on User {
            id
            permissions {
                id
                showProfile
                showMissions
                showStore
                showInfos
                showExperiences
                showQualification
                showInstructor
                askForQualification
                showPreferences
                showCompany
                __typename
            }
            __typename
        }

        fragment LinkedInImport on Freelance {
            id
            fetchingLinkedIn
            lastLinkedInImport {
                id
                status
                lastError
                importedAt
                __typename
            }
            biography
            user {
                id
                profilePictureUrl
                jobTitle
                __typename
            }
            experienceInYears
            experiences {
                id
                isCometMission
                startDate
                endDate
                companyName
                description
                location
                skills {
                    id
                    name
                    primary
                    freelanceExperienceSkillId
                    __typename
                }
                __typename
            }
            education {
                id
                schoolName
                degree
                topic
                description
                startedIn
                graduatedIn
                __typename
            }
            __typename
        }
        """

    variables = {
        "email": email,
        "password": password,
        "signupToken": None
    }

    data = {
        "query": query,
        "variables": variables
    }

    response = requests.post('https://api.comet.co/api/graphql', json=data)

    status_code = response.status_code

    json_response = response.json()

    if status_code != 200 or 'errors' in json_response:
        error_message = json_response['errors'][0]['message']
        return {"error": error_message}

    user_data = json_response['data']['authenticate']
    return user_data


def map_freelancer(user, response):
    freelancer, created = Freelancer.objects.update_or_create(
        user=user,
        defaults={
            'email': response['email'],
            'first_name': response['firstName'],
            'last_name': response['lastName'],
            'full_name': response['fullName'],
            'job_title': response['jobTitle'],
            'phone_number': response['phoneNumber'],
            'picture': response['profilePictureUrl'],
            'slack_username': response['slackUsername'],
            'linkedin_url': response['freelance']['linkedInUrl'],
            'freelancer_id': response['freelance']['id'],
            'kaggle_url': response['freelance']['kaggleUrl'],
            'github_url': response['freelance']['gitHubUrl'],
            'iban': response['freelance']['iban'],
            'biography': response['freelance']['biography'],
            'experience_in_years': response['freelance']['experienceInYears'],
        }
    )

    if not created:
        freelancer.experiences.all().delete()

    for experience_data in response['freelance']['experiences']:
        experience = Experience.objects.create(
            experience_id=experience_data['id'],
            start_date=datetime.fromisoformat(
                experience_data['startDate'][:-1]),
            end_date=datetime.fromisoformat(
                experience_data['endDate'][:-1]) if experience_data['endDate'] else None,
            company_name=experience_data['companyName'],
            description=experience_data['description'],
            location=experience_data['location'],
            freelancer=freelancer,
        )

        for skill_data in experience_data['skills']:
            Skill.objects.create(
                skill_id=skill_data['id'],
                name=skill_data['name'],
                experience=experience,
            )
