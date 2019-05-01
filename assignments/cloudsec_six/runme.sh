#!/bin/bash

# compiling and packaging the code
javac -cp $(hadoop classpath) ./programs/*.java
jar cf package.jar *.class
rm -rf *.class

# copying sample datasets over to HadoopFS
hadoop fs -mkdir /user/prgs-input
hadoop fs -put ./inputs/book.txt /user/prgs-input/book.txt
hadoop fs -put ./inputs/log.txt /user/prgs-input/log.txt

# executing the jobs from the packaged JAR file
hadoop jar ./package.jar WordCount /user/prgs-input/book.txt /user/wdc-output/
hadoop jar ./package.jar LogIPCount /user/prgs-input/log.txt /user/ipc-output/

# viewing the success/failure status and output of the jobs
hadoop fs -ls /user/wdc-output
hadoop fs -cat /user/wdc-output/part-r-00000
hadoop fs -ls /user/ipc-output
hadoop fs -cat /user/ipc-output/part-r-00000

# extracting the output of the jobs
mkdir outputs
hadoop fs -get /user/wdc-output/part-r-00000 ./outputs/wdc-op.txt
hadoop fs -get /user/ipc-output/part-r-00000 ./outputs/ipc-op.txt
