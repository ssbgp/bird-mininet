# Run BIRD under Mininet

This simple tutorial shows how to run the [BIRD Internet Routing Daemon](http://bird.network.cz) under [Mininet](http://mininet.org). The tutorial focuses on a forked version of BIRD (available [here](https://github.com/ssbgp/bird)), which implements the SS-BGP routing protocol. It does not aim to be a complete guide on how to use BIRD or Mininet. The main goal is to have a step by step guide on how to have BIRD running under a virtual network (Mininet).

## Install Mininet

Mininet can be installed natively on a linux machine. However, this is not the recommended installation method. As described in Mininet's [official documentation](http://mininet.org/download), the easiest way to install Mininet is by downloading Mininet's VM image and run it under some virtualization system. We are going to follow this method here.

Follow these steps to install the VM:

1. Download the [Mininet VM image](https://github.com/mininet/mininet/wiki/Mininet-VM-Images).

1. Unzip the VM image. Make sure it created a directory called mininet-_version_ with two files with extensions `.ovf` and `.vdmk`.

1. Download [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and install it. Mininet's official documentation recommends [VirtualBox](https://www.virtualbox.org/wiki/Downloads) because it is free and works on most operating systems, including Linux, Windows, and MacOS. Still, you can use any virtualization system you want.

1. Create the VM from the image downloaded before.

  1. Open VirtualBox and go to **Machine -> New**.
  1. Give a name to the VM (any name you want).
  1. Set the **Type** to **Linux**.
  1. Set the **Version** to **Ubuntu (64-bit)**.
  1. Click **Next**.
  1. Click **Next** again (leave the memory size at the default value).
  1. Select option **Use an existing virtual hard disk file**.
  1. Click on the browse button on the right of the combo box. It will open up a choose dialog to choose the VM image.
  1. Go to the directory containing the VM image and select the file with extension `.vmdk`.
  1. Finally click **Create**. The VM is now created and should show up in VirtualBox's main window with the name you gave it.

1. Enable SSH access to the newly created VM
  1. Go to **Machine -> Settings**, while keeping the VM selected.
  1. Under Settings go to **Network**, click on the **Advanced** toggle, and click on **Port Forwarding**.
  1. Click on the add button to the right. It will create an entry on the forwarding table.
  1. Fill each column as follows:
    - **Name**: SSH
    - **Protocol**: TCP
    - **Host IP**: 0.0.0.0
    - **Host Port**: 5022
    - **Guest IP**: 0.0.0.0
    - **Guest Port**: 22
  1. Then click **OK**.

1. Start the VM.

At this point the VM should be booting. Once the VM has booted we can access to it using any SSH client. Use the following parameters to connect to the VM.

- **IP address**: localhost or 127.0.0.1
- **Port**: 5022
- **Username**: mininet
- **Password**: mininet

At this point you should have an SSH connection to the VM with mininet already pre-installed. Next step is to install BIRD.

## Install BIRD

Having an SSH connection to the Mininet's VM follow these steps to install BIRD with support for SS-BGP:

1. Clone the project.

        git clone https://github.com/ssbgp/bird.git

1. Move to project's directory.

        cd bird/

1. Install dependencies.

        sudo apt-get install bison m4 flex libncurses-dev libreadline6 libreadline6-dev

1. Compile and install BIRD.

        autoreconf
        ./configure
        make
        sudo make install

BIRD should now be installed. Enter this command to check: `bird --version`. It should show you a message like this "*BIRD version 1.6.3*" if BIRD was correctly installed.
