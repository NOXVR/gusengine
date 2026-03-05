<!-- Source: https://documentation.ubuntu.com/multipass/stable/reference/command-line-interface/unalias/ -->
# unalias

# unalias[¶](#unalias)

See also: [`alias`](../alias/), [Alias](../../../explanation/alias/), [How to use command aliases](../../../how-to-guides/manage-instances/use-instance-command-aliases/)

The `multipass unalias` command removes a previously defined alias.

multipass unalias name

This will remove the given alias `name`, returning an error if the alias is not defined.

Note

If an instance is deleted and purged, it is not necessary to run `unalias` for the aliases defined on that instance, as they are automatically removed.

You can remove multiple aliases in a single command:

multipass unalias name1 name2 name3

Or, use the argument `--all` to remove all the defined aliases:

multipass unalias --all

The full `multipass help unalias` output explains the available options:

Usage: multipass unalias [options] <name> [<name> ...]
Remove aliases

Options:
  -h, --help     Displays help on commandline options
  -v, --verbose  Increase logging verbosity. Repeat the 'v' in the short option
                 for more detail. Maximum verbosity is obtained with 4 (or more)
                 v's, i.e. -vvvv.
  --all          Remove all aliases from current context

Arguments:
  name           Names of aliases to remove