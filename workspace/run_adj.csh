#!/bin/tcsh

set directory_tree=${1}
set iter_name=${2}
set end_yyyy=${3}
set end_mm=${4}
set end_dd=${5}
set end_hh=${6}

set base_dir=`grep -- "base_dir" ${directory_tree} | awk '{print $2}'`
set wrfplus_repo_dir=`grep -- "wrfplus_repo_dir" ${directory_tree} | awk '{print $2}'`
set namelist_repo_dir=`grep -- "namelist_repo_dir" ${directory_tree} | awk '{print $2}'`
set util_repo_dir=`grep -- "util_repo_dir" ${directory_tree} | awk '{print $2}'`

set end_date=${end_yyyy}-${end_mm}-${end_dd}_${end_hh}:00:00

set wrfplus_trj_dir=${base_dir}/nonlin_trj
set work_dir=${base_dir}/linear_adj
set init_repo_dir=${base_dir}/archive/${iter_name}

set curr_dir=`pwd`
echo "moving from ${curr_dir} to ${work_dir}..."

mkdir -p ${work_dir}
cd ${work_dir}
# Soft-link required files from wrfplus_repo_dir
ln -sf ${wrfplus_repo_dir}/main/wrf.exe .
ln -sf ${wrfplus_repo_dir}/run/RRTM_DATA_DBL RRTM_DATA
ln -sf ${wrfplus_repo_dir}/run/RRTMG_LW_DATA_DBL RRTMG_LW_DATA
ln -sf ${wrfplus_repo_dir}/run/RRTMG_SW_DATA_DBL RRTMG_SW_DATA
ln -sf ${wrfplus_repo_dir}/run/SOILPARM.TBL .  
ln -sf ${wrfplus_repo_dir}/run/VEGPARM.TBL .  
ln -sf ${wrfplus_repo_dir}/run/GENPARM.TBL .  
ln -sf ${wrfplus_repo_dir}/run/LANDUSE.TBL .
# Soft-link namelist and plus.io_config files
ln -sf ${namelist_repo_dir}/namelist.input.adj namelist.input
ln -sf ${util_repo_dir}/plus.io_config plus.io_config
# Soft-link auxhist6 files from wrfplus_trj_dir
ln -sf ${wrfplus_trj_dir}/auxhist6_* .
# Hard-copy wrfout files from wrfplus_trj_dir
cp ${wrfplus_trj_dir}/wrfout_* .
# Hard-copy wrfinput files from init_repo_dir (this may need to change as wrfinput_d01 gets modified)
cp ${init_repo_dir}/wrfinput_d01 .
cp ${init_repo_dir}/wrfbdy_d01 .

cp wrfout_d01_${end_date} fcst.nc
cp wrfout_d01_${end_date} wrfout_d01_${end_date}_control 
ln -sf wrfinput_d01 xref.nc
ln -sf ${util_repo_dir}/adj_forcing_mu.ncl adj_forcing.ncl

ncl adj_forcing.ncl
mv fcst.nc final_sens_d01_${end_date}
ln -sf final_sens_d01_${end_date} wrfout_d01_${end_date}
ln -sf final_sens_d01_${end_date} final_sens_d01
mpirun -np 24 ./wrf.exe

