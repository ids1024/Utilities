#include <sys/inotify.h>
#include <unistd.h>
#include <sys/wait.h>
#include <limits.h>

#define BUF_LEN ( sizeof(struct inotify_event) + NAME_MAX + 1 )

int main(int argc, char *argv[])
{
	int notify;
	char buf[BUF_LEN];
	struct inotify_event *event;
	const char *watchpath = "/home/ian/.PRINT";

	notify = inotify_init();
	
	if (inotify_add_watch(notify, watchpath, IN_CLOSE_WRITE) == -1)
		return 1;
	if (chdir(watchpath) !=0)
		return 1;

	while (1)
	{
		read(notify, buf, BUF_LEN);
		event = (struct inotify_event *) &buf[0];
		if (event->name[0] == '.')
			continue;
		if(fork() == 0) {
			execlp("lpr" ,"-r" , event->name, NULL);
			return 0;
		}
		wait(NULL);
		unlink(event->name);
	}
}
