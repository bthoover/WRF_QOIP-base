#! /bin/sh
########################################################################################
#
# Set python environment
#
########################################################################################
#
source activate bth-wrf_qoip
#
########################################################################################
#
# Collect user inputs
#
SENS_FILE=${1}
DR=${2}
NC_OUTFILE=${3}
PYTHON_PROG=${4}
#
########################################################################################
#
# Run python program
#
python3 ${PYTHON_PROG} << EOF
${SENS_FILE}
${DR}
${NC_OUTFILE}
EOF
#
########################################################################################
#
# END
#

