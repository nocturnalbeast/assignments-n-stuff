COMP = gcc
OBJ = parser
FLAGS = -Wall
EXECDIR = ./bin/
LOGFILE = ../eelotracker.log

default:
	mkdir ${EXECDIR}
	${COMP} ${OBJ}.c ${FLAGS} -o ${EXECDIR}${OBJ}

clean:
	-rm -rf ${EXECDIR}

run:
	${EXECDIR}${OBJ} ${LOGFILE}
