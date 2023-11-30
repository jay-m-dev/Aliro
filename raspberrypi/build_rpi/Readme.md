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
2. Download the **Aliro-*.zip file from the latest GitHub Release.
3. Copy the **raspberrypi** directory (the one that contains this Readme file) onto your USB Flash Drive.
4. Copy the downloaded **Aliro-*.zip** file onto your USB Flash Drive.

## On the Raspberry Pi.
1. Insert the MicroSD Card in the **Pi** and boot it up.
2. Login to the **Pi** as user **aliroed**.
3. Insert the USB Flash Drive on an available USB Port. Mount it manually on `/mnt/usb/`, if it's not automounted
4. Ensure the Pi is connected to the internet (run `$ sudo raspi-config` to configure if necessary)
5. Copy the scripts into the **home** directory: `$ cp /mnt/usb/raspberrypi/build_rpi/scripts/*.sh ~`
** Run the following commands from the **home** directory (`$ cd ~`)
6. Run `$ ./setup_dirs.sh`
7. Unzip the **Aliro-*.zip**
8. Copy the main contents of Aliro into **/aliroed** with `$ cp -r target/production/Aliro-x.yy/* /aliroed/` (replace x.yy with the actual Aliro version)
9. Copy the files in the **data** directory: `$ cp /mnt/usb/raspberrypi/build_rpi/data/* /aliroed/data/datasets/user`
10. Run `$ ./install.sh`
11. Check that docker was installed: `$ docker --version`
12. Run `$ docker compose -f /aliroed/docker-compose.yml pull`
13. Run `$ ./docker_compress.sh`
14. Copy the services: `$ sudo cp /mnt/usb/raspberrypi/build_rpi/services/* /etc/systemd/system`
15. Enable each service:
- `$ sudo systemctl enable aliroed-load.service`
- `$ sudo systemctl enable aliroed-compose.service`
16. Run `$ ./browser_setup.sh`
17. Run `$ ./docker_prune.sh`
18. Run `$ ./cleanup.sh`

If Everything went well, the custom OS should be ready, at this point you could proceed with the steps to build the aliro-imager.exe
But it's a good idea to test that this process worked by launching Booting up the OS.  
**Note:** After

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
## Linux
1. Extract the image into a **.img** file with a tool like **dd**: `sudo dd if=/dev/sdX of=aliroed.img bs=4M`
2. Use PiShrink to shrink the image. The image should also be compressed with **xz**. There are 2 options for this: `sudo ./pishrink.sh aliroed.img`
    a. use PiShrink with the -Z option, or 
    b. use the `xz` utility independently: `xz -9 aliroed.img` (**Note: This option has worked best so far**)
