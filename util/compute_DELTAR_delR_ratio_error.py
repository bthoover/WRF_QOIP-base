#########################################################################
#
# PYTHON 3 PROGRAM
#
# Given six files:
#
# 1. Old (unperturbed, on this iteration) wrfinput file
# 2. New (perturbed, on this iteration) wrfinput file
# 3. Adjoint-derived sensitivity (t=t0) file
# 4. Adjoint-defined sensitivity (t=tf) file
# 5. Unperturbed nonlinear WRF forecast (t=tf) file
# 6. Perturbed nonlinear WRF forecast (t=tf) file
#
# This program will compute the error in the adjoint-based estimate of
# the impact of the initial perturbation on the response function (R) at
# the forecast time t=tf. This is defined by computing two quantities:
#
# del_R: Adjoint-estimate of impact = dot(xp(t=t0),dR/dx(t=t0))
# DELTA_R: Nonlinear perturbation = dot(x2(t=tf)-x1(t=tf),dR/dx(t=tf))
#
# The error is defined as the absolute value of the deviation of the ratio
# DELTA_R/del_R from 1.0, or:
#
# Error = abs((DELTA_R/del_R)-1.0)
#
# We can define some threshold for an allowable error as a percentage of
# over- or under-estimating the nonlinear impact of the perturbation, such
# as a threshold of 0.5, indicating that the perturbation in the nonlinear
# model cannot exceed 50% greater or smaller impact than what the adjoint
# estimated the impact would be.
#
# NOTE: del_R only needs to be computed over all components of the state
#       vector that are contained in the optimal perturbation to the
#       initial state (e.g. only over [u,v,t] for an optimal perturbation
#       formed from a kinetic+avilable potential energy norm, or over
#       [u,v,t,q] for an optimal perturbation that also contains a
#       moisture component). However, DELTA_R is not so easily
#       constrained, since the response function may be defined by
#       components of the state vector that aren't part of the optimal
#       perturbation. For example: a mu-based response function that
#       defines the intensity of a cyclone, which is not part of a
#       [u,v,t,(q)]-space optimal perturbation. For this reason, the
#       DELTA_R terms are carried out over more components of the state
#       vector, so there are more wrf-fcst and sensitivity components
#       extracted from the files than only those used for del_R. You
#       may need to add additional terms if you define new response
#       functions for which the appropriate DELTA_R components are not
#       already specified.
#
#       For some state vector component S, you need to add the following:
#       
#       1. Under "Extract fields from files", you need to extract the
#          sensitivity gradient with respect to S at t=tf, the WRF
#          (unperturbed) forecast of S at t=tf, and the WRF (perturbed)
#          forecast of S at t=tf.
#       2. Under "Compute perturbations to u, v, t fields at t=t0 and 
#          t=tf", you need to compute an additional perturbation term,
#          Sfp, as the perturbation (perturbed-unperturbed) S at t=tf.
#       3. Under "Compute del_R and DELTA_R values", you need to compute
#          an additional term DELTA_RS as:
#
#          [nz],ny,nx = np.shape(Sfp)
#          DELTA_RS = np.dot(np.reshape(Sfp,[nz*]ny*nx),np.reshape(rS,[nz*]ny*nx))
#
#          Where rS is the sensitivity gradient with respect to S at t=tf
#          and [nz] is the vertical dimension, which may or may not exist
#          for S depending on if S is a 3-D or 2-D variable. For example,
#          for S=mu, a 2-D variable, nz would be ommitted in the above
#          lines of code and the dot-product is carried out only over
#          flattened arrays of size ny*nx.
#       4. Under "Compute del_R and DELTA_R values", you have to add the
#          DELTA_RS term to DELTA_R: DELTA_R = DELTA_R + DELTA_RS 
#
#
# 05/03/21: Adding compensating moisture term to delR. For clarity, the
#           text output will now contain both the prescribed delR value
#           specified by the user in the top-level run script, as well
#           as the final delR value once the compensating moisture term
#           has been included. Errors are calculated based on the final
#           delR value.
#
#########################################################################
#
# Import required modules
#
import numpy as np #..................................................... array module
from netCDF4 import Dataset #............................................ netCDF i/o module
#
#########################################################################
#
# Obtain inputs from user
#
old_wrfinput_file = input() #............................................ old (unperturbed, on this iteration) wrfinput file
new_wrfinput_file = input() #............................................ new (perturbed, on this iteration) wrfinput file
adj_sens_file = input() #................................................ adjoint-derived sensitivity (t=t0) file
adj_init_file = input() #................................................ adjoint-defined sensitivity (t=tf) file
uptd_wrffcst_file = input() #............................................ unperturbed nonlinear WRF forecast (t=tf) file
ptd_wrffcst_file = input() #............................................. perturbed nonlinear WRF forecast (t=tf) file
R_error_threshold_str = input() #........................................ threshold of R_error for accept/reject (string)
delR_orig_str = input() #................................................ original (user specified at top-level script) delR value (string)
pert_mag_str = input() #................................................. perturbation magnitude for this inner-loop (string)
# Define R_error_threshold, delR_orig, pert_mag as float
R_error_threshold = float(R_error_threshold_str) #....................... threshold of R_error for accept/reject (float)
delR_orig = float(delR_orig_str) #....................................... original (user specified at top-level script) delR value (float)
pert_mag = float(pert_mag_str) #......................................... perturbation magnitude for this inner-loop (float)
#
delR_orig = delR_orig * pert_mag
#
#########################################################################
#
# Extract fields from files
#
old_wrfinput_hdl = Dataset(old_wrfinput_file) #.......................... old_wrfinput_file handle
u0 = np.asarray(old_wrfinput_hdl.variables['U']).squeeze() #............. old zonal flow field (t=t0)
v0 = np.asarray(old_wrfinput_hdl.variables['V']).squeeze() #............. old merid flow field (t=t0)
t0 = np.asarray(old_wrfinput_hdl.variables['T']).squeeze() #............. old temperature field (t=t0)
q0 = np.asarray(old_wrfinput_hdl.variables['QVAPOR']).squeeze() #........ old water vapor mixing ratio field (t=t0)
new_wrfinput_hdl = Dataset(new_wrfinput_file) #.......................... new_wrfinput_file handle
u1 = np.asarray(new_wrfinput_hdl.variables['U']).squeeze() #............. new zonal flow field (t=t0)
v1 = np.asarray(new_wrfinput_hdl.variables['V']).squeeze() #............. new merid flow field (t=t0)
t1 = np.asarray(new_wrfinput_hdl.variables['T']).squeeze() #............. new temperature field (t=t0)
q1 = np.asarray(new_wrfinput_hdl.variables['QVAPOR']).squeeze() #........ new water vapor mixing ratio field (t=t0)
adj_sens_hdl = Dataset(adj_sens_file) #.................................. adj_sens_file handle
au = np.asarray(adj_sens_hdl.variables['A_U']).squeeze() #............... adjoint-derived sensitivity to zonal flow field (t=t0)
av = np.asarray(adj_sens_hdl.variables['A_V']).squeeze() #............... adjoint-derived sensitivity to merid flow field (t=t0)
at = np.asarray(adj_sens_hdl.variables['A_T']).squeeze() #............... adjoint-derived sensitivity to temperature field (t=t0)
aq = np.asarray(adj_sens_hdl.variables['A_QVAPOR']).squeeze() #.......... adjoint-derived sensitivity to water vapor mixing ratio field (t=t0)
adj_init_hdl = Dataset(adj_init_file) #.................................. adj_init_file handle
ru = np.asarray(adj_init_hdl.variables['G_U']).squeeze() #............... adjoint-defined sensitivity to zonal flow field (t=tf)
rv = np.asarray(adj_init_hdl.variables['G_V']).squeeze() #............... adjoint-defined sensitivity to merid flow field (t=tf)
rt = np.asarray(adj_init_hdl.variables['G_T']).squeeze() #............... adjoint-defined sensitivity to temperature field (t=tf)
rm = np.asarray(adj_init_hdl.variables['G_MU']).squeeze() #.............. adjoint-defined sensitivity to mu (dry air mass) field (t=tf)
uptd_wrffcst_hdl = Dataset(uptd_wrffcst_file) #.......................... uptd_wrffcst_file handle
uf0 = np.asarray(uptd_wrffcst_hdl.variables['U']).squeeze() #............ unperturbed nonlinear WRF forecast zonal flow field (t=tf)
vf0 = np.asarray(uptd_wrffcst_hdl.variables['V']).squeeze() #............ unperturbed nonlinear WRF forecast merid flow field (t=tf)
tf0 = np.asarray(uptd_wrffcst_hdl.variables['T']).squeeze() #............ unperturbed nonlinear WRF forecast temperature field (t=tf)
mf0 = np.asarray(uptd_wrffcst_hdl.variables['MU']).squeeze() #........... unperturbed nonlinear WRF forecast mu (dry air mass) field (t=tf)
ptd_wrffcst_hdl = Dataset(ptd_wrffcst_file) #............................ ptd_wrffcst_file handle
uf1 = np.asarray(ptd_wrffcst_hdl.variables['U']).squeeze() #............. perturbed nonlinear WRF forecast zonal flow field (t=tf)
vf1 = np.asarray(ptd_wrffcst_hdl.variables['V']).squeeze() #............. perturbed nonlinear WRF forecast merid flow field (t=tf)
tf1 = np.asarray(ptd_wrffcst_hdl.variables['T']).squeeze() #............. perturbed nonlinear WRF forecast temperature field (t=tf)
mf1 = np.asarray(ptd_wrffcst_hdl.variables['MU']).squeeze() #............ perturbed nonlinear WRF forecast mu (dry air mass) field (t=tf)
#
old_wrfinput_hdl.close()
new_wrfinput_hdl.close()
adj_sens_hdl.close()
adj_init_hdl.close()
uptd_wrffcst_hdl.close()
ptd_wrffcst_hdl.close()
#
#########################################################################
#
# Compute perturbations to u, v, t, [q] fields at t=t0 and t=tf (include 
# mu perturbation at t=tf for response functions based on mu)
#
up = u1-u0 #............................................................. zonal flow perturbation at t=t0
vp = v1-v0 #............................................................. merid flow perturbation at t=t0
tp = t1-t0 #............................................................. temperature perturbation at t=t0
qp = q1-q0 #............................................................. water vapor mixing ratio perturbation at t=t0
#
ufp = uf1-uf0 #.......................................................... zonal flow perturbation at t=tf
vfp = vf1-vf0 #.......................................................... merid flow perturbation at t=tf
tfp = tf1-tf0 #.......................................................... temperature perturbation at t=tf
mfp = mf1-mf0 #.......................................................... mu (dry air mass) perturbation at t=tf
#
#########################################################################
#
# Compute del_R and DELTA_R values
#
nz,ny,nx = np.shape(up) #................................................ dimensions of zonal flow field
del_Ru = np.dot(np.reshape(up,nz*ny*nx),np.reshape(au,nz*ny*nx)) #....... del_R for zonal flow component
DELTA_Ru = np.dot(np.reshape(ufp,nz*ny*nx),np.reshape(ru,nz*ny*nx)) #.... DELTA_R for zonal flow component
#
nz,ny,nx = np.shape(vp) #................................................ dimensions of merid flow field
del_Rv = np.dot(np.reshape(vp,nz*ny*nx),np.reshape(av,nz*ny*nx)) #....... del_R for merid flow component
DELTA_Rv = np.dot(np.reshape(vfp,nz*ny*nx),np.reshape(rv,nz*ny*nx)) #.... DELTA_R for merid flow component
#
nz,ny,nx = np.shape(tp) #................................................ dimensions of temperature field
del_Rt = np.dot(np.reshape(tp,nz*ny*nx),np.reshape(at,nz*ny*nx)) #....... del_R for temperature component
DELTA_Rt = np.dot(np.reshape(tfp,nz*ny*nx),np.reshape(rt,nz*ny*nx)) #.... DELTA_R for temperature component
#
nz,ny,nx = np.shape(qp) #................................................ dimensions of temperature field
del_Rq = np.dot(np.reshape(qp,nz*ny*nx),np.reshape(aq,nz*ny*nx)) #....... del_R for water vapor mixing ratio component
#
del_R = del_Ru + del_Rv + del_Rt + del_Rq #.............................. del_R across all (u,v,t,[q]) components
# Include mu term in DELTA_R (for response functions based on mu)
ny,nx = np.shape(mfp)
DELTA_Rm = np.dot(np.reshape(mfp,ny*nx),np.reshape(rm,ny*nx)) #.......... DELTA_R for mu (dry air mass) component
#
DELTA_R = DELTA_Ru + DELTA_Rv + DELTA_Rt + DELTA_Rm #.................... DELTA_R across all (u,v,t,mu) components
#########################################################################
#
# Compute error
#
R_error = abs((DELTA_R/del_R) - 1.0) #.................................... error in estimating DELTA_R from del_R
#
# Evaluate accept (1) or reject (-1) criteria based on R_error_threshold
# NOTE: If the perturbation was reduced to zero-magnitude in the inner-
#       loop, R_error will be np.nan instead of zero, since there is
#       a zero in the denominator. So this case is added to the accept-
#       criteria.
#
if ( (R_error <= R_error_threshold) | (np.isnan(R_error)) ):
    acc_rej = 1
else:
    acc_rej = -1
#
# Report to file
#
outf = open('R_error.txt','w')
outf.write(
            "{:.2e}".format(DELTA_R) + " " +  # change in R between unperturbed and perturbed nonlinear forecasts
            "{:.2e}".format(del_R)   + " " +  # adjoint-derived estimated change in R (final, includes effect of compensating moisture)
            "{:.2e}".format(delR_orig) + " " +# adjoint-derived estimated change in R (user-specified, does not include effect of compensating moisture)
            "{:.3f}".format(R_error) + " " +  # fractional percent-error in adjoint-derived estimate (pos. def.)
            "{:d}".format(acc_rej)            # 1 == meets criteria for passing, -1 == does not meet criteria
          )
outf.close()
#
#########################################################################
#
# END
#
