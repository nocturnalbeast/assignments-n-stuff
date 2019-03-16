COMP = gcc
OBJ_SCNR = virus_scanner
ADD_OBJS = infector infector_mini the_buster hex_dump_stub
CFLAGS = -Wall -Wformat-truncation=0
CFLAGS_SCNR =  -lssl -lcrypto
EXECDIR = ./bin


default:
	mkdir -p ${EXECDIR}
	${COMP} ${OBJ_SCNR}.c ${CFLAGS} ${CFLAGS_SCNR} -o ${EXECDIR}/${OBJ_SCNR}
	@for OBJ in $(ADD_OBJS); do \
		${COMP} $$OBJ.c ${CFLAGS} -o ${EXECDIR}/$$OBJ; \
	done

clean:
	-rm -rf ${EXECDIR}