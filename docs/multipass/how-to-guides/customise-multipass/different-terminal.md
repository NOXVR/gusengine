<!-- Source: https://documentation.ubuntu.com/multipass/stable/how-to-guides/customise-multipass/use-a-different-terminal-from-the-system-icon/ -->
# Use a different terminal from the system icon

# Use a different terminal from the system icon[¶](#use-a-different-terminal-from-the-system-icon)

See also: [How to install Multipass](../../install-multipass/), [`shell`](../../../reference/command-line-interface/shell/).

If you want, you can change the terminal application used by the Multipass system menu icon.

Note

Currently available only for macOS

To do so, you need to tell macOS which terminal to use for the `.command` file type. This document presents two ways of achieving this.

## Using `duti`[¶](#using-duti)

[`duti`](https://github.com/moretension/duti/) is a small helper application that can modify the default application preferences. It’s also [available from `brew`](https://formulae.brew.sh/formula/duti).

Find out your preferred terminal’s bundle identifier using `mdls`:

mdls /Applications/iTerm.app/ | grep BundleIdentifier
kMDItemCFBundleIdentifier              = "com.googlecode.iterm2"

And make it the default for script files using `duti`:

duti -s com.googlecode.iTerm2 com.apple.terminal.shell-script shell

## Using Finder[¶](#using-finder)

Create an empty file with a `.command` extension and find it in Finder. Select the file and press `⌘I`. You should be presented with an information pane like this:

Expand the “Open with:” section, select your preferred terminal application and click on “Change All…”.