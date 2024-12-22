from AuthenticationApp.models import CustomUser
from ProfileApp.models import Profile

for user in CustomUser.objects.all():
    Profile.objects.get_or_create(user=user)

# if youre having error " user profile doesnt exist " try running this script
# python manage.py shell
# exec(open('create_profile.py').read())
