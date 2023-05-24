#! /bin/sh
################################################################
#
# Set python environment
# 
source activate bth-wrf_qoip
#
################################################################
#
# Collect user inputs
#
OLD_WRFINPUT_FILE=${1}
NEW_WRFINPUT_FILE=${2}
ADJ_SENS_FILE=${3}
ADJ_INIT_FILE=${4}
UPTD_FCST_FILE=${5}
PTD_FCST_FILE=${6}
R_ERROR_THRESHOLD=${7}
DELR_ORIG=${8}
PERT_MAG=${9}
PYTHON_PROG=${10}
#
################################################################
#
# Run PYTHON_PROG
#
python3 ${PYTHON_PROG} << EOF
${OLD_WRFINPUT_FILE}
${NEW_WRFINPUT_FILE}
${ADJ_SENS_FILE}
${ADJ_INIT_FILE}
${UPTD_FCST_FILE}
${PTD_FCST_FILE}
${R_ERROR_THRESHOLD}
${DELR_ORIG}
${PERT_MAG}
EOF
#
################################################################
#
# END
#
