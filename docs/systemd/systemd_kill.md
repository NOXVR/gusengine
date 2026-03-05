# Source: https://man7.org/linux/man-pages/man5/systemd.kill.5.html
# Downloaded: 2026-02-16

---

systemd.kill(5) - Linux manual page
    
- 
    
- 

    
        
            
                
                    

                        man7.org > Linux > man-pages
                    

                
                
                    
Linux/UNIX system programming training

                
            
        
    

# systemd.kill(5) — Linux manual page

    
        

NAME | SYNOPSIS | DESCRIPTION | OPTIONS | SEE ALSO | COLOPHON
        

    

    
        

            
                
                    
                    
                    
                
            

        
    
     

SYSTEMD.KILL(5)                systemd.kill               SYSTEMD.KILL(5)

## NAME          top

       systemd.kill - Process killing procedure configuration

## SYNOPSIS          top

       service.service, socket.socket, mount.mount, swap.swap,
       scope.scope

## DESCRIPTION          top

       Unit configuration files for services, sockets, mount points, swap
       devices and scopes share a subset of configuration options which
       define the killing procedure of processes belonging to the unit.

       This man page lists the configuration options shared by these five
       unit types. See systemd.unit(5) for the common options shared by
       all unit configuration files, and systemd.service(5),
       systemd.socket(5), systemd.swap(5), systemd.mount(5) and
       systemd.scope(5) for more information on the configuration file
       options specific to each unit type.

       The kill procedure configuration options are configured in the
       [Service], [Socket], [Mount] or [Swap] section, depending on the
       unit type.

## OPTIONS          top

       KillMode=
           Specifies how processes of this unit shall be killed. One of
           control-group, mixed, process, none.

           If set to control-group, all remaining processes in the
           control group of this unit will be killed on unit stop (for
           services: after the stop command is executed, as configured
           with ExecStop=). If set to mixed, the SIGTERM signal (see
           below) is sent to the main process while the subsequent
           SIGKILL signal (see below) is sent to all remaining processes
           of the unit's control group. If set to process, only the main
           process itself is killed (not recommended!). If set to none,
           no process is killed (strongly recommended against!). In this
           case, only the stop command will be executed on unit stop, but
           no process will be killed otherwise. Processes remaining alive
           after stop are left in their control group and the control
           group continues to exist after stop unless empty.

           Note that it is not recommended to set KillMode= to process or
           even none, as this allows processes to escape the service
           manager's lifecycle and resource management, and to remain
           running even while their service is considered stopped and is
           assumed to not consume any resources.

           Processes will first be terminated via SIGTERM (unless the
           signal to send is changed via KillSignal= or
           RestartKillSignal=). Optionally, this is immediately followed
           by a SIGHUP (if enabled with SendSIGHUP=). If processes still
           remain after:

           â¢   the main process of a unit has exited (applies to
               KillMode=: mixed)

           â¢   the delay configured via the TimeoutStopSec= has passed
               (applies to KillMode=: control-group, mixed, process)

           the termination request is repeated with the SIGKILL signal or
           the signal specified via FinalKillSignal= (unless this is
           disabled via the SendSIGKILL= option). See kill(2) for more
           information.

           Defaults to control-group.

           Added in version 187.

       KillSignal=
           Specifies which signal to use when stopping a service. This
           controls the signal that is sent as first step of shutting
           down a unit (see above), and is usually followed by SIGKILL
           (see above and below). For a list of valid signals, see
           signal(7). Defaults to SIGTERM.

           Note that, right after sending the signal specified in this
           setting, systemd will always send SIGCONT, to ensure that even
           suspended tasks can be terminated cleanly.

           Added in version 187.

       RestartKillSignal=
           Specifies which signal to use when restarting a service. The
           same as KillSignal= described above, with the exception that
           this setting is used in a restart job. Not set by default, and
           the value of KillSignal= is used.

           Added in version 244.

       SendSIGHUP=
           Specifies whether to send SIGHUP to remaining processes
           immediately after sending the signal configured with
           KillSignal=. This is useful to indicate to shells and
           shell-like programs that their connection has been severed.
           Takes a boolean value. Defaults to "no".

           Added in version 207.

       SendSIGKILL=
           Specifies whether to send SIGKILL (or the signal specified by
           FinalKillSignal=) to remaining processes after a timeout, if
           the normal shutdown procedure left processes of the service
           around. When disabled, a KillMode= of control-group or mixed
           service will not restart if processes from prior services
           exist within the control group. Takes a boolean value.
           Defaults to "yes".

           Added in version 187.

       FinalKillSignal=
           Specifies which signal to send to remaining processes after a
           timeout if SendSIGKILL= is enabled. The signal configured here
           should be one that is not typically caught and processed by
           services (SIGTERM is not suitable). Developers can find it
           useful to use this to generate a coredump to troubleshoot why
           a service did not terminate upon receiving the initial SIGTERM
           signal. This can be achieved by configuring LimitCORE= and
           setting FinalKillSignal= to either SIGQUIT or SIGABRT.
           Defaults to SIGKILL.

           Added in version 240.

       WatchdogSignal=
           Specifies which signal to use to terminate the service when
           the watchdog timeout expires (enabled through WatchdogSec=).
           Defaults to SIGABRT.

           Added in version 240.

## SEE ALSO          top

       systemd(1), systemctl(1), journalctl(1), systemd.unit(5),
       systemd.service(5), systemd.socket(5), systemd.swap(5),
       systemd.mount(5), systemd.exec(5), systemd.directives(7), kill(2),
       signal(7)

## COLOPHON          top

       This page is part of the systemd (systemd system and service
       manager) project.  Information about the project can be found at
       â¨http://www.freedesktop.org/wiki/Software/systemdâ©.  If you have a
       bug report for this manual page, see
       â¨http://www.freedesktop.org/wiki/Software/systemd/#bugreportsâ©.
       This page was obtained from the project's upstream Git repository
       â¨https://github.com/systemd/systemd.gitâ© on 2026-01-16.  (At that
       time, the date of the most recent commit that was found in the
       repository was 2026-01-16.)  If you discover any rendering
       problems in this HTML version of the page, or you believe there is
       a better or more up-to-date source for the page, or you have
       corrections or improvements to the information in this COLOPHON
       (which is not part of the original manual page), send a mail to
       man-pages@man7.org

systemd 260~devel                                         SYSTEMD.KILL(5)

Pages that refer to this page:
    systemd-run(1), 
    systemd.automount(5), 
    systemd.exec(5), 
    systemd.mount(5), 
    systemd.path(5), 
    systemd.scope(5), 
    systemd.service(5), 
    systemd.socket(5), 
    systemd.swap(5), 
    systemd.timer(5), 
    systemd.directives(7), 
    systemd.index(7)

 

    
    
        

            HTML rendering created 2026-01-16
            by Michael Kerrisk,
            author of
            The Linux Programming Interface.
        

        

            For details of in-depth
            Linux/UNIX system programming training courses
            that I teach, look here.
        

        

            Hosting by jambit GmbH.
