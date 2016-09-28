#!/bin/sh
python preprocess.py --srcfile ../NUCLE2014_colloc/src-train.txt --targetfile ../NUCLE2014_colloc/targ-train.txt \
--srcvalfile ../NUCLE2014_colloc/src-val.txt --targetvalfile ../NUCLE2014_colloc/targ-val.txt --outputfile ../NUCLE2014_colloc/nucle2014_colloc
