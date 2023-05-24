#! /bin/sh
#
# REQUIRED SETTINGS
#
# directory_tree ............................... full-path to text file containing directory-tree for run
# iter_name .................................... name of current iteration
# next_iter_name ............................... name of next iteration (wrf input files for next iteration will be placed here)
# beg_yyyy ..................................... beginning year of trajectory
# beg_mm ....................................... beginning month of trajectory
# beg_dd ....................................... beginning day of trajectory
# beg_hh ....................................... beginning hour of trajectory
# end_yyyy ..................................... ending year of trajectory
# end_mm ....................................... ending month of trajectory
# end_dd ....................................... ending day of trajectory
# end_hh ....................................... ending hour of trajectory
# R_error_threshold ............................ threshold of allowable error in adjoint-estimate of dR, as fractional percentage
# dR ........................................... target dR value for optimal perturbation
#
directory_tree=/Users/hoover/WRF_QOIP/nov2019_q/workspace/directory_tree.txt
iter_name=iter_22
next_iter_name=iter_23
beg_yyyy=2019
beg_mm=11
beg_dd=25
beg_hh=12
end_yyyy=2019
end_mm=11
end_dd=27
end_hh=00
R_error_threshold=0.5
dR=-44100.0
#
# Move to base_dir
#
base_dir=`grep -- "base_dir" ${directory_tree} | awk '{print $2}'`
util_repo_dir=`grep -- "util_repo_dir" ${directory_tree} | awk '{print $2}'`
#
cd ${base_dir} 
#
# Run forward trajectory
#
echo "running forward trajectory..."
./run_trj.csh ${directory_tree} ${iter_name}
#
# Run adjoint
#
echo "running adjoint..."
./run_adj.csh ${directory_tree} ${iter_name} ${end_yyyy} ${end_mm} ${end_dd} ${end_hh}
#
# Run compute optimal perturbation
#
echo "running compute optimal perturbation..."
./run_compute_optimal_perturbation.sh ${directory_tree} ${iter_name} ${beg_yyyy} ${beg_mm} ${beg_dd} ${beg_hh} ${dR}
#
# INNER LOOP
#
P_MAG=1.0
#
# Add optimal perturbation at P_MAG magnitude 
#
echo "running add optimal perturbation..."
./run_add_optimal_perturbation.sh ${directory_tree} ${iter_name} ${beg_yyyy} ${beg_mm} ${beg_dd} ${beg_hh} ${P_MAG}
#
# Run inner-loop 
#
echo "running inner-loop trajectory..."
./run_trj_inner_loop.csh ${directory_tree} ${iter_name}
#
# Run compute R-error
#
echo "running compute R-error..."
./run_compute_R_error.sh ${directory_tree} ${beg_yyyy} ${beg_mm} ${beg_dd} ${beg_hh} ${end_yyyy} ${end_mm} ${end_dd} ${end_hh} ${R_error_threshold} ${dR} ${P_MAG}
#
# Extract error values and accept/reject from R_error.txt and set inner-loop counter
#
DELTA_R=`head -1 ${base_dir}/compute_R_error/R_error.txt | awk '{print $1}'`
del_R=`head -1 ${base_dir}/compute_R_error/R_error.txt | awk '{print $2}'`
del_R_orig=`head -1 ${base_dir}/compute_R_error/R_error.txt | awk '{print $3}'`
R_err=`head -1 ${base_dir}/compute_R_error/R_error.txt | awk '{print $4}'`
let acc_rej=`head -1 ${base_dir}/compute_R_error/R_error.txt | awk '{print $5}'`
let il_cnt=0
# Record inner-loop statistics
echo "${il_cnt} ${DELTA_R} ${del_R} ${del_R_orig} ${R_err} ${R_error_threshold} ${acc_rej}" > ${base_dir}/inner_loop_stats.txt
while [ ${acc_rej} -lt 0 ]
do
    # Increment il_cnt
    let il_cnt++
    echo "INNER LOOP COUNT: ${il_cnt}"
    # Remove inloop_trj and compute_R_error directories
    rm -rf ${base_dir}/inloop_trj
    rm -rf ${base_dir}/compute_R_error
    # Remove wrfinput_d01_perturbed from opt_pert
    rm ${base_dir}/opt_pert/wrfinput_d01_perturbed
    # Reduce P_MAG by 0.1
    P_MAG=`awk "BEGIN{print ${P_MAG}-0.1}"`
    #
    # Add optimal perturbation at P_MAG magnitude 
    #
    echo "running add optimal perturbation..."
    ./run_add_optimal_perturbation.sh ${directory_tree} ${iter_name} ${beg_yyyy} ${beg_mm} ${beg_dd} ${beg_hh} ${P_MAG}
    #
    # Run inner-loop 
    #
    echo "running inner-loop trajectory..."
    ./run_trj_inner_loop.csh ${directory_tree} ${iter_name}
    #
    # Run compute R-error
    #
    echo "running compute R-error..."
    ./run_compute_R_error.sh ${directory_tree} ${beg_yyyy} ${beg_mm} ${beg_dd} ${beg_hh} ${end_yyyy} ${end_mm} ${end_dd} ${end_hh} ${R_error_threshold} ${dR} ${P_MAG}
    #
    # Extract error values and accept/reject from R_error.txt
    #
    DELTA_R=`head -1 ${base_dir}/compute_R_error/R_error.txt | awk '{print $1}'`
    del_R=`head -1 ${base_dir}/compute_R_error/R_error.txt | awk '{print $2}'`
    del_R_orig=`head -1 ${base_dir}/compute_R_error/R_error.txt | awk '{print $3}'`
    R_err=`head -1 ${base_dir}/compute_R_error/R_error.txt | awk '{print $4}'`
    let acc_rej=`head -1 ${base_dir}/compute_R_error/R_error.txt | awk '{print $5}'`
    # Record inner-loop statistics
    echo "${il_cnt} ${DELTA_R} ${del_R} ${del_R_orig} ${R_err} ${R_error_threshold} ${acc_rej}" >> ${base_dir}/inner_loop_stats.txt
done
#
# Run archive/cleanup
#
echo "running archive/cleanup..."
./run_archive_and_cleanup.sh ${directory_tree} ${iter_name} ${next_iter_name} ${beg_yyyy} ${beg_mm} ${beg_dd} ${beg_hh} ${end_yyyy} ${end_mm} ${end_dd} ${end_hh}
#
# END
#
echo "DONE!"
