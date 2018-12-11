#!/bin/sh

exec mvn exec:java -Dexec.mainClass="cz.vutbr.fit.pdb.project01.App" -Dexec.args="$*"
