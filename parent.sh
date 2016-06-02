#!/bin/sh
#
sh stanford-postagger.sh > data/output_pos.txt
sh /usr/local/Cellar/stanford-parser/3.5.2/libexec/lexparser.sh data/plot_summary_all.txt > data/output_dep.txt
