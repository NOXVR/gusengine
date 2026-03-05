<!-- Source: https://documentation.ubuntu.com/multipass/stable/how-to-guides/customise-multipass/configure-where-multipass-stores-external-data/ -->
# Configure where Multipass stores external data

# Configure where Multipass stores external data[¶](#configure-where-multipass-stores-external-data)

This document demonstrates how to configure the location where Multipass stores instances, caches images, and other data. Configuring a new storage location can be useful, for example, if you need to free up storage space on your boot partition.

## Configuring a new storage location[¶](#configuring-a-new-storage-location)

Caution

**Caveats:**

- 
Multipass will not migrate your existing data; this article explains how to do it manually. If you do not transfer the data, you will have to re-download any Ubuntu images and reinitialise any instances that you need.

- 
When uninstalling Multipass, the uninstaller will not remove data stored in custom locations, so you’ll have to delete it manually.

LinuxmacOSWindows
First, stop the Multipass daemon:

sudo snap stop multipass

Since Multipass is installed using a strictly confined snap, it is limited on what it can do or access on your host. Depending on where the new storage directory is located, you will need to connect the respective interface to the Multipass snap. Because of [snap confinement](https://snapcraft.io/docs/snap-confinement), this directory needs to be located in either `/home` (connected by default) or one of the removable mounts points (`/mnt` or `/media`). To connect the removable mount points, use the command:

sudo snap connect multipass:removable-media

Create the new directory in which Multipass will store its data:

mkdir -p <path>
sudo chown root <path>

After that, create the override config file, replacing `<path>` with the absolute path of the directory created above.

sudo mkdir /etc/systemd/system/snap.multipass.multipassd.service.d/
sudo tee /etc/systemd/system/snap.multipass.multipassd.service.d/override.conf <<EOF
[Service]
Environment=MULTIPASS_STORAGE=<path>
EOF

The output at this point will be:

[Service]
Environment=MULTIPASS_STORAGE=<path>

Then, instruct `systemd` to reload the daemon configuration files:

sudo systemctl daemon-reload

Now you can transfer the data from its original location to the new location:

sudo cp -r /var/snap/multipass/common/data/multipassd <path>/data
sudo cp -r /var/snap/multipass/common/cache/multipassd <path>/cache

You also need to edit the following configuration files so that the specified paths point to the new Multipass storage directory, otherwise your instances will fail to start:

- 
`multipass-vm-instances.json`: Update the absolute path of the instance images in the “arguments” key for each instance.

- 
`vault/multipassd-instance-image-records.json`: Update the “path” key for each instance.

Finally, start the Multipass daemon:

sudo snap start multipass

You can delete the original data at your discretion, to free up space:

sudo rm -rf /var/snap/multipass/common/data/multipassd/vault
sudo rm -rf /var/snap/multipass/common/cache/multipassd

First, become `root`:

sudo su

Stop the Multipass daemon:

launchctl unload /Library/LaunchDaemons/com.canonical.multipassd.plist

Move your current data from its original location to `<path>`, replacing `<path>` with your custom location of choice:

mv /var/root/Library/Application\ Support/multipassd <path>

Caution

Make sure the `multipassd` directory is moved to `<path>`, and not inside the  `<path>` folder.

Define a symbolic link from the original location to the absolute path of new location:

ln -s <path> /var/root/Library/Application\ Support/multipassd

Finally, start the Multipass daemon:

launchctl load /Library/LaunchDaemons/com.canonical.multipassd.plist

First, open a PowerShell prompt with administration privileges.

Stop Multipass instances:

multipass stop --all

Stop the Multipass daemon:

Stop-Service Multipass

Create and set the new storage location, replacing `<path>` with the absolute path of your choice:

New-Item -ItemType Directory -Path "<path>"
Set-ItemProperty -Path "HKLM:System\CurrentControlSet\Control\Session Manager\Environment" -Name MULTIPASS_STORAGE -Value "<path>"

Now you can transfer the data from its original location to the new location:

Copy-Item -Path "C:\ProgramData\Multipass\*" -Recurse -Force -Destination "<path>"

Caution

It is important to copy any existing data to the new location. This avoids unauthenticated client issues, permission issues, and in general, to have any previously created instances available.

You also need to edit several settings so that the specified paths point to the new Multipass storage directory, otherwise your instances will fail to start:

- 
`<path>/data/vault/multipassd-instance-image-records.json`: Update the “path” key for each instance.

- 
Open Hyper-V Manager > For each instance right-click the instance and open the settings. Navigate to SCSI Controller > Hard Drive and update the Media path. Do the same for SCSI Controller > DVD Drive > Media Image file.

Finally, start the Multipass daemon:

Start-Service Multipass

You can delete the original data at your discretion, to free up space:

Remove-Item -Path "C:\ProgramData\Multipass\cache\*" -Recurse
Remove-Item -Path "C:\ProgramData\Multipass\data\vault\*" -Recurse

## Reverting back to the default location[¶](#reverting-back-to-the-default-location)

LinuxmacOSWindows
Stop the Multipass daemon:

sudo snap stop multipass

Although not required, to make sure that Multipass does not have access to directories that it shouldn’t, you can disconnect the respective interface depending on where the custom storage location was set (see [Configuring a new storage location](#configuring-a-new-storage-location) above).
For example, to disconnect the removable mounts points (`/mnt` or `/media`), run:

sudo snap disconnect multipass:removable-media

Then, remove the override config file:

sudo rm /etc/systemd/system/snap.multipass.multipassd.service.d/override.conf
sudo systemctl daemon-reload

Now you can transfer your data from the custom location back to its original location:

sudo cp -r <path>/data /var/snap/multipass/common/data/multipassd
sudo cp -r <path>/cache /var/snap/multipass/common/cache/multipassd

You also need to edit the following configuration files so that the specified paths point to the original Multipass storage directory, otherwise your instances will fail to start:

- 
`multipass-vm-instances.json`: Update the absolute path of the instance images in the “arguments” key for each instance.

- 
`vault/multipassd-instance-image-records.json`: Update the “path” key for each instance.

Finally, start the Multipass daemon:

sudo snap start multipass

You can delete the data from the custom location at your discretion, to free up space:

sudo rm -rf <path>

First, become `root`:

sudo su

Stop the Multipass daemon:

launchctl unload /Library/LaunchDaemons/com.canonical.multipassd.plist

Remove the link pointing to your custom location:

unlink /var/root/Library/Application\ Support/multipassd

Move the data from your custom location back to its original location:

mv <path> /var/root/Library/Application\ Support/multipassd

Finally, start the Multipass daemon:

launchctl load /Library/LaunchDaemons/com.canonical.multipassd.plist

First, open a PowerShell prompt with administrator privileges.

Stop Multipass instances:

multipass stop --all

Stop the Multipass daemon:

Stop-Service Multipass

Remove the setting for the custom storage location:

Remove-ItemProperty -Path "HKLM:System\CurrentControlSet\Control\Session Manager\Environment" -Name MULTIPASS_STORAGE

Now you can transfer the data back to its original location:

Copy-Item -Path "<path>\*" -Destination "C:\ProgramData\Multipass" -Recurse -Force

Follow the same instructions from setting up the custom image location to update the paths to their original location.

Finally, start the Multipass daemon:

Start-Service Multipass

You can delete the data from the custom location at your discretion, to free up space:

Remove-Item -Path "<path>" -Recurse -Force