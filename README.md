# collect-wx-emoticon

A tool to collect and archive WeChat emoticons.

## Collect Emoticons

The tool provides a TamperMonkey extension for Web WeChat, monitoring incoming emoticons and saving them to the disk.

 1. Install TamperMonkey extension in `extension/CollectWXEmoticon.js`.
 2. Select "Downloads BETA > Download Mode > Broswer API" in TamperMonkey Settings page.
 2. Log onto Web WeChat, and click the "Start Auto-saving Emotions" button in the top-right corner.
 3. Open your "File Transfer" (文件传输助手) on your phone / PC WeChat, and send the emoticons you want to collect. The extension automatically dumps them to the disk.

Default storage path is `${DOWNLOADS}/wx_emoticons/`, where `${DOWNLOADS}` is the Downloads folder of your browser (e.g. `~/Downloads` in Ubuntu).

## Archive Emoticons

The tool provides a Python script `scripts/archive.py` to rename, copy and delete duplicated emoticons. Usage:

```
usage: archive.py [-h] [-s SOURCE] [-d DEST]

Archive saved Wechat emoticons from Downloads folder

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        path to the Downloads folder of this computer
                        default: /path/to/Downloads
  -d DEST, --dest DEST  path to the folder that stores archived emoticons
                        default: /path/to/this/repository/archived_emoticons
```