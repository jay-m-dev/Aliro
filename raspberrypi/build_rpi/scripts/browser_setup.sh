#/bin/bash
# setup the browsers home page
mkdir p ~/.config/chromium/Default

sed -i 's/"homepage" : "about:blank"/"homepage" : "file///aliroed/intropage/index.html"/' ~/.config/chromium/Default/Preferences
