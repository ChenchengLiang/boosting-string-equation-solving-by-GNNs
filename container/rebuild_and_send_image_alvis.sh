#!/bin/bash
rm alvis_word_equation_recipe-A100.sif

apptainer build alvis_word_equation_recipe-A100.sif alvis_word_equation_recipe-A100.def


echo "send to alvis"
send_to_alvis alvis_word_equation_recipe-A100.sif /cephyr/users/liangch/Alvis/container


echo "done" 
