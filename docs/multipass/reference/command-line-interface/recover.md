<!-- Source: https://documentation.ubuntu.com/multipass/stable/reference/command-line-interface/recover/ -->
# recover

# recover[¶](#recover)

See also: [`delete`](../delete/), [`purge`](../purge/)

The `multipass recover` command will revive an instance that was previously removed with `multipass delete`. For this to be possible, the instance cannot have been purged with `multipass purge` nor with `multipass delete --purge`.

Use the `--all` option to recover all deleted instances at once:

multipass recover --all

The full `multipass help restart` output explains the available options:

Usage: multipass recover [options] <name> [<name> ...]
Recover deleted instances so they can be used again.

Options:
  -h, --help     Display this help on commandline options
  -v, --verbose  Increase logging verbosity. Repeat the 'v' in the short option
                 for more detail. Maximum verbosity is obtained with 4 (or more)
                 v's, i.e. -vvvv.
  --all          Recover all deleted instances

Arguments:
  name           Names of instances to recover