#! /bin/sh

directory_tree=${1}
beg_yyyy=${2}
beg_mm=${3}
beg_dd=${4}
beg_hh=${5}
end_yyyy=${6}
end_mm=${7}
end_dd=${8}
end_hh=${9}
R_error_threshold=${10}
delR_orig=${11}
pert_mag=${12}
#
beg_date=${beg_yyyy}-${beg_mm}-${beg_dd}_${beg_hh}:00:00
end_date=${end_yyyy}-${end_mm}-${end_dd}_${end_hh}:00:00
#
base_dir=`grep -- "base_dir" ${directory_tree} | awk '{print $2}'`
util_repo_dir=`grep -- "util_repo_dir" ${directory_tree} | awk '{print $2}'`
#
work_dir=${base_dir}/compute_R_error
# Move to work_dir
curr_dir=`pwd`
mkdir -p ${work_dir}
cd ${work_dir}
#
# Soft-link required files
#
ln -sf ${util_repo_dir}/compute_DELTAR_delR_ratio_error.py .
ln -sf ${util_repo_dir}/exec_compute_R_error.sh .
ln -sf ${base_dir}/nonlin_trj/wrfinput_d01 old_wrfinput
ln -sf ${base_dir}/inloop_trj/wrfinput_d01 new_wrfinput
ln -sf ${base_dir}/linear_adj/gradient_wrfplus_d01_${beg_date} adj_sens
ln -sf ${base_dir}/linear_adj/final_sens_d01_${end_date} adj_init
ln -sf ${base_dir}/nonlin_trj/wrfout_d01_${end_date} uptd_wrffcst
ln -sf ${base_dir}/inloop_trj/wrfout_d01_${end_date} ptd_wrffcst
#
# Run exec* script to compute R_error, store in R_error.txt
#
./exec_compute_R_error.sh old_wrfinput new_wrfinput adj_sens adj_init uptd_wrffcst ptd_wrffcst ${R_error_threshold} ${delR_orig} ${pert_mag} compute_DELTAR_delR_ratio_error.py
# Return to prior directory
cd ${curr_dir}
#
# END
#
