import os
import time
import json
import colorama
import requests
import git
import shutil
import errno
import subprocess
from typing import Optional

def handle_remove_readonly(func, path, exc):
    if exc[1].errno == errno.EACCES:
        os.chmod(path, 0o666)
        func(path)
    else:
        raise

class Installer:
    
    def __init__(self):
        colorama.init()
        self.username = os.getlogin()
        self.default_path = f"C:\\Users\\{self.username}\\AppData\\Roaming\\Grammer"
        self.config_file = "installer_config.json"
        self.errors = 0
        self.config = self._load_config()
        self.repos = "https://github.com/reallyShould/GrammerV2.git"

    def _load_config(self) -> dict:
        default_config = {
            "path": self.default_path,
            "telegram_id": None,
            "token": None
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            return default_config
        except Exception as e:
            print(f"{colorama.Fore.RED}Error loading config: {str(e)}{colorama.Style.RESET_ALL}")
            return default_config

    def _save_config(self) -> None:
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"{colorama.Fore.RED}Error saving config: {str(e)}{colorama.Style.RESET_ALL}")

    def _reset_config(self) -> None:
        try:
            os.remove(self.config_file)
        except Exception as e:
            print(f"{colorama.Fore.RED}Error resetting config: {str(e)}{colorama.Style.RESET_ALL}")

    def _display_logo(self) -> None:
        print(f"""{colorama.Fore.CYAN}
░██████╗░██████╗░░█████╗░███╗░░░███╗███╗░░░███╗███████╗██████╗░
██╔════╝░██╔══██╗██╔══██╗████╗░████║████╗░████║██╔════╝██╔══██╗
██║░░██╗░██████╔╝███████║██╔████╔██║██╔████╔██║█████╗░░██████╔╝
██║░░╚██╗██╔══██╗██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝░░██╔══██╗
╚██████╔╝██║░░██║██║░░██║██║░╚═╝░██║██║░╚═╝░██║███████╗██║░░██║
░╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝
{colorama.Style.RESET_ALL}""")
        print("""█ █▄░█ █▀ ▀█▀ ▄▀█ █░░ █░░ █▀▀ █▀█
█ █░▀█ ▄█ ░█░ █▀█ █▄▄ █▄▄ ██▄ █▀▄
=================================""")
        
    def _check_internet(self, url: str, box: bool = False) -> Optional[str]:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return f"{colorama.Fore.GREEN}[✓]" if box else True
            self.errors += 1
            return f"{colorama.Fore.RED}[✗]" if box else False
        except requests.RequestException:
            self.errors += 1
            return f"{colorama.Fore.RED}[✗]" if box else False

    def _check_admin(self) -> str:
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            return f"{colorama.Fore.GREEN}[✓]" if is_admin else f"{colorama.Fore.RED}[✗]"
        except Exception:
            self.errors += 1
            return f"{colorama.Fore.RED}[✗]"

    def _add_to_startup(self, script_path: str, task_name: str = "GrammerScript") -> bool:
        try:
            if not os.path.exists(script_path):
                print(f"{colorama.Fore.RED}Error: Script {script_path} does not exist{colorama.Style.RESET_ALL}")
                return False

            python_path = os.path.join(self.config['path'], "python", "Scripts", "pythonw.exe")
            if not os.path.exists(python_path):
                print(f"{colorama.Fore.RED}Error: Python interpreter {python_path} not found{colorama.Style.RESET_ALL}")
                return False

            command = (
                f'schtasks /Create /SC ONLOGON /TN "{task_name}" '
                f'/TR "\'{python_path}\' \'{script_path}\'" /RL HIGHEST /F'
            )
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"{colorama.Fore.GREEN}Task {task_name} successfully added to startup with admin privileges{colorama.Style.RESET_ALL}")
                return True
            else:
                print(f"{colorama.Fore.RED}Error creating task: {result.stderr}{colorama.Style.RESET_ALL}")
                return False
        except Exception as e:
            print(f"{colorama.Fore.RED}Error adding to startup: {str(e)}{colorama.Style.RESET_ALL}")
            return False

    def _initial_check(self) -> bool:
        self._display_logo()
        print(f"{self._check_admin()} Admin rights{colorama.Style.RESET_ALL}")
        print(f"{self._check_internet('https://github.com', True)} Connection with https://github.com{colorama.Style.RESET_ALL}")
        print(f"{self._check_internet('https://t.me', True)} Connection with https://t.me{colorama.Style.RESET_ALL}")
        
        if self.errors > 0:
            print(f"{colorama.Fore.RED}Errors detected! Aborting...{colorama.Style.RESET_ALL}")
            time.sleep(3)
            return False
        return True

    def _install(self) -> None:
        try:
            try:
                shutil.rmtree(self.config['path'], onerror=handle_remove_readonly)
            except:
                pass
            os.makedirs(self.config['path'], exist_ok=True)
            
            git.Repo.clone_from(self.repos, self.config['path'])
            
            config_path = os.path.join(self.config['path'], "config.py")
            with open(config_path, "r") as f:
                config_content = f.read()
            config_content = config_content.replace("<PATH>", self.config["path"]).replace("\\", "\\\\")
            config_content = config_content.replace("<TOKEN>", self.config["token"])
            config_content = config_content.replace("\"<ID>\"", self.config["telegram_id"])
            config_content = config_content.replace("<PYTHON>", f'{self.config["path"]}\\python\\Scripts\\pythonw.exe'.replace("\\", "\\\\"))
            with open(config_path, "w+") as f:
                f.write(config_content)

            script_path = os.path.join(self.config['path'], "grammer.py")
            if os.path.exists(script_path):
                if self._add_to_startup(script_path, "GrammerScript"):
                    print(f"{colorama.Fore.GREEN}Script {script_path} added to startup{colorama.Style.RESET_ALL}")
                else:
                    print(f"{colorama.Fore.RED}Failed to add script to startup{colorama.Style.RESET_ALL}")
            else:
                print(f"{colorama.Fore.RED}Script {script_path} not found, startup not configured{colorama.Style.RESET_ALL}")

            print(f"{colorama.Fore.GREEN}Installation completed successfully!{colorama.Style.RESET_ALL}")
            time.sleep(2)
        except Exception as e:
            print(f"{colorama.Fore.RED}Installation failed: {str(e)}{colorama.Style.RESET_ALL}")
            time.sleep(2)

    def _display_menu(self) -> None:
        os.system("cls")
        self._display_logo()
        
        print(f"""User: {self.username}
Install path: {self.config['path']}
Telegram ID: {self.config['telegram_id'] or 'Not set'}
Token: {'*' * 8 if self.config['token'] else 'Not set'}""")
        
        print(f"""{colorama.Fore.GREEN}
[1] Clean and install
[2] Change path
[3] Change Telegram ID
[4] Change token
[5] Reset installer
{colorama.Fore.RED}
[6-9] Exit{colorama.Style.RESET_ALL}""")
        
        try:
            choice = int(input(">>> "))
            if choice == 1:
                self._install()
            elif choice == 2:
                self.config['path'] = input("Enter new path >>> ")
                self._save_config()
            elif choice == 3:
                self.config['telegram_id'] = input("Enter new Telegram ID >>> ")
                self._save_config()
            elif choice == 4:
                self.config['token'] = input("Enter new token >>> ")
                self._save_config()
            elif choice == 5:
                self._reset_config()
            else:
                exit()
        except ValueError:
            print(f"{colorama.Fore.RED}Invalid input! Please enter a number.{colorama.Style.RESET_ALL}")
            time.sleep(2)
        
        self._display_menu()

    def run(self) -> None:
        os.system("cls")
        self._display_logo()
        if not self.config['token']:
            self.config['token'] = input("Enter your token >>> ")
            self._save_config()
        if not self.config['telegram_id']:
            self.config['telegram_id'] = input("Enter your Telegram ID >>> ")
            self._save_config()
        os.system("cls")
        if self._initial_check():
            time.sleep(2)
            self._display_menu()

if __name__ == "__main__":
    installer = Installer()
    installer.run()