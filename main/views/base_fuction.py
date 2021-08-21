import re, random, string, kavenegar
from datetime import datetime

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def check_str_length(value, permitted_length):
    value_length = len(value)
    if value_length > 0 and value_length <= permitted_length:
        return True
    else:
        return False
        

def is_valid_mobile_number(input):
    if not re.search(r'^09\d{9}$', input):
        return False
    return True


def is_valid_date(input):
    if not re.search(r'^\d{4}-\d{2}-\d{2}$', input):
        return False
    return True


def is_valid_email(input):
    if not re.search(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', input):
        return False
    return True


# check password (password must be at least 8 characters - including lowercase letters and numbers)
def check_password(password, repeat_password):
    password_pattern = r'^[A-Za-z0-9@#$%^&+=!()\-\_\.\*\\\/\[\]\{\}?,~`]{8,}$'
    if password == repeat_password:
        if (re.search(password_pattern, password)) and (re.search(password_pattern, repeat_password)):
            return True, None
        else:
            return False, 'رمز عبور و تکرار آن مطابق الگو نمی باشند.'
    else:
        return False, 'رمز عبور و تکرار آن یکسان نمی باشند.'


def send_sms(to_number, verify_code):
    try:
        api = kavenegar.KavenegarAPI(
            '2B485230622F74625978584E343167657576785041736B4A586D6E524C4661577A56566B44366D674C75413D')
        params = {
            'receptor': to_number,
            # sogoli-verify-code
            'template': 'verify-code',
            'token': verify_code,
            'type': 'sms',
        }
        api.verify_lookup(params)
        return True, None
    except Exception as e:
        return False, str(e)


def convert_to_regex(this_text):
    # set regex
    text = this_text.split(' ')
    text = list(filter(lambda i: i != '', text))
    word_list = []
    for word in text:
        result_word = list(map(lambda x: x + '\s*', word.replace(' ', '')[:-1]))
        result_word = ''.join(result_word) + word[-1]
        word_list.append(result_word)
    result_word = r'.*'.join(word_list)
    return result_word


def generate_random_code(length):
    code = ''.join(random.choice(string.digits) for i in range(length))
    return code