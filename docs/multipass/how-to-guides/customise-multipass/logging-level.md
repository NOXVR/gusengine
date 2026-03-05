<!-- Source: https://documentation.ubuntu.com/multipass/stable/how-to-guides/customise-multipass/configure-multipass-default-logging-level/ -->
# Configure Multipass’s default logging level

# Configure Multipass’s default logging level[¶](#configure-multipasss-default-logging-level)

See also: [Logging levels](../../../reference/logging-levels/)

This document demonstrates how to configure the default logging level of the Multipass service. Changing the logging level can be useful, for example, if you want to decrease the size of logging files or get more detailed information about what the daemon is doing. Logging levels can be set to one of the following: `error`, `warning`, `info`, `debug`, or `trace`, with case sensitivity.

## Changing the default logging level[¶](#changing-the-default-logging-level)

LinuxmacOSWindows
First, stop the Multipass daemon:

sudo snap stop multipass

After that, create the override config file, replacing `<level>` with your desired logging level:

sudo mkdir /etc/systemd/system/snap.multipass.multipassd.service.d/
sudo tee /etc/systemd/system/snap.multipass.multipassd.service.d/override.conf <<EOF
[Service]
ExecStart=
ExecStart=/usr/bin/snap run multipass.multipassd --verbosity <level>
EOF
sudo systemctl daemon-reload

Finally, start the Multipass daemon:

sudo snap start multipass

First, become `root`:

sudo su

Stop the Multipass daemon:

launchctl unload /Library/LaunchDaemons/com.canonical.multipassd.plist

Then, open `/Library/LaunchDaemons/com.canonical.multipassd.plist` in your favourite [text editor](https://www.google.com/search?q=vi) and edit the path `/dict/array/string[2]` from `debug` to the logging level of your choice.

Finally, start the Multipass daemon:

launchctl load /Library/LaunchDaemons/com.canonical.multipassd.plist

First, open an administrator privileged PowerShell prompt.

Stop the Multipass service:

Stop-Service Multipass

Then, edit the Multipass service registry key with the following command:

Set-ItemProperty -path HKLM:\System\CurrentControlSet\Services\Multipass -Name ImagePath -Value "'C:\Program Files\Multipass\bin\multipassd.exe' /svc --verbosity <level>"

Replacing `<level>` with your desired logging level.

Finally, start the Multipass service:

Start-Service Multipass