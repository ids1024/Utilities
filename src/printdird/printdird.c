#include <sys/inotify.h>
#include <unistd.h>
#include <limits.h>
#include <cups/cups.h>

#define BUF_LEN (sizeof(struct inotify_event) + NAME_MAX + 1)
#define WATCHPATH "/home/ian/.PRINT"

int main(int argc, char *argv[]) {
  cups_dest_t *dest;
  char *printer;
  int notify = inotify_init();

  if (inotify_add_watch(notify, WATCHPATH, IN_CLOSE_WRITE) == -1)
    return 1;
  if (chdir(WATCHPATH) != 0)
    return 1;

  // Get default printer
  if ((dest = cupsGetNamedDest(NULL, NULL, NULL)) == NULL)
    return 1;
  printer = strdup(dest->name);
  free(dest);

  while (1) {
    char buf[BUF_LEN];
    struct inotify_event *event;
    char *filename;
    int job_id;

    read(notify, buf, BUF_LEN);
    event = (struct inotify_event *)&buf[0];
    filename = event->name;
    if (filename[0] == '.')
      continue;

    job_id = cupsPrintFile(printer, filename, filename, 0, NULL);
    cupsStartDocument(CUPS_HTTP_DEFAULT, printer, job_id, NULL,
                      CUPS_FORMAT_AUTO, 1);
    unlink(filename);
  }
}
