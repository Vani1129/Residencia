from django_otp.plugins.otp_static.models import StaticDevice
import random
def send_otp(user):
    # Generate an OTP
    device = StaticDevice.objects.get_or_create(user=user)[0]
    token = device.token_set.get()
    otp = token.token
    # Implement logic to send OTP via SMS or email to user
    return otp


def generate_otp(length=6):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])