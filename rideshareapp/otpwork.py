import random


def otpgen():
    otp = int(''.join(str(random.randint(1, 9)) for i in range(4)))
    return otp
