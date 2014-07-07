#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libgen.h>
#include <archive.h>
#include <archive_entry.h>
#include <sys/stat.h>

int main(int argc, char *argv[]) {
    struct archive *inarc;
    struct archive *outarc;
    struct archive_entry *entry;
    struct archive_entry *newentry;
    FILE *infile;
    FILE *outfile;
    char *inname;
    char *outname;
    char *fullpath;
    char *path;
    char *filename;
    void *buff;
    FILE *file;
    int size;
    struct stat st;

    if (argc == 1) {
        printf("usage: rebuild-epub file\n");
        return 1;
    }

    inname = realpath(argv[1], NULL);

    outname = malloc(strlen(inname) + 4);
    strcpy(outname, inname);
    strcat(outname, ".new");

    inarc = archive_read_new();
    archive_read_support_format_zip(inarc);
    archive_read_open_filename(inarc, inname, sysconf(_SC_PAGESIZE));

    outarc = archive_write_new();
    archive_write_set_format_zip(outarc);
    archive_write_open_filename(outarc, outname);

    while (archive_read_next_header(inarc, &entry) != ARCHIVE_EOF) {
        newentry = archive_entry_clone(entry);

        fullpath = strdup(archive_entry_pathname(entry));
        filename = basename(fullpath);
        path = dirname(fullpath);

        if (strcmp(path, "OEBPS/Text") == 0
            && (file = fopen(filename, "rb")) != NULL) {
            stat(filename, &st);
	    size = st.st_size;

            buff = malloc(size);
            fread(buff, size, 1, file);
            fclose(file);
            printf("Replaced %s\n", filename);
        }
        else {
            size = archive_entry_size(entry);
            buff = malloc(size);
            archive_read_data(inarc, buff, size);
        }
        free(fullpath); 
        archive_write_header(outarc, newentry);
        archive_write_data(outarc, buff, size);
        free(buff);
    }

    archive_read_free(inarc);
    archive_write_free(outarc);

    rename(outname, inname);
    free(inname);
    free(outname);
    return 0;
}
