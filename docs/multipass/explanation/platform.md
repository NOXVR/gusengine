<!-- Source: https://documentation.ubuntu.com/multipass/stable/explanation/platform/ -->
# Platform

# Platform[¶](#platform)

See also: [How to install Multipass](../../how-to-guides/install-multipass/), [Host](../host/), [Driver](../driver/)

In Multipass, **platform** refers to the host computer’s operating system. This can be Windows, macOS, or Linux.

## Feature disparities[¶](#feature-disparities)

While we strive to offer a uniform interface across the board, not all features are available on all platforms and there are some behaviour differences:

Feature

Only supported on…

Notes

**Windows terminal integration**

- Windows

This affects the setting [`client.apps.windows-terminal.profiles`](../../reference/settings/client-apps-windows-terminal-profiles/)

**File and URL launches**

- Linux

This affects the [`launch`](../../reference/command-line-interface/launch/) command.

**Mounts**

- Linux
- macOS
- Windows *(disabled by default)*

On Windows, mounts can be enabled with the setting [`local.privileged-mounts`](../../reference/settings/local-privileged-mounts/). 
This affects the [`mount`](../../reference/command-line-interface/mount/), [`umount`](../../reference/command-line-interface/umount/), and [`launch`](../../reference/command-line-interface/launch/) commands.

**Extra networks (QEMU)**

- Linux
- macOS

When using the QEMU driver, extra networks are only supported on macOS. 
This affects the [`networks`](../../reference/command-line-interface/networks/) command, as well as `--network` and `--bridged` options in [`launch`](../../reference/command-line-interface/launch/).

**Global IPv6 (QEMU)**

- Linux
- macOS

When using the QEMU driver, global IPv6 addresses are only available on macOS.

**Drivers**

- Linux
- macOS
- Windows

Different drivers are available on different platforms. 
This affects the [`local.driver`](../../reference/settings/local-driver/) setting. 
See [Feature disparities](../driver/#driver-feature-disparities) for further behaviour differences depending on the selected driver.

**Bridging Wi-Fi networks**

- macOS

Wi-Fi networks are not shown in the output of the [`networks`](../../reference/command-line-interface/networks/) command on Linux and Windows.