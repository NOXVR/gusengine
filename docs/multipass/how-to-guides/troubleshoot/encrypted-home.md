<!-- Source: https://documentation.ubuntu.com/multipass/stable/how-to-guides/troubleshoot/mount-an-encrypted-home-folder/ -->
# Mount an encrypted home folder

# Mount an encrypted home folder[¶](#mount-an-encrypted-home-folder)

See also: [`mount`](../../../reference/command-line-interface/mount/), [Instance](../../../explanation/instance/)

When you create the [Primary instance](../../../explanation/instance/#primary-instance)  using `multipass start` or `multipass shell` without additional arguments, Multipass automatically mounts your home directory into it.

On Linux, if your local home folder is encrypted using ` fscrypt`, [snap confinement](https://snapcraft.io/docs/snap-confinement) prevents you from accessing its contents from a Multipass mount due the peculiar directory structure (`/home/.ecryptfs/<user>/.Private/`). This also applies to the primary instance, where the home folder is mounted automatically.

A workaround is mounting the entire `/home` folder into the instance, using the command:

multipass mount /home primary

By doing so, the home folder’s contents will be mounted correctly.

**Contributors:** @ricab, @gzanchi 
-->