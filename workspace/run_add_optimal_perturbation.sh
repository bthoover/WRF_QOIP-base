#! /bin/sh
########################################################################################
#
directory_tree=${1}
iter_name=${2}
beg_yyyy=${3}
beg_mm=${4}
beg_dd=${5}
beg_hh=${6}
pert_mag=${7}
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
########################################################################################
#
# ADD OPTIMAL PERTURBATION
#
# Soft-link and copy required files
ln -sf ${work_dir}/optimal_pert_d01_${beg_date} opt_pert_file
ln -sf ${util_repo_dir}/add_optimal_perturbation.py prog.py
ln -sf ${util_repo_dir}/exec_add_optimal_perturbation.sh exec_script.sh
cp ${init_repo_dir}/wrfinput_d01 .
# Define settings
OLD_WRFINPUT_FILE=${work_dir}/wrfinput_d01
NEW_WRFINPUT_FILE=${work_dir}/wrfinput_d01_perturbed
OPT_PERT_FILE=${work_dir}/opt_pert_file
PYTHON_PROG=prog.py
# Define log file and run exec* script
LOG_FILE=add_optimal_perturbation_d01_${beg_date}.log
mkdir -p ${log_dir}
bash ${work_dir}/exec_script.sh ${OLD_WRFINPUT_FILE} ${NEW_WRFINPUT_FILE} ${OPT_PERT_FILE} ${pert_mag} ${PYTHON_PROG} > ${log_dir}/${LOG_FILE}
#
#
# Return to current directory
cd ${curr_dir}
#
########################################################################################
#
# END
#

