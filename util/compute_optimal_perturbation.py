#########################################################################
#
# PYTHON 3 PROGRAM
#
# Given an adjoint file (gradient_wrfplus_d<domain>_<date-time>) and a
# target change to a response function (dR), this program computes the
# optimal U, V, T perturbations subject to a kinetic and available
# potential energy cost-function:
#
# f(u,v,t) = 0.5 * [u^2 + v^2 + (cp/T0)*t^2]
#
# As per Ehrendorfer, M., R. M. Errico, and K. D. Raeder, 1999: 
# Singular-vector perturabtion growth in a primative equation model with
# moist physics. Journal of the Atmospheric Sciences, 56, 1627-1648,
# doi: 10.1175/1520-0469(1999)056<1627:SVPGIA>2.0.CO;2
#
# This cost-function does not contain a pressure term, nor a moisture
# term. The pressure term is ommitted since the WRF adjoint is not
# (currently) capable of providing sensitivity of R with respect to
# pressure. There is a sensitivity with respect to water vapor mixing
# ratio, but no moisture term is currently provided here because there
# is a concern about creating supersaturated regions with a moisture
# perturbation completely determined by sensitivity. There may be an
# adjustment in the future to provide a compensating moisture term,
# complimenting the temperature perturbation to keep the relative
# humidity constant, that could utilize the sensitivity to water
# vapor mixing ratio in order to provide a refined correction to
# the impact of the perturbation.
#
#########################################################################
#
# Import necessary modules
#
import numpy as np #..................................................... array module
from netCDF4 import Dataset #............................................ netCDF i/o module
from qoip_dependencies import compute_optimal_perturbation #............. optimal perturbation module
#
#########################################################################
#
# Obtain inputs from user
#
sens_file       = input() #.............................................. full path to gradient_wrfplus_d<domain>_<date-time> file
dR_str          = input() #.............................................. target change to response function (string-format)
nc_outfile_name = input() #.............................................. full path to output netCDF file containing optimal perturbations
# Convert dR_str to dR
dR = float(dR_str)
#
#########################################################################
#
# Extract sensitivity gradients from sens_file
#
sens_hdl = Dataset(sens_file) #.......................................... netCDF file handle for sens_file
sens_u = np.asarray(sens_hdl.variables['A_U']).squeeze() #............... sensitivity to zonal wind [lev,lat,lon]
sens_v = np.asarray(sens_hdl.variables['A_V']).squeeze() #............... sensitivity to merid wind [lev,lat,lon]
sens_t = np.asarray(sens_hdl.variables['A_T']).squeeze() #............... sensitivity to (potential) temperature [lev,lat,lon]
#
#########################################################################
#
# Compute optimal u, v, t perturbations
#
# Define inputs to compute_optimal_perturbation() function
cp = 1004. #............................................................ heat capacity of air at constant pressure (J/kg)
t0 = 270. #............................................................. reference temperature (K)
#
W_u = 1.0 #............................................................. weighting coefficient for zonal wind in cost-function
W_v = 1.0 #............................................................. weighting coefficient for merid wind in cost-function
W_t = cp/t0 #........................................................... weighting coefficient for temperature in cost-function
#
W = [W_u,W_v,W_t] #..................................................... list of weighting coefficients [u,v,t]
S = [sens_u,sens_v,sens_t] #............................................ list of sensitivity gradient grids [u,v,t]
# Define optimal perturbations
opts = compute_optimal_perturbation(dR,W,S) #........................... list of optimal perturbation grids [u,v,t]
# divide S into discrete variables
opt_u = opts[0] #....................................................... optimal zonal wind perturbation [lev,lat,lon]
opt_v = opts[1] #....................................................... optimal merid wind perturbation [lev,lat,lon]
opt_t = opts[2] #....................................................... optimal temperature perturbation [lev,lat,lon]
#
#########################################################################
#
# Write to netCDF file (presumed to not exist, will be created, no
# clobbering but errors if file exists)
#
nc_out = Dataset( #...................................................... Dataset object for output
                  nc_outfile_name  , # Dataset input: Output file name
                  "w"              , # Dataset input: Make file write-able
                  format="NETCDF4" , # Dataset input: Set output format to netCDF4
                )
# Dimensions
lat_vstag  = nc_out.createDimension( #................................... Output dimension
                                     "lat_vstag" , # nc_out.createDimension input: Dimension name 
                                      None         # nc_out.createDimension input: Dimension size limit ("None" == unlimited)
                                   )
lat  = nc_out.createDimension( #......................................... Output dimension
                               "lat" , # nc_out.createDimension input: Dimension name 
                                None   # nc_out.createDimension input: Dimension size limit ("None" == unlimited)
                             )
lon_ustag  = nc_out.createDimension( #................................... Output dimension
                                     "lon_ustag" , # nc_out.createDimension input: Dimension name 
                                      None         # nc_out.createDimension input: Dimension size limit ("None" == unlimited)
                                   )
lon  = nc_out.createDimension( #......................................... Output dimension
                               "lon" , # nc_out.createDimension input: Dimension name 
                               None    # nc_out.createDimension input: Dimension size limit ("None" == unlimited)
                             )
lev = nc_out.createDimension( #.......................................... Output dimension
                               "lev" , # nc_out.createDimension input: Dimension name 
                               None    # nc_out.createDimension input: Dimension size limit ("None" == unlimited)
                             )
param = nc_out.createDimension( #........................................ Output dimension
                               "param" , # nc_out.createDimension input: Dimension name 
                               None      # nc_out.createDimension input: Dimension size limit ("None" == unlimited)
                             )
# Variables
OPT_U_PERT = nc_out.createVariable( #.................................... Output variable
                                    "OPT_U_PERT"  , # nc_out.createVariable input: Variable name 
                                    "f8"          , # nc_out.createVariable input: Variable format 
                                    ( 
                                      "lev"       , # nc_out.createVariable input: Variable dimension
                                      "lat"       , # nc_out.createVariable input: Variable dimension
                                      "lon_ustag"   # nc_out.createVariable input: Variable dimension
                                    )
                                  )
OPT_V_PERT = nc_out.createVariable( #.................................... Output variable
                                    "OPT_V_PERT"  , # nc_out.createVariable input: Variable name 
                                    "f8"          , # nc_out.createVariable input: Variable format 
                                    ( 
                                      "lev"       , # nc_out.createVariable input: Variable dimension
                                      "lat_vstag" , # nc_out.createVariable input: Variable dimension
                                      "lon"         # nc_out.createVariable input: Variable dimension
                                    )
                                  )
OPT_T_PERT = nc_out.createVariable( #.................................... Output variable
                                    "OPT_T_PERT"  , # nc_out.createVariable input: Variable name 
                                    "f8"          , # nc_out.createVariable input: Variable format 
                                    ( 
                                      "lev"       , # nc_out.createVariable input: Variable dimension
                                      "lat"       , # nc_out.createVariable input: Variable dimension
                                      "lon"         # nc_out.createVariable input: Variable dimension
                                    )
                                  )
DEL_R = nc_out.createVariable( #......................................... Output variable
                               "DEL_R"   , # nc_out.createVariable input: Variable name 
                               "f8"      , # nc_out.createVariable input: Variable format 
                               ( 
                                 "param"   # nc_out.createVariable input: Variable dimension
                               )
                             )
# Fill netCDF arrays via slicing
OPT_U_PERT[:,:,:] = opt_u
OPT_V_PERT[:,:,:] = opt_v
OPT_T_PERT[:,:,:] = opt_t
DEL_R[:] = dR
# Close netCDF file
nc_out.close()
#
#########################################################################
#
# END
#
