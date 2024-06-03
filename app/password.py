from Comunication_LTD.settings import BASE_DIR
from django.core.mail import send_mail
import random
import json
import hashlib
import re

path = BASE_DIR/'static'/'config.txt'


#If Retrun None => it OK
def CheckPasswordIsOk(password):
    
    config_info ={}
    check = None
    
    with open(path, 'r+') as file:
        # Read the entire contents of the file
        config_text = file.read()
        print(config_text)
        config_info = json.loads(config_text)
        file.close()
        
    try:
        if( config_info['lenght_min'] >  len(password) or len(password) > config_info['lenght_max']):
            raise Exception("Password is not in the correct lenght")
        
        for x in config_info['contain']:
            pattern = '['+x+']'
            if(re.search(pattern, password) == None):
                raise Exception(f"Password is not contain the correct letters: {x}")
        
        if password in config_info['forbidden']:
            raise Exception("Password is weak")

    except Exception as error:
        check = error
    
    return check
        
        


def BuildPattern(template):
    
    pattern = '^'
    
    for x in template:
        pattern += "(?=.+["+x+"])"
    pattern +='$'
    return pattern


def sendEmailVerifiction(email):
    subject = 'Subject of the Email'
    message = 'This is the body of the email.'
    from_email = "Communication_LTD@domain.com"  # This can be omitted to use DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    code =  ''.join(random.choices('0123456789', k=6))
    
    # Convert the code to bytes (UTF-8 encoding)
    code_bytes = code.encode('utf-8')
    sha1_hash = hashlib.sha1()
    sha1_hash.update(code_bytes)
    code_with_SAH_1 = sha1_hash.hexdigest()
    
    message = f"Hi {from_email} ,\n\nthis is you code reset: {code_with_SAH_1}"
    
    try:
        print("sad assad ")
        send_mail(subject, message, from_email, recipient_list)
        return code_with_SAH_1
    except Exception as e:
        raise Exception(e)