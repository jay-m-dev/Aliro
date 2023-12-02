# Raspberry Pi OS Setup Instructions
## Required Tools
- A Raspberry Pi 4 (**Pi**)
- A PC where you can download and run the official Raspberry Pi Imager (**Imager**)
- A MicroSD Card with at least 16GB of space.
- An external USB Flash Drive with at least 4GB of space.
## On your local computer
1. Download the official **Imager** and use it to burn a copy of the Raspberry Pi OS Lite (64-bit) on your MicroSD Card.
- The **Imager** will let you configure these settings:
  - hostname: **aliroed**
  - username: **aliroed**
  - password: **aliroed**
  - Network settings: it is recommended to configure this temporarily, we'll remove this config at a later step.
  - Locale settings: Set a timezone and make sure the keyboard layout is set to **us**.
2. Download the **Aliro-*.zip file from the latest GitHub Release
3. Assuming your USB Flash Drive was mounted to **/mnt/usb**:
- `$ unzip Aliro-*.zip`
- `$ mkdir /mnt/usb/aliroed`
- `$ cp -r target/production/Aliro-*/* /mnt/usb/aliroed`
- `$ cp -r target/production/Aliro-*/.env /mnt/usb/aliroed` (hidden files need to be copied separately)
4. Copy the contents of this **raspberrypi** directory (the one that contains this Readme file) onto your USB Flash Drive:
- `$ mkdir /mnt/usb/config && cp raspberrypi/build_rpi/config/* /mnt/usb/config/`
- `$ mkdir /mnt/usb/scripts && cp raspberrypi/build_rpi/scripts/* /mnt/usb/scripts/`
- `$ mkdir /mnt/usb/services && cp raspberrypi/build_rpi/scripts/* /mnt/usb/services/`
- `$ mkdir /mnt/usb/data && cp raspberrypi/data/* /mnt/usb/aliroed/data/datasets/user/`
- `$ mkdir /mnt/usb/intropage && cp -r raspberrypi/intropage /mnt/usb/intropage`
5. Unmount the USB Flash Drive and have it ready to plug in to the **Pi**

## On the Raspberry Pi.
1. Insert the MicroSD Card in the **Pi** and boot it up.
2. Login to the **Pi** as user **aliroed** 
3. Insert the USB Flash Drive on an available USB Port. Mount it manually on `/mnt/usb/`, if it's not automounted
4. Ensure the Pi is connected to the internet (run `$ sudo raspi-config` to configure if necessary)
5. Run these commands:
- `$ cp /mnt/usb/scripts/*.sh /home/aliroed/`
- `$ ./setup_dirs.sh`
- `$ cp -r /mnt/usb/aliroed/* /aliroed/`
- `$ cp /mnt/usb/aliroed/.env /aliroed` (hidden files need to be copied separately)
- `$ ./install.sh`
6. Check that docker was installed: `$ docker --version`
7. Configure the docker images
- `$ docker compose -f /aliroed/docker-compose.yml pulludos
- `$ ./docker_compress.sh` (This step will take a few minutes)
- `$ sudo cp /mnt/usb/services/* /etc/systemd/system/`
8. Enable services.**Note:** Do **not** enable the `aliroed-load.service` yet.
- `$ sudo systemctl enable aliroed-load-test.service`
- `$ sudo systemctl enable aliroed-compose.service`
- `$ sudo cp /mnt/usb/config/autostart /etc/xdg/openbox/`
- `$ ./docker_prune.sh`
- `$ ./cleanup.sh`
9. run `sudo raspi-config` and enable **System Options > Desktop Autologin**
10. Reboot the **Pi** and test that everything works as expected
11. Configure the Chromium Web browser by setting the `/intropage/index.html` as the **homepage**, add a **bookmark**
to this page and show the Bookmarks Bar, and in Settings, configure this page to be launched **On Startup**.
12. After testing that everything works, run:
- `$ sudo systemctl disable aliroed-load-test.service`
- `$ sudo rm /etc/systemd/system/alrioed-load-test.service`
- `$ sudo systemctl enable aliroed-load.service`
13. Clean up again:
- `$ ./docker_prune.sh`
- `$ ./cleanup.sh`

## Extract, Shrink and Compress the MicroSD Card image
1. Extract the image into a **.img** file with a tool like **dd**: `sudo dd if=/dev/sdX of=aliroed.img bs=4M`
2. Use PiShrink to shrink the image. The image should also be compressed with **xz**. There are 2 options for this: `sudo ./pishrink.sh aliroed.img`
   a. use PiShrink with the -Z option, or
   b. use the `xz` utility independently: `xz -9 aliroed.img` (**Note: This option has worked best so far**)
# Building the aliro-image executable
## Windows
Perform these steps after performing the steps in Linux to extract the .img file, shrinking with PiShrink and compressing with xz.
These steps work on a Windows 11 machine:
1. Ensure you have a Code Signing Certificate installed.
2. Embed the aliro.img.xz file in the same level as the **src** directory. 
3. Open the Epistasis/aliro-imager project in Qt Creator (follow the instructions on the aliro-imager repository)
4. Configure the version number as needed. The current scheme is to use the version of the latest Aliro Release (e.g. 0.21)
5. Proceed to `Build All Projects` in Qt Creator
6. Use `nsis-binary-7336-1` to build the installer, using the **aliro-imager.nsi** script output by the Qt Creator build.
