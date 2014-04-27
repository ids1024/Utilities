#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libgen.h>
#include <archive.h>
#include <archive_entry.h>

int main(int argc, char *argv[]) {
    struct archive *inarc;
    struct archive *outarc;
    struct archive_entry *entry;
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

    if (argc == 1) {
        printf("usage: rebuild-epub file\n");
        return 1;
    }

    inname = argv[1];

    outname = malloc(strlen(inname) + 4);
    strcpy(outname, inname);
    strcat(outname, ".new");

    infile = fopen(inname, "r");
    inarc = archive_read_new();
    archive_read_support_format_zip(inarc);
    archive_read_open_FILE(inarc, infile);

    outfile = fopen(outname, "w");
    outarc = archive_write_new();
    archive_write_set_format_zip(outarc);
    archive_write_open_FILE(outarc, outfile);

    while (archive_read_next_header(inarc, &entry) != ARCHIVE_EOF) {
        archive_write_header(outarc, entry);

        fullpath = strdup(archive_entry_pathname(entry));
        filename = basename(fullpath);
        path = dirname(fullpath);

        if (strcmp(path, "OEBPS/Text") == 0
            && (file = fopen(filename, "rb")) != NULL) {
            fseek(file, 0L, SEEK_END);
            size = ftell(file);
            fseek(file, 0L, SEEK_SET);
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
        archive_write_data(outarc, buff, size);
        free(buff);
    }

    archive_read_free(inarc);
    fclose(infile);
    archive_write_free(outarc);
    fclose(outfile);

    rename(outname, inname);
    return 0;
}
