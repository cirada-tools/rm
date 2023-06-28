#=============================================================================#
#                          MODEL DEFINITION FILE                              #
#=============================================================================#
import numpy as np
import bilby
from bilby.core.prior import PriorDict, Constraint

#-----------------------------------------------------------------------------#
# Function defining the model.                                                #
#                                                                             #
#  pDict       = Dictionary of parameters, created by parsing inParms, below. #
#  lamSqArr_m2 = Array of lambda-squared values                               #
#  quArr       = Complex array containing the Re and Im spectra.              #
#-----------------------------------------------------------------------------#
def model(pDict, lamSqArr_m2):
    """
    
    Two separate Faraday components with differential Faraday rotation
    Double "Burn slab"
    Averaged within the same telescope beam (i.e., unresolved)
    
    Ref (for individual source component):
    Burn (1966) Eq 18; with N >> (H_r/2H_z^0)^2
    Sokoloff et al. (1998) Eq 3
    O'Sullivan et al. (2012) Eq 9
    Ma et al. (2019a) Eq 12
    
    """
    
    # Calculate the complex fractional q and u spectra
    pArr1 = pDict["fracPol1"] * np.ones_like(lamSqArr_m2)
    pArr2 = pDict["fracPol2"] * np.ones_like(lamSqArr_m2)

    quArr1 = pArr1 * np.exp( 2j * (np.radians(pDict["psi01_deg"]) +
                                   (0.5*pDict["deltaRM1_radm2"] +
                                    pDict["RM1_radm2"]) * lamSqArr_m2))
    quArr2 = pArr2 * np.exp( 2j * (np.radians(pDict["psi02_deg"]) +
                                   (0.5*pDict["deltaRM2_radm2"] +
                                    pDict["RM2_radm2"]) * lamSqArr_m2))
    quArr = (quArr1 * np.sin(pDict["deltaRM1_radm2"] * lamSqArr_m2) / 
             (pDict["deltaRM1_radm2"] * lamSqArr_m2) +
             quArr2 * np.sin(pDict["deltaRM2_radm2"] * lamSqArr_m2) / 
             (pDict["deltaRM2_radm2"] * lamSqArr_m2))
    
    return quArr


#-----------------------------------------------------------------------------#
# Priors for the above model.                                                 #
# See https://lscsoft.docs.ligo.org/bilby/prior.html for details.             #
#                                                                             #
#-----------------------------------------------------------------------------#
def converter(parameters):
    """
    Function to convert between sampled parameters and constraint parameter.

    Parameters
    ----------
    parameters: dict
        Dictionary containing sampled parameter values, 'RM1_radm2', 'RM1_radm2',
        'fracPol1', 'fracPol2'

    Returns
    -------
    dict: Dictionary with constraint parameter 'delta_RM1_RM2_radm2' and 'sum_p1_p2' added.
    """
    converted_parameters = parameters.copy()
    converted_parameters['delta_RM1_RM2_radm2'] = parameters['RM1_radm2'] - parameters['RM2_radm2']
    converted_parameters['sum_p1_p2'] = parameters['fracPol1'] + parameters['fracPol2']
    return converted_parameters

priors = PriorDict(conversion_function=converter)

priors['fracPol1'] = bilby.prior.Uniform(
    minimum=0.0,
    maximum=1.0,
    name='fracPol1',
    latex_label='$p_1$',
)
priors['fracPol2'] = bilby.prior.Uniform(
    minimum=0.0,
    maximum=1.0,
    name='fracPol2',
    latex_label='$p_2$',
)

priors['psi01_deg'] = bilby.prior.Uniform(
    minimum=0,
    maximum=180.0,
    name="psi01_deg",
    latex_label="$\psi_{0,1}$ (deg)",
    boundary="periodic",
)
priors['psi02_deg'] = bilby.prior.Uniform(
    minimum=0,
    maximum=180.0,
    name="psi02_deg",
    latex_label="$\psi_{0,2}$ (deg)",
    boundary="periodic",
)

priors['RM1_radm2'] = bilby.prior.Uniform(
    minimum=-1100.0,
    maximum=1100.0,
    name="RM1_radm2",
    latex_label="$\phi_1$ (rad m$^{-2}$)",
)
priors['RM2_radm2'] = bilby.prior.Uniform(
    minimum=-1100.0,
    maximum=1100.0,
    name="RM2_radm2",
    latex_label="$\phi_2$ (rad m$^{-2}$)",
)
priors['deltaRM1_radm2'] = bilby.prior.Uniform(
        minimum=0.0,
        maximum=100.0,
        name="deltaRM1_radm2",
        latex_label="$\Delta{RM,1}$ (rad m$^{-2}$))",
)
priors['deltaRM2_radm2'] = bilby.prior.Uniform(
        minimum=0.0,
        maximum=100.0,
        name="deltaRM2_radm2",
        latex_label="$\Delta{RM,2}$ (rad m$^{-2}$)",
)
priors['delta_RM1_RM2_radm2'] = Constraint(
    minimum=0,
    maximum=2200.0,
    name="delta_RM1_RM2_radm2",
    latex_label="$\Delta\phi_{1,2}$ (rad m$^{-2}$)",
)
priors['sum_p1_p2'] = Constraint(
    minimum=0.0,
    maximum=1,
    name="sum_p1_p2",
    latex_label="$p_1+p_2$)",
)
