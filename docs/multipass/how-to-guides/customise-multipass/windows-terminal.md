<!-- Source: https://documentation.ubuntu.com/multipass/stable/how-to-guides/customise-multipass/integrate-with-windows-terminal/ -->
# How to integrate with Windows Terminal

# How to integrate with Windows Terminal[¶](#how-to-integrate-with-windows-terminal)

If you are on Windows and you want to use [Windows Terminal](https://aka.ms/terminal), Multipass can integrate with it to offer you an automatic `primary` profile.

## Multipass profile[¶](#multipass-profile)

Currently, Multipass can add a profile to Windows Terminal for the [Primary instance](../../../explanation/instance/#primary-instance). When you open a Windows Terminal tab with this profile, you’ll automatically find yourself in a primary instance shell. Multipass automatically starts or launches the primary instance if needed.

## Install Windows Terminal[¶](#install-windows-terminal)

The first step is to [install Windows Terminal](https://github.com/microsoft/terminal#installing-and-running-windows-terminal). Once you have it along Multipass, you can enable the integration.

## Enable integration[¶](#enable-integration)

Open a terminal (Windows Terminal or any other) and enable the integration with the following command:

multipass set client.apps.windows-terminal.profiles=primary

For more information on this setting, see [`client.apps.windows-terminal.profiles`](../../../reference/settings/client-apps-windows-terminal-profiles/). Until you modify it, Multipass will try to add the profile if it finds it missing. To remove the profile see [Revert](#integrate-with-windows-terminal-revert) below.

## Open a Multipass tab[¶](#open-a-multipass-tab)

You can now open a “Multipass” tab to get a shell in the primary instance. That can be achieved by clicking the new-tab drop-down and selecting the Multipass profile:

That’s it!

## Revert[¶](#revert)

If you want to disable the profile again, you can do so with:

multipass set client.apps.windows-terminal.profiles=none

Multipass will then remove the profile if it exists.