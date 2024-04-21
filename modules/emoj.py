FOLDER = "📁"
FILE = "📄"
USER = "👤"
PREF = "🛠"
QUESTION = "❓"
PC = "🖥"
LOCK = "🔒"
DONE = "✅"

errors = {
    "ERROR": "⛔️",
    "WARNING": "⚠️"
}

def ERROR_STR(text:str, status:str):
    try:
        return f"{errors[status]}{text}"
    except:
        return text