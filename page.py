page = 1

def get():
    return page

def set(value):
    global page
    page = value
    return page

