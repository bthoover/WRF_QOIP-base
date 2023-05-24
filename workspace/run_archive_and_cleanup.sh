#! /bin/sh
#######################################################################################################
#
# DESCRIPTION
#
# Moves key files on an iteration to an archive. These include:
#
# 1. original (unperturbed) wrfinput and wrfbdy files that were used to initialize the trajectory-run
# 2. wrfout files produced for the trajectory-run
# 3. final-time wrfout file produced from the final inner-loop run
# 4. final_sens initialization file for adjoint-run
# 5. gradient_wrfplus and gradient_wrfbdy sensitivity files for adjoint-run
# 6. optimal perturbation file
# 7. new (perturbed) wrfinput file incorporating optimal perturbation
# 8. inner-loop statistics file
#
#######################################################################################################
#
directory_tree=${1}
arch_name=${2}
next_arch_name=${3}
beg_yyyy=${4}
beg_mm=${5}
beg_dd=${6}
beg_hh=${7}
end_yyyy=${8}
end_mm=${9}
end_dd=${10}
end_hh=${11}
#
beg_date=${beg_yyyy}-${beg_mm}-${beg_dd}_${beg_hh}:00:00
end_date=${end_yyyy}-${end_mm}-${end_dd}_${end_hh}:00:00
#
base_dir=`grep -- "base_dir" ${directory_tree} | awk '{print $2}'`
#
wrfplus_trj_dir=${base_dir}/nonlin_trj
wrfplus_adj_dir=${base_dir}/linear_adj
optimal_prt_dir=${base_dir}/opt_pert
innerlo_trj_dir=${base_dir}/inloop_trj
compute_err_dir=${base_dir}/compute_R_error
#
arch_dir=${base_dir}/archive/${arch_name}
next_arch_dir=${base_dir}/archive/${next_arch_name}
mkdir -p ${arch_dir}
mkdir -p ${next_arch_dir}
# Copy files to archive:
# 1. original (unperturbed) wrfinput and wrfbdy files that were used to initialize the trajectory-run
cp ${wrfplus_trj_dir}/wrfinput_d01 ${arch_dir}/.
cp ${wrfplus_trj_dir}/wrfbdy_d01 ${arch_dir}/.
# 2. wrfout files produced for the trajectory-run
cp ${wrfplus_trj_dir}/wrfout_d01_* ${arch_dir}/.
# 3. final-time wrfout file produced from the final inner-loop run
cp ${innerlo_trj_dir}/wrfout_d01_${end_date} ${arch_dir}/wrfout_d01_${end_date}_perturbed
# 4. final_sens initialization file for adjoint-run
cp ${wrfplus_adj_dir}/final_sens_d01_${end_date} ${arch_dir}/.
# 5. gradient_wrfplus and gradient_wrfbdy sensitivity files for adjoint-run
cp ${wrfplus_adj_dir}/gradient_wrfplus_d01_${beg_date} ${arch_dir}/.
cp ${wrfplus_adj_dir}/gradient_wrfbdy_d01 ${arch_dir}/.
# 6. optimal perturbation file
cp ${optimal_prt_dir}/optimal_pert_d01_${beg_date} ${arch_dir}/.
# 7. new (perturbed) wrfinput file incorporating optimal perturbation
cp ${optimal_prt_dir}/wrfinput_d01_perturbed ${arch_dir}/.
# 8. inner-loop statistics file
mv ${base_dir}/inner_loop_stats.txt ${arch_dir}/.
#
# In addition, we are going to copy the perturbed wrfinput and (currently unperturbed) wrfbdy files
# to next_arch_dir as the original (unperturbed) wrfinput and wrfbdy files for the next iteration
#
cp ${optimal_prt_dir}/wrfinput_d01_perturbed ${next_arch_dir}/wrfinput_d01
cp ${wrfplus_trj_dir}/wrfbdy_d01 ${next_arch_dir}/.
# Remove working directories for this run
rm -rf ${wrfplus_trj_dir}
rm -rf ${wrfplus_adj_dir}
rm -rf ${optimal_prt_dir}
rm -rf ${innerlo_trj_dir}
rm -rf ${compute_err_dir}
#
# END
#
