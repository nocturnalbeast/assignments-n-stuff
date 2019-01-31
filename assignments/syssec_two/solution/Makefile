COMP = gcc
OBJ = unshadow
CFLAGS = -Wall -lcrypt -lm
EXECDIR = ./bin

LEV_ONE_DIRS := gecos_lists dictionary_lists
LEV_TWO_DIRS := hashlists plainlists

DEF_PASSWD = ../passwd_file.txt
DEF_SHADOW = ../shadow_file.txt
DEF_DICT = ../dictionary_file.txt
DEF_OUTPUT = ../cracked_output.txt

default: generate
	${COMP} ${OBJ}.c ${CFLAGS} -o ${EXECDIR}/${OBJ}

generate:
	@for L_ONE in $(LEV_ONE_DIRS); do \
		for L_TWO in $(LEV_TWO_DIRS); do \
			mkdir -p ${EXECDIR}/$$L_ONE/$$L_TWO; \
		done \
	done

clean:
	-rm -f ${EXECDIR}/${OBJ}

freshen:
	@for L_ONE in $(LEV_ONE_DIRS); do \
		rm -rf ${EXECDIR}/$$L_ONE; \
	done

run:
	${EXECDIR}/${OBJ} -p ${DEF_PASSWD} -s ${DEF_SHADOW} -d ${DEF_DICT} -o ${DEF_OUTPUT} -v -c
