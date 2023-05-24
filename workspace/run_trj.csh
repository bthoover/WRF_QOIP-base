#!/bin/tcsh

set directory_tree=${1}
set iter_name=${2}

set base_dir=`grep -- "base_dir" ${directory_tree} | awk '{print $2}'`
set wrfplus_repo_dir=`grep -- "wrfplus_repo_dir" ${directory_tree} | awk '{print $2}'`
set namelist_repo_dir=`grep -- "namelist_repo_dir" ${directory_tree} | awk '{print $2}'`
set util_repo_dir=`grep -- "util_repo_dir" ${directory_tree} | awk '{print $2}'`

set curr_dir=`pwd`
set work_dir=${base_dir}/nonlin_trj
set init_repo_dir=${base_dir}/archive/${iter_name}
echo "moving from ${curr_dir} to ${work_dir}..."

mkdir -p ${work_dir}
cd ${work_dir}
ln -sf ${wrfplus_repo_dir}/main/wrf.exe .
ln -sf ${wrfplus_repo_dir}/run/RRTM_DATA_DBL RRTM_DATA
ln -sf ${wrfplus_repo_dir}/run/RRTMG_LW_DATA_DBL RRTMG_LW_DATA
ln -sf ${wrfplus_repo_dir}/run/RRTMG_SW_DATA_DBL RRTMG_SW_DATA
ln -sf ${wrfplus_repo_dir}/run/SOILPARM.TBL .  
ln -sf ${wrfplus_repo_dir}/run/VEGPARM.TBL .  
ln -sf ${wrfplus_repo_dir}/run/GENPARM.TBL .  
ln -sf ${wrfplus_repo_dir}/run/LANDUSE.TBL .

ln -sf ${namelist_repo_dir}/namelist.input.trj namelist.input
ln -sf ${util_repo_dir}/plus.io_config plus.io_config
cp ${init_repo_dir}/wrfinput_d01 .
cp ${init_repo_dir}/wrfbdy_d01 .



mpirun -np 24 ./wrf.exe

echo "running, returning from ${work_dir} to ${curr_dir}..."
cd ${curr_dir}

