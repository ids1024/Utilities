from ianxenv import Task

sxhkd = Task("sxhkd", background=True)
xcmenu = Task("xcmenu", "--daemon")
xautolock = Task("xautolock", "-time", "5", "-locker", "slock", background=True)
hsetroot = Task("hsetroot", "-full", "/home/ian/Pictures/desktop.png")
aria2 = Task("aria2c", "--enable-rpc", "--daemon")
wmname = Task("wmname", "LG3D")
jack = Task("start-jack")
redshift = Task("redshift", background=True)
xmodmap = Task("xmodmap", "/home/ian/.Xmodmap") #Required for mdev


wicdgtk = Task("wicd-gtk", "-t", background=True)
compton = Task("compton", "--config", "~/.compton.conf", "-b", background=True)

dstatus = Task("dstatus", background=True)
dwmstatuspy = Task("dwmstatus.py")

environments = (
        ('i3', 'i3', (sxhkd, xcmenu, xautolock, hsetroot, aria2)),
        ('awesome', 'awesome', None),
        ('dwm','dwm', (dwmstatuspy ,sxhkd, xcmenu, xautolock, hsetroot, aria2, wmname, redshift, xmodmap)),
        #('dwm','dwm', (sxhkd, xcmenu, xautolock, hsetroot, aria2)),
        ('e18', 'enlightenment_start', None),
        ('rio', ('9','rio'), None),
        ('icewm', 'icewm', compton),
        ('0ad', '0ad', None),
        ('supertux', 'supertux2', None),
        ('lxqt', 'lxqt-session', None),
        ('xterm', 'xterm', None),
        ('dosbox', 'dosbox', None),
        ('gnome', 'gnome-session', None),
        ('xmonad', 'xmonad', None),
        )

default_environment = 'dwm'
