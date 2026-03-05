# Source: https://man7.org/linux/man-pages/man1/crontab.1.html
# Downloaded: 2026-02-16

---

crontab(1) - Linux manual page
    
- 
    
- 

    
        
            
                
                    

                        man7.org > Linux > man-pages
                    

                
                
                    
Linux/UNIX system programming training

                
            
        
    

# crontab(1) — Linux manual page

    
        

NAME | SYNOPSIS | DESCRIPTION | OPTIONS | CAVEATS | SEE ALSO | FILES | STANDARDS | DIAGNOSTICS | AUTHOR | COLOPHON
        

    

    
        

            
                
                    
                    
                    
                
            

        
    
     

CRONTAB(1)                    User Commands                    CRONTAB(1)

## NAME          top

       crontab - maintains crontab files for individual users

## SYNOPSIS          top

       crontab [-u user] <file | ->
       crontab [-T] <file | ->
       crontab [-u user] <-l | -r | -e> [-i] [-s]
       crontab -n [ hostname ]
       crontab -c
       crontab -V

## DESCRIPTION          top

       Crontab is the program used to install a crontab table file,
       remove or list the existing tables used to serve the cron(8)
       daemon.  Each user can have their own crontab, and though these
       are files in /var/spool/, they are not intended to be edited
       directly.  For SELinux in MLS mode, you can define more crontabs
       for each range.  For more information, see selinux(8).

       In this version of Cron it is possible to use a network-mounted
       shared /var/spool/cron across a cluster of hosts and specify that
       only one of the hosts should run the crontab jobs in the
       particular directory at any one time.  You may also use crontab
       from any of these hosts to edit the same shared set of crontab
       files, and to set and query which host should run the crontab
       jobs.

       Scheduling cron jobs with crontab can be allowed or disallowed for
       different users.  For this purpose, use the cron.allow and
       cron.deny files.  If the cron.allow file exists, a user must be
       listed in it to be allowed to use crontab.  If the cron.allow file
       does not exist but the cron.deny file does exist, then a user must
       not be listed in the cron.deny file in order to use crontab.  If
       neither of these files exist, then only the super user is allowed
       to use crontab.

       Another way to restrict the scheduling of cron jobs beyond crontab
       is to use PAM authentication in /etc/security/access.conf to set
       up users, which are allowed or disallowed to use crontab or modify
       system cron jobs in the /etc/cron.d/ directory.

       The temporary directory can be set in an environment variable.  If
       it is not set by the user, the /tmp directory is used.

       When listing a crontab on a terminal the output will be colorized
       unless an environment variable NO_COLOR is set.

       On edition or deletion of the crontab, a backup of the last
       crontab will be saved to $XDG_CACHE_HOME/crontab/crontab.bak or
       $XDG_CACHE_HOME/crontab/crontab.<user>.bak if -u is used.  If the
       XDG_CACHE_HOME environment variable is not set, $HOME/.cache will
       be used instead.

## OPTIONS          top

       -u     Specifies the name of the user whose crontab is to be
              modified.  If this option is not used, crontab examines
              "your" crontab, i.e., the crontab of the person executing
              the command. If no crontab exists for a particular user, it
              is created for them the first time the crontab -u command
              is used under their username.

       -T     Test the crontab file syntax without installing it.  Once
              an issue is found, the validation is interrupted, so this
              will not return all the existing issues at the same
              execution.

       -l     Displays the current crontab on standard output.

       -r     Removes the current crontab.

       -e     Edits the current crontab using the editor specified by the
              VISUAL or EDITOR environment variables.  After you exit
              from the editor, the modified crontab will be installed
              automatically.

       -i     This option modifies the -r option to prompt the user for a
              'y/Y' response before actually removing the crontab.

       -s     Appends the current SELinux security context string as an
              MLS_LEVEL setting to the crontab file before editing /
              replacement occurs - see the documentation of MLS_LEVEL in
              crontab(5).

       -n     This option is relevant only if cron(8) was started with
              the -c option, to enable clustering support.  It is used to
              set the host in the cluster which should run the jobs
              specified in the crontab files in the /var/spool/cron
              directory.  If a hostname is supplied, the host whose
              hostname returned by gethostname(2) matches the supplied
              hostname, will be selected to run the selected cron jobs
              subsequently.  If there is no host in the cluster matching
              the supplied hostname, or you explicitly specify an empty
              hostname, then the selected jobs will not be run at all.
              If the hostname is omitted, the name of the local host
              returned by gethostname(2) is used.  Using this option has
              no effect on the /etc/crontab file and the files in the
              /etc/cron.d directory, which are always run, and considered
              host-specific.  For more information on clustering support,
              see cron(8).

       -c     This option is only relevant if cron(8) was started with
              the -c option, to enable clustering support.  It is used to
              query which host in the cluster is currently set to run the
              jobs specified in the crontab files in the directory
              /var/spool/cron , as set using the -n option.

       -V     Print version and exit.

## CAVEATS          top

       The files cron.allow and cron.deny cannot be used to restrict the
       execution of cron jobs; they only restrict the use of crontab.  In
       particular, restricting access to crontab has no effect on an
       existing crontab of a user. Its jobs will continue to be executed
       until the crontab is removed.

       The files cron.allow and cron.deny must be readable by the user
       invoking crontab.  If this is not the case, then they are treated
       as non-existent.

## SEE ALSO          top

       crontab(5), cron(8)

## FILES          top

       /etc/cron.allow
       /etc/cron.deny

## STANDARDS          top

       The crontab command conforms to IEEE Std1003.2-1992 (``POSIX'')
       with one exception: For replacing the current crontab with data
       from standard input the - has to be specified on the command line
       if the standard input is a TTY.  This new command syntax differs
       from previous versions of Vixie Cron, as well as from the classic
       SVR3 syntax.

## DIAGNOSTICS          top

       An informative usage message appears if you run a crontab with a
       faulty command defined in it.

## AUTHOR          top

       Paul Vixie â¨vixie@isc.orgâ©
       Colin Dean â¨colin@colin-dean.orgâ©

## COLOPHON          top

       This page is part of the cronie (crond daemon) project.
       Information about the project can be found at 
       â¨https://github.com/cronie-crond/cronieâ©.  If you have a bug report
       for this manual page, see
       â¨https://github.com/cronie-crond/cronie/issuesâ©.  This page was
       obtained from the project's upstream Git repository
       â¨https://github.com/cronie-crond/cronie.gitâ© on 2026-01-16.  (At
       that time, the date of the most recent commit that was found in
       the repository was 2025-12-05.)  If you discover any rendering
       problems in this HTML version of the page, or you believe there is
       a better or more up-to-date source for the page, or you have
       corrections or improvements to the information in this COLOPHON
       (which is not part of the original manual page), send a mail to
       man-pages@man7.org

cronie                          2019-10-29                     CRONTAB(1)

Pages that refer to this page:
    cronnext(1), 
    pmsnap(1), 
    anacrontab(5), 
    crontab(5), 
    systemd.exec(5), 
    cron(8)

 

    
    
        

            HTML rendering created 2026-01-16
            by Michael Kerrisk,
            author of
            The Linux Programming Interface.
        

        

            For details of in-depth
            Linux/UNIX system programming training courses
            that I teach, look here.
        

        

            Hosting by jambit GmbH.
