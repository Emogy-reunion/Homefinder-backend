ALLOWED_EXTENSIONS = ['jpeg', 'jpg', 'png', 'webp', 'svg']

def allowed_file(filename):
    '''
    checks if the file extension is valid
    '''
    if '.' in filename:
        parts = filename.rsplit('.', 1)
        extension = parts[1].lower()
        if extension in ALLOWED_EXTENSIONS:
            return True
        else:
            return False
    else:
        return False
