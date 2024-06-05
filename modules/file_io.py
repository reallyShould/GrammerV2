from modules.emoj import *

def readFile(path):
    if path:
        try:
            file = open(path, "r", encoding="utf-8")
            text = file.read()
            file.close()
            return text
        except Exception as ex:
            if ex is FileExistsError:
                return ERROR_STR(f"File {path} is not exist!", "ERROR")
            else:
                print(ex)
                return ERROR_STR(f"Read {path} error!", "ERROR")
    else:
        return ERROR_STR(f"Variable path is empty", "ERROR")
