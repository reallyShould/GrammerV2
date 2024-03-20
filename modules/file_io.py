def readFile(path):
    if path:
        try:
            file = open(path, "r")
            text = file.read()
            file.close()
            return text
        except:
            return f"Read {path} error"
    else:
        return f"File {path} exist?"
