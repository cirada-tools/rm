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
    
    Three separate Faraday thin sources
    Averaged within the same telescope beam (i.e., unresolved)
    
    Ref (for individual source component):
    Sokoloff et al. (1998) Eq 2
    O'Sullivan et al. (2012) Eq 8
    Ma et al. (2019a) Eq 10
    
    """
    
    # Calculate the complex fractional q and u spectra
    pArr1 = pDict["fracPol1"] * np.ones_like(lamSqArr_m2)
    pArr2 = pDict["fracPol2"] * np.ones_like(lamSqArr_m2)
    pArr3 = pDict["fracPol3"] * np.ones_like(lamSqArr_m2)
    quArr1 = pArr1 * np.exp( 2j * (np.radians(pDict["psi01_deg"]) +
                                   pDict["RM1_radm2"] * lamSqArr_m2))
    quArr2 = pArr2 * np.exp( 2j * (np.radians(pDict["psi02_deg"]) +
                                   pDict["RM2_radm2"] * lamSqArr_m2))
    quArr3 = pArr3 * np.exp( 2j * (np.radians(pDict["psi03_deg"]) +
                                   pDict["RM3_radm2"] * lamSqArr_m2))
    quArr = (quArr1 + quArr2 + quArr3)
    
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
        Dictionary containing sampled parameter values, 'RM1_radm2', 'RM2_radm2',
        'RM3_radm2', 'fracPol1', 'fracPol2', 'fracPol3'

    Returns
    -------
    dict: Dictionary with constraint parameter 'delta_RM1_RM2_radm2' and 'sum_p1_p2_p3' added.
    """
    converted_parameters = parameters.copy()
    converted_parameters['delta_RM1_RM2_radm2'] = parameters['RM1_radm2'] - parameters['RM2_radm2']
    converted_parameters['delta_RM2_RM3_radm2'] = parameters['RM2_radm2'] - parameters['RM3_radm2']
    converted_parameters['sum_p1_p2_p3'] = parameters['fracPol1'] + parameters['fracPol2'] + parameters['fracPol3']
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
priors['fracPol3'] = bilby.prior.Uniform(
    minimum=0.0,
    maximum=1.0,
    name='fracPol3',
    latex_label='$p_3$',
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
priors['psi03_deg'] = bilby.prior.Uniform(
    minimum=0,
    maximum=180.0,
    name="psi03_deg",
    latex_label="$\psi_{0,3}$ (deg)",
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
priors['RM3_radm2'] = bilby.prior.Uniform(
    minimum=-1100.0,
    maximum=1100.0,
    name="RM3_radm2",
    latex_label="$\phi_3$ (rad m$^{-2}$)",
)
priors['delta_RM1_RM2_radm2'] = Constraint(
    minimum=0,
    maximum=2200.0,
    name="delta_RM1_RM2_radm2",
    latex_label="$\Delta\phi_{1,2}$ (rad m$^{-2}$)",
)
priors['delta_RM2_RM3_radm2'] = Constraint(
    minimum=0,
    maximum=2200.0,
    name="delta_RM2_RM3_radm2",
    latex_label="$\Delta\phi_{1,2}$ (rad m$^{-2}$)",
)
priors['sum_p1_p2_p3'] = Constraint(
    minimum=0.0,
    maximum=1,
    name="sum_p1_p2_p3",
    latex_label="$p_1+p_2+p_3$)",
)