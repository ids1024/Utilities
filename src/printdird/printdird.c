#include <sys/inotify.h>
#include <unistd.h>
#include <limits.h>
#include <cups/cups.h>

#define BUF_LEN ( sizeof(struct inotify_event) + NAME_MAX + 1 )

int main(int argc, char *argv[])
{
    int notify;
    char buf[BUF_LEN];
    struct inotify_event *event;
    cups_dest_t *dest;
    char *printer;
    char *filename;
    int job_id;
    const char *watchpath = "/home/ian/.PRINT";

    notify = inotify_init();
    
    if (inotify_add_watch(notify, watchpath, IN_CLOSE_WRITE) == -1)
        return 1;
    if (chdir(watchpath) !=0)
        return 1;

    //Get default printer
    if ((dest = cupsGetNamedDest(NULL, NULL, NULL)) == NULL ) 
	    return 1;
    printer = dest->name;


    while (1)
    {
        read(notify, buf, BUF_LEN);
        event = (struct inotify_event *) &buf[0];
	filename = event->name;
        if (filename[0] == '.')
            continue;

        job_id = cupsPrintFile(printer, filename, filename, 0, NULL);
        cupsStartDocument(CUPS_HTTP_DEFAULT, printer, job_id, NULL, CUPS_FORMAT_AUTO, 1);
        unlink(filename);
    }
}
