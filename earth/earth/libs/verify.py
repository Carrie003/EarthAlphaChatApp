import re,hashlib

email = re.compile("^[a-zA-Z0-9_\-.]*@[a-zA-Z0-9_\-.]*$")
phone = re.compile("^[0-9]{11}$")
key = re.compile("^[0-9]{6}$")
password = re.compile("^[0-9a-zA-Z!\-.?]*$")
uid = re.compile("^[0-9a-zA-Z]{8}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{12}$")
picture = re.compile("")
#address filter
pureword = re.compile("^\w*$") #none symbol content
general = re.compile("^[\w,!.? #]*$") # normal text
zipcode = re.compile("^[0-9]{5}$")
picture = re.compile("^[0-9a-zA-Z#&=/]*$")

def md5(content):
    m5 = hashlib.md5()
    m5.update(content.encode("utf-8"))
    hashed = m5.hexdigest()
    return hashed

def secure(content):
    content = content.replace("\"","").replace("<","")
    content = content.replace(">","").replace("\'","")
    return content

def verPhone(content):
    if phone.match(content):
        return True
    return False

def verEmail(content):
    if (email.match(content)&len(content)<=50):
        return True
    return False

def verKey(content):
    if key.match(content):
        return True
    return False

def verPassword(content):
    if password.match(content):
        if len(content)<=30:
            return True
    return False


def verUrl(content):
    #TODO: filter
    return True

def verID(content):
    if uid.match(content):
        return True
    return False

def verContent(style,content):
    if style == 2:
        if len(content) <= 2000 <= 50000:
            return True
        else:
            return False
    return True

def verTags(content):
    return True
