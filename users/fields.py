import string

from django import forms
from django.core.validators import validate_email
from django.forms.widgets import CheckboxInput
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from .conf import settings


class LengthValidator(object):
    code = 'length'

    def __init__(self, min_length=None, max_length=None):
        self.min_length = min_length or settings.USERS_PASSWORD_MIN_LENGTH
        self.max_length = max_length or settings.USERS_PASSWORD_MAX_LENGTH

    def __call__(self, value):
        if self.min_length and len(value) < self.min_length:
            raise forms.ValidationError(
                _('密码太短 (不能小于 %s 字符)') % self.min_length,
                code=self.code)
        elif self.max_length and len(value) > self.max_length:
            raise forms.ValidationError(
                _('密码太长(不能大于 %s 字符)') % self.max_length,
                code=self.code)

length_validator = LengthValidator()


class ComplexityValidator(object):
    code = 'complexity'
    message = _('密码太弱, %s')

    def __init__(self):
        self.password_policy = settings.USERS_PASSWORD_POLICY

    def __call__(self, value):
        if not settings.USERS_CHECK_PASSWORD_COMPLEXITY:  # pragma: no cover
            return

        uppercase, lowercase, digits, non_ascii, punctuation = set(), set(), set(), set(), set()

        for char in value:
            if char.isupper():
                uppercase.add(char)
            elif char.islower():
                lowercase.add(char)
            elif char.isdigit():
                digits.add(char)
            elif char in string.punctuation:
                punctuation.add(char)
            else:
                non_ascii.add(char)

        if len(uppercase) < self.password_policy.get('UPPER', 0):
            raise forms.ValidationError(
                self.message % _('必须包含 %(UPPER)s 或者 '
                                 '需要有 (A-Z)') % self.password_policy,
                code=self.code)
        elif len(lowercase) < self.password_policy.get('LOWER', 0):
            raise forms.ValidationError(
                self.message % _('必须包含 %(LOWER)s 或者 '
                                 '需要有 (a-z)') % self.password_policy,
                code=self.code)
        elif len(digits) < self.password_policy.get('DIGITS', 0):
            raise forms.ValidationError(
                self.message % _('必须包含%(DIGITS)s 或者 '
                                 '需要有小写字母(0-9)') % self.password_policy,
                code=self.code)
        elif len(punctuation) < self.password_policy.get('PUNCTUATION', 0):
            raise forms.ValidationError(
                self.message % _('必须包含 %(PUNCTUATION)s 或者 需要有 '
                                 'symbols') % self.password_policy,
                code=self.code)


complexity_validator = ComplexityValidator()


class PasswordField(forms.CharField):
    widget = forms.PasswordInput()
    default_validators = [length_validator, complexity_validator, ]


class HoneyPotField(forms.BooleanField):
    widget = CheckboxInput

    def __init__(self, *args, **kwargs):
        super(HoneyPotField, self).__init__(*args, **kwargs)
        self.required = False
        if not self.label:
            self.label = _('我们需要确保不是程序注册，敬请谅解')
        if not self.help_text:
            self.help_text = _('如果是本意注册，请不要选择。')

    def validate(self, value):
        if value:
            raise forms.ValidationError(_('Doh! You are a robot!'))


class EmailDomainValidator(object):
    message = _('抱歉, %s 该邮箱不能注册.请更换其他邮箱.')
    code = 'invalid'

    def __init__(self, ):
        self.domain_blacklist = settings.USERS_EMAIL_DOMAINS_BLACKLIST
        self.domain_whitelist = settings.USERS_EMAIL_DOMAINS_WHITELIST

    def __call__(self, value):
        if not settings.USERS_VALIDATE_EMAIL_DOMAIN:  # pragma: no cover
            return

        if not value or '@' not in value:
            raise forms.ValidationError(_('无效的邮箱.'), code=self.code)

        value = force_text(value)
        user_part, domain_part = value.rsplit('@', 1)

        if self.domain_blacklist and domain_part in self.domain_blacklist:
            raise forms.ValidationError(self.message % domain_part, code=self.code)

        if self.domain_whitelist and domain_part not in self.domain_whitelist:
            raise forms.ValidationError(self.message % domain_part, code=self.code)


validate_email_domain = EmailDomainValidator()


class UsersEmailField(forms.EmailField):
    default_validators = [validate_email, validate_email_domain]