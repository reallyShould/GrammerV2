# GrammerV2
The program allows you to control your computer using only Telegram.

## Install
To install, you will need an [API](https://t.me/BotFather) key and your [Telegram ID](https://t.me/my_id_bot)
- Input your ID and API
- Click Install

## Usage
Write `/start` and the bot will write you the available commands.
### Basic Commands:

- `SHUTDOWN`: Shut down the computer.
- `REBOOT`: Reboot the computer.
- `SLEEP`: Put the computer to sleep.
- `LOCK`: Lock the computer.
- `LOGOUT`: Log out of the system.
- `screen`: Take a screenshot of the screen.

### Other Commands:

- `ls`: List files in the specified directory.
- `mkdir`: Create a new directory.
- `cd <path>`: Change the current directory.
- `cp <from> <to>`: Copy a file.
- `mv <from> <to>`: Move a file.
- `rm <path>`: Delete a file or directory.
- `start`: Open a file.
- `getfile <from>`: Get a file from the computer (limited).
- `cmd <command>`: Execute a command in the Windows command prompt (limited).
- `cmd2`: Execute a command in the command prompt with output (testing).
- `drop`: Upload a file to the computer (unstable).
- `cat <path>`: Read a text file.
- `touch <path>`: Create a file.

### Voice Commands:

- `voice`: Start voice recording.
- `voice setseconds <int>`: Set the recording duration in seconds.
- `voice setchunk <int>`: Set the recording block size.
- `voice setrate <int>`: Set the sampling rate (48000, 44100).
- `voice setchannels <int>`: Set the number of recording channels.
- `voice setdevice <int>`: Set the recording device.
- `voice settings`: Show current voice recording settings.
- `voice list`: Show a list of available recording devices.