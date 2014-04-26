include config.mk

SRC = rebuild-epub.c
OBJ = ${SRC:.c=.o}

all: rebuild-epub

${OBJ}: config.mk

rebuild-epub: ${OBJ}
	@echo CC -o $@
	@${CC} -o $@ ${OBJ} ${LDFLAGS}

clean:
	@echo cleaning
	@rm -f rebuild-epub ${OBJ}


install: all
	@echo installing executable file to ${DESTDIR}${PREFIX}/bin
	@mkdir -p ${DESTDIR}${PREFIX}/bin
	@cp -f rebuild-epub ${DESTDIR}${PREFIX}/bin
	@chmod 755 ${DESTDIR}${PREFIX}/bin/rebuild-epub

uninstall:
	@echo removing executable file from ${DESTDIR}${PREFIX}/bin
	@rm -f ${DESTDIR}${PREFIX}/bin/rebuild-epub

.PHONY: all clean install uninstall
