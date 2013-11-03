libfunctions.so: functions.o
	gcc -shared -o libfunctions.so functions.o

functions.o: functions.c
	gcc -Wall -fPIC -c functions.c

clean:
	rm -f *.exe *.o *.stackdump *~

backup:
	test -d backups || mkdir backups
	cp *.cpp backups
	cp *.h backups
	cp Makefile backups
