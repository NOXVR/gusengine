# Source: https://man7.org/linux/man-pages/man5/systemd.target.5.html
# Downloaded: 2026-02-16

---

systemd.target(5) - Linux manual page
    
- 
    
- 

    
        
            
                
                    

                        man7.org > Linux > man-pages
                    

                
                
                    
Linux/UNIX system programming training

                
            
        
    

# systemd.target(5) — Linux manual page

    
        

NAME | SYNOPSIS | DESCRIPTION | AUTOMATIC DEPENDENCIES | OPTIONS | EXAMPLE | SEE ALSO | COLOPHON
        

    

    
        

            
                
                    
                    
                    
                
            

        
    
     

SYSTEMD.TARGET(5)             systemd.target            SYSTEMD.TARGET(5)

## NAME          top

       systemd.target - Target unit configuration

## SYNOPSIS          top

       target.target

## DESCRIPTION          top

       A unit configuration file whose name ends in ".target" encodes
       information about a target unit of systemd. Target units are used
       to group units and to set synchronization points for ordering
       dependencies with other unit files.

       This unit type has no specific options. See systemd.unit(5) for
       the common options of all unit configuration files. The common
       configuration items are configured in the generic [Unit] and
       [Install] sections. A separate [Target] section does not exist,
       since no target-specific options may be configured.

       Target units do not offer any additional functionality on top of
       the generic functionality provided by units. They merely group
       units, allowing a single target name to be used in Wants= and
       Requires= settings to establish a dependency on a set of units
       defined by the target, and in Before= and After= settings to
       establish ordering. Targets establish standardized names for
       synchronization points during boot and shutdown. Importantly, see
       systemd.special(7) for examples and descriptions of standard
       systemd targets.

       Target units provide a more flexible replacement for SysV
       runlevels in the classic SysV init system.

       Note that a target unit file must not be empty, lest it be
       considered a masked unit. It is recommended to provide a [Unit]
       section which includes informative Description= and Documentation=
       options.

## AUTOMATIC DEPENDENCIES          top

   Implicit Dependencies
       There are no implicit dependencies for target units.

   Default Dependencies
       The following dependencies are added unless DefaultDependencies=no
       is set:

       â¢   Target units will automatically complement all configured
           dependencies of type Wants= or Requires= with dependencies of
           type After= unless DefaultDependencies=no is set in the
           specified units.

           Note that the reverse is not true. For example, defining
           Wants=that.target in some.service will not automatically add
           the After=that.target ordering dependency for some.service.
           Instead, some.service should use the primary synchronization
           function of target type units, by setting a specific
           After=that.target or Before=that.target ordering dependency in
           its .service unit file.

       â¢   Target units automatically gain Conflicts= and Before=
           dependencies against shutdown.target.

## OPTIONS          top

       Target unit files may include [Unit] and [Install] sections, which
       are described in systemd.unit(5). No options specific to this file
       type are supported.

## EXAMPLE          top

       Example 1. Simple standalone target

           # emergency-net.target

           [Unit]
           Description=Emergency Mode with Networking
           Requires=emergency.target systemd-networkd.service
           After=emergency.target systemd-networkd.service
           AllowIsolate=yes

       When adding dependencies to other units, it is important to check
       if they set DefaultDependencies=. Service units, unless they set
       DefaultDependencies=no, automatically get a dependency on
       sysinit.target. In this case, both emergency.target and
       systemd-networkd.service have DefaultDependencies=no, so they are
       suitable for use in this target, and do not pull in
       sysinit.target.

       You can now switch into this emergency mode by running systemctl
       isolate emergency-net.target or by passing the option
       systemd.unit=emergency-net.target on the kernel command line.

       Other units can have WantedBy=emergency-net.target in the
       [Install] section. After they are enabled using systemctl enable,
       they will be started before emergency-net.target is started. It is
       also possible to add arbitrary units as dependencies of
       emergency.target without modifying them by using systemctl
       add-wants.

## SEE ALSO          top

       systemd(1), systemctl(1), systemd.unit(5), systemd.special(7),
       systemd.directives(7)

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

systemd 260~devel                                       SYSTEMD.TARGET(5)

Pages that refer to this page:
    systemctl(1), 
    systemd(1), 
    systemd.unit(5), 
    bootup(7), 
    systemd.directives(7), 
    systemd.index(7), 
    systemd.special(7), 
    systemd.syntax(7), 
    systemd-xdg-autostart-generator(8)

 

    
    
        

            HTML rendering created 2026-01-16
            by Michael Kerrisk,
            author of
            The Linux Programming Interface.
        

        

            For details of in-depth
            Linux/UNIX system programming training courses
            that I teach, look here.
        

        

            Hosting by jambit GmbH.
