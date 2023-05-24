######################################################################################################
#
# silentremove: function to remove files if they exist, handle exceptions
#
#
# INPUTS:
#
#    filename ................................................................ filename to test/remove
#
# OUTPUTS:
#
#    None
#
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred
#
######################################################################################################
#
def compute_optimal_perturbation(dR,W,S):
    #####################################################################
    #
    # DEFINITION:
    #
    # Given a target response function value (dR) and lists of weighting
    # coefficients (W) and sensitivity gradients (S), this function
    # produces optimal perturbations to each variable in the list on the
    # grid the sensitivities are defined on. The optimal perturbation is
    # designed to change the response function by dR while minimizing a
    # cost-function defined by the sum of squared differences in each
    # variable weighted by their respective weighting coefficients.
    #
    # We are using the Lagrange multiplier method to define optimal
    # perturbations, as described in:
    #
    # Errico, R. M., 1997: What is an adjoint model? Bulletin of the
    # American Meteorological Society, 78, 2577-2592.
    #
    # As a sanity check, the inner-product of the optimal perturbation
    # and the sensitivity gradient, summed across all variables, should
    # exactly equal the value of dR.
    #
    # INPUTS:
    #
    # dR ............................. target change in response function
    # W ................ list of weighting coefficients for each variable
    # S ....... list of gridded arrays of sensitivitity for each variable
    #
    # OUTPUTS:
    #
    # O ....... list of gridded arrays of optimal perturbations for each
    #           variable
    #
    # NOTES:
    #
    # Uses numPy
    #
    #####################################################################
    #
    # Import necessary modules
    #
    import numpy as np #................................................. array module
    #
    #####################################################################
    #
    # Initialize O, LAMDA
    #
    O = [] #............................................................. list of optimal perturbation arrays (initialized to empty)
    LAMDA = 0. #......................................................... Lagrange multiplier coefficient (initialized to zero)
    #
    # CHECK: If W and S have different lengths, return with error
    #
    nW = len(W) #........................................................ number of weighting coefficients
    nS = len(S) #........................................................ number of sensitivity gradients
    if (nW != nS):
        print('ERROR: Number of weights does not match number of ' +
              'variables')
        return O
    #
    #####################################################################
    #
    # First loop through variables: Define LAMDA
    #
    for i in range(nW):
        # Extract weighting coefficient and sensitivity gradient
        w0 = W[i] #...................................................... TEMPORARY VARIABLE: weighting coefficient of current variable
        s0 = S[i] #...................................................... TEMPORARY VARIABLE: sensitivity gradient of R with respect to current variable
        # Compute contribution to LAMDA
        LAMDA = LAMDA + np.sum((w0**-1.) * s0**2.)
    # Finalize LAMDA
    LAMDA = dR * LAMDA**-1.
    #
    #####################################################################
    #
    # Second loop through variables: Define O
    #
    for i in range(nW):
        # Extract weighting coefficient and sensitivity gradient
        w0 = W[i] #...................................................... TEMPORARY VARIABLE: weighting coefficient of current variable
        s0 = S[i] #...................................................... TEMPORARY VARIABLE: sensitivity gradient of R with respect to current variable
        # Compute contribution to O
        O.append((LAMDA/w0)*s0)
    # Return O
    return O
    #
    #####################################################################
    # 
    # END
    #

