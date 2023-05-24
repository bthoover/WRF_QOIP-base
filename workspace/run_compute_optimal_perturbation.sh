#! /bin/sh
########################################################################################
#
directory_tree=${1}
iter_name=${2}
beg_yyyy=${3}
beg_mm=${4}
beg_dd=${5}
beg_hh=${6}
DR=${7}
#
base_dir=`grep -- "base_dir" ${directory_tree} | awk '{print $2}'`
util_repo_dir=`grep -- "util_repo_dir" ${directory_tree} | awk '{print $2}'`
#
curr_dir=`pwd`
wrfplus_adj_dir=${base_dir}/linear_adj
work_dir=${base_dir}/opt_pert
log_dir=${work_dir}/logs
init_repo_dir=${base_dir}/archive/${iter_name}
#
beg_date=${beg_yyyy}-${beg_mm}-${beg_dd}_${beg_hh}:00:00
#
# Move to work_dir
mkdir -p ${work_dir}
cd ${work_dir}
#
# COMPUTE OPTIMAL PERTURBATION
#
# Soft-link required files
ln -sf ${wrfplus_adj_dir}/gradient_wrfplus_d01_${beg_date} sens_file
ln -sf ${util_repo_dir}/compute_optimal_perturbation.py prog.py
ln -sf ${util_repo_dir}/exec_compute_optimal_perturbation.sh exec_script.sh
# Define settings
SENS_FILE=${work_dir}/sens_file
NC_OUTFILE=${work_dir}/optimal_pert_d01_${beg_date}
PYTHON_PROG=prog.py
# Define log file and run exec* script
LOG_FILE=compute_optimal_perturbation_d01_${beg_date}.log
mkdir -p ${log_dir}
bash ${work_dir}/exec_script.sh ${SENS_FILE} ${DR} ${NC_OUTFILE} ${pert_mag} ${PYTHON_PROG} > ${log_dir}/${LOG_FILE}
#
# Return to current directory
cd ${curr_dir}
#
########################################################################################
#
# END
#

