def readFile(path):
    if path:
        try:
            file = open(path, "r")
            text = file.read()
            file.close()
            return text
        except:
            return -1
    else:
        return -1
