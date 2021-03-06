from django.db import models
from django.utils.translation import gettext_lazy as _

from common.utils import generate_token_16
from naire import settings

from user.models import User


# For compatibility with old migrations
generate_invite_token = generate_token_16


class Org(models.Model):
    name = models.CharField(max_length=120)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Membership', related_name='members_of_org')
    root_folder = models.OneToOneField('form.Folder', on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
    invite_token = models.SlugField(max_length=32, unique=True, default=generate_token_16)

    def common_info(self):
        return {
            'id': self.id,
            'name': self.name,
            'member_count': self.members.count(),
        }

    def privileged_info(self):
        return {
            **self.common_info(),
            'invite_token': self.invite_token,
        }

    def basic_info(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Membership(models.Model):
    class Role(models.IntegerChoices):
        MEMBER = 0, _('member')
        ADMIN = 1, _('admin')
        OWNER = 2, _('owner')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
    role = models.IntegerField(
        choices=Role.choices,
        default=Role.MEMBER,
    )

    def org_info(self) -> dict[str]:
        return {
            **self.org.common_info(),
            'role': self.role,
            'can_leave': not (
                self.role >= Membership.Role.OWNER and
                self.org.membership_set.filter(role=Membership.Role.OWNER).count() <= 1
            ),
        }

    def member_info(self) -> dict[str]:
        res = self.user.info()
        res['role'] = self.role
        return res
