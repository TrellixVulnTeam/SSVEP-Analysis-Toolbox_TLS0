"""
TRCA based recognition methods
"""

from typing import Union, Optional, Dict, List, Tuple, Callable
from numpy import ndarray
from joblib import Parallel, delayed
from functools import partial
from copy import deepcopy

import numpy as np
import numpy.matlib as npmat
import scipy.linalg as slin
import scipy.stats as stats
import warnings

from .basemodel import BaseModel
from .utils import gen_template, sort, canoncorr, separate_trainSig, qr_list, blkrep

def _trcaR_cal_template_U(X_single_stimulus : ndarray,
                          I : ndarray,
                          n_component : int):
    """
    Calculate templates and trials' spatial filters in TRCA-R
    """
    trial_num, filterbank_num, channel_num, signal_len = X_single_stimulus.shape
    # prepare center matrix
    # I = np.eye(signal_len)
    LL = npmat.repmat(I, trial_num, trial_num) - blkrep(I, trial_num)
    # calculate spatial filters of each filterbank
    U_trial = []
    for filterbank_idx in range(filterbank_num):
        X_single_stimulus_single_filterbank = X_single_stimulus[:,filterbank_idx,:,:]
        template = []
        for trial_idx in range(trial_num):
            template.append(X_single_stimulus_single_filterbank[trial_idx,:,:])
        template = np.concatenate(template, axis = 1)
        # calculate spatial filters of trials
        Sb = template @ LL @ template.T
        Sw = template @ template.T
        eig_d1, eig_v1 = slin.eig(Sb, Sw) #eig(Sw\Sb)
        sort_idx = np.argsort(eig_d1)[::-1]
        eig_vec = eig_v1[:,sort_idx]
        if np.iscomplex(eig_vec).any():
            eig_vec = np.real(eig_vec[:channel_num,:n_component])
        else:
            eig_vec = eig_vec[:channel_num,:n_component]
        U_trial.append(np.expand_dims(eig_vec, axis = 0))
    U_trial = np.concatenate(U_trial, axis = 0)
    return U_trial

def _trca_U_1(X: list) -> Tuple[ndarray, ndarray]:
    """
    Calculcate first step of trca

    Parameters
    ------------
    X : list
        List of EEG data
        Length: (trial_num,)
        Shape of EEG: (channel_num, signal_len)

    Returns
    -----------
    trca_X1 : ndarray
    trca_X2 : ndarray
    """
    trca_X1 = np.zeros(X[0].shape)
    trca_X2 = []
    for X0 in X:
        trca_X1 = trca_X1 + X0
        trca_X2.append(X0.T)
    trca_X2 = np.concatenate(trca_X2, axis = 0)
    return trca_X1, trca_X2

def _trca_U_2(trca_X1: ndarray, 
              trca_X2: ndarray) -> ndarray:
    """
    Calculcate second step of trca

    Parameters
    ------------
    trca_X1 : ndarray
    trca_X2 : ndarray

    Returns
    -----------
    U : ndarray
        Spatial filter
        shape: (channel_num * n_component)
    """
    S=trca_X1 @ trca_X1.T - trca_X2.T @ trca_X2
    Q=trca_X2.T @ trca_X2
    eig_d1, eig_v1 = slin.eig(S, Q)
    sort_idx = np.argsort(eig_d1)[::-1]
    eig_vec=eig_v1[:,sort_idx]
    return eig_vec

def _trca_U(X: list) -> ndarray:
    """
    Calculate spatial filters of trca

    Parameters
    ------------
    X : list
        List of EEG data
        Length: (trial_num,)
        Shape of EEG: (channel_num, signal_len)

    Returns
    -----------
    U : ndarray
        Spatial filter
        shape: (channel_num * n_component)
    """
    # trca_X1 = np.zeros(X[0].shape)
    # trca_X2 = []
    # for X0 in X:
    #     trca_X1 = trca_X1 + X0
    #     trca_X2.append(X0.T)
    # trca_X2 = np.concatenate(trca_X2, axis = 0)
    trca_X1, trca_X2 = _trca_U_1(X)
    # S=trca_X1 @ trca_X1.T - trca_X2.T @ trca_X2
    # Q=trca_X2.T @ trca_X2
    # eig_d1, eig_v1 = slin.eig(S, Q)
    # sort_idx = np.argsort(eig_d1)[::-1]
    # eig_vec=eig_v1[:,sort_idx]
    eig_vec = _trca_U_2(trca_X1, trca_X2)

    return eig_vec

def _r_cca_canoncorr_withUV(X: ndarray,
                            Y: List[ndarray],
                            U: ndarray,
                            V: ndarray) -> ndarray:
    """
    Calculate correlation of CCA based on canoncorr for single trial data using existing U and V

    Parameters
    ----------
    X : ndarray
        Single trial EEG data
        EEG shape: (filterbank_num, channel_num, signal_len)
    Y : List[ndarray]
        List of reference signals
    U : ndarray
        Spatial filter
        shape: (filterbank_num * stimulus_num * channel_num * n_component)
    V : ndarray
        Weights of harmonics
        shape: (filterbank_num * stimulus_num * harmonic_num * n_component)

    Returns
    -------
    R : ndarray
        Correlation
        shape: (filterbank_num * stimulus_num)
    """
    filterbank_num, channel_num, signal_len = X.shape
    if len(Y[0].shape)==2:
        harmonic_num = Y[0].shape[0]
    elif len(Y[0].shape)==3:
        harmonic_num = Y[0].shape[1]
    else:
        raise ValueError('Unknown data type')
    stimulus_num = len(Y)
    
    R = np.zeros((filterbank_num, stimulus_num))
    
    for k in range(filterbank_num):
        tmp = X[k,:,:]
        for i in range(stimulus_num):
            if len(Y[i].shape)==2:
                Y_tmp = Y[i]
            elif len(Y[i].shape)==3:
                Y_tmp = Y[i][k,:,:]
            else:
                raise ValueError('Unknown data type')
            
            A_r = U[k,i,:,:]
            B_r = V[k,i,:,:]
            
            a = A_r.T @ tmp
            b = B_r.T @ Y_tmp
            a = np.reshape(a, (-1))
            b = np.reshape(b, (-1))
            
            # r2 = stats.pearsonr(a, b)[0]
            r = stats.pearsonr(a, b)[0]
            R[k,i] = r
    return R


class TRCA(BaseModel):
    """
    TRCA method
    """
    def __init__(self,
                 n_component: int = 1,
                 n_jobs: Optional[int] = None,
                 weights_filterbank: Optional[List[float]] = None):
        super().__init__(ID = 'TRCA',
                         n_component = n_component,
                         n_jobs = n_jobs,
                         weights_filterbank = weights_filterbank)
        self.model['U'] = None # Spatial filter of EEG

    def __copy__(self):
        copy_model = TRCA(n_component = self.n_component,
                          n_jobs = self.n_jobs,
                          weights_filterbank = self.model['weights_filterbank'])
        copy_model.model = deepcopy(self.model)
        return copy_model

    def fit(self,
            freqs: Optional[List[float]] = None,
            X: Optional[List[ndarray]] = None,
            Y: Optional[List[int]] = None,
            ref_sig: Optional[List[ndarray]] = None):
        if Y is None:
            raise ValueError('TRCA requires training label')
        if X is None:
            raise ValueError('TRCA requires training data')
           
        template_sig = gen_template(X, Y) # List of shape: (stimulus_num,); 
                                          # Template shape: (filterbank_num, channel_num, signal_len)
        self.model['template_sig'] = template_sig

        # spatial filters
        #   U: (filterbank_num * stimulus_num * channel_num * n_component)
        #   X: (filterbank_num, channel_num, signal_len)
        filterbank_num = template_sig[0].shape[0]
        stimulus_num = len(template_sig)
        channel_num = template_sig[0].shape[1]
        n_component = self.n_component
        U_trca = np.zeros((filterbank_num, stimulus_num, channel_num, n_component))
        possible_class = list(set(Y))
        possible_class.sort(reverse = False)
        for filterbank_idx in range(filterbank_num):
            X_train = [[X[i][filterbank_idx,:,:] for i in np.where(np.array(Y) == class_val)[0]] for class_val in possible_class]
            U = Parallel(n_jobs = self.n_jobs)(delayed(_trca_U)(X = X_single_class) for X_single_class in X_train)
            for stim_idx, u in enumerate(U):
                U_trca[filterbank_idx, stim_idx, :, :] = u[:channel_num,:n_component]
        self.model['U'] = U_trca

    def predict(self,
            X: List[ndarray]) -> List[int]:
        weights_filterbank = self.model['weights_filterbank']
        if weights_filterbank is None:
            weights_filterbank = [1 for _ in range(X[0].shape[0])]
        if type(weights_filterbank) is list:
            weights_filterbank = np.expand_dims(np.array(weights_filterbank),1).T
        else:
            if len(weights_filterbank.shape) != 2:
                raise ValueError("'weights_filterbank' has wrong shape")
            if weights_filterbank.shape[0] != 1:
                weights_filterbank = weights_filterbank.T
        if weights_filterbank.shape[0] != 1:
            raise ValueError("'weights_filterbank' has wrong shape")

        template_sig = self.model['template_sig']
        U = self.model['U'] 

        r = Parallel(n_jobs=self.n_jobs)(delayed(partial(_r_cca_canoncorr_withUV, Y=template_sig, U=U, V=U))(X=a) for a in X)

        Y_pred = [int( np.argmax( weights_filterbank @ r_tmp)) for r_tmp in r]
        
        return Y_pred 

class TRCAwithR(BaseModel):
    """
    TRCA method with reference signals
    """
    def __init__(self,
                 n_component: int = 1,
                 n_jobs: Optional[int] = None,
                 weights_filterbank: Optional[List[float]] = None):
        super().__init__(ID = 'TRCA-R',
                         n_component = n_component,
                         n_jobs = n_jobs,
                         weights_filterbank = weights_filterbank)
        self.model['U'] = None # Spatial filter of EEG

    def __copy__(self):
        copy_model = TRCAwithR(n_component = self.n_component,
                                n_jobs = self.n_jobs,
                                weights_filterbank = self.model['weights_filterbank'])
        copy_model.model = deepcopy(self.model)
        return copy_model

    def fit(self,
            freqs: Optional[List[float]] = None,
            X: Optional[List[ndarray]] = None,
            Y: Optional[List[int]] = None,
            ref_sig: Optional[List[ndarray]] = None):
        if Y is None:
            raise ValueError('TRCA with reference signals requires training label')
        if X is None:
            raise ValueError('TRCA with reference signals training data')
        if ref_sig is None:
            raise ValueError('TRCA with reference signals requires sine-cosine-based reference signal')

        template_sig = gen_template(X, Y) # List of shape: (stimulus_num,); 
                                          # Template shape: (filterbank_num, channel_num, signal_len)
        self.model['template_sig'] = template_sig

        separated_trainSig = separate_trainSig(X, Y)
        ref_sig_Q, ref_sig_R, ref_sig_P = qr_list(ref_sig)

        U_all_stimuli = Parallel(n_jobs=self.n_jobs)(delayed(partial(_trcaR_cal_template_U, n_component = self.n_component))(X_single_stimulus = a, I = Q @ Q.T) for a, Q in zip(separated_trainSig, ref_sig_Q))
        U_trca = [np.expand_dims(u, axis=1) for u in U_all_stimuli]
        U_trca = np.concatenate(U_trca, axis = 1)
        self.model['U'] = U_trca

    def predict(self,
            X: List[ndarray]) -> List[int]:
        weights_filterbank = self.model['weights_filterbank']
        if weights_filterbank is None:
            weights_filterbank = [1 for _ in range(X[0].shape[0])]
        if type(weights_filterbank) is list:
            weights_filterbank = np.expand_dims(np.array(weights_filterbank),1).T
        else:
            if len(weights_filterbank.shape) != 2:
                raise ValueError("'weights_filterbank' has wrong shape")
            if weights_filterbank.shape[0] != 1:
                weights_filterbank = weights_filterbank.T
        if weights_filterbank.shape[0] != 1:
            raise ValueError("'weights_filterbank' has wrong shape")

        template_sig = self.model['template_sig']
        U = self.model['U'] 

        r = Parallel(n_jobs=self.n_jobs)(delayed(partial(_r_cca_canoncorr_withUV, Y=template_sig, U=U, V=U))(X=a) for a in X)

        Y_pred = [int( np.argmax( weights_filterbank @ r_tmp)) for r_tmp in r]
        
        return Y_pred 

class ETRCA(BaseModel):
    """
    eTRCA method
    """
    def __init__(self,
                 n_component: Optional[int] = None,
                 n_jobs: Optional[int] = None,
                 weights_filterbank: Optional[List[float]] = None):
        if n_component is not None:
            warnings.warn("Although 'n_component' is provided, it will not considered in eTRCA")
        n_component = 1
        super().__init__(ID = 'eTRCA',
                         n_component = n_component,
                         n_jobs = n_jobs,
                         weights_filterbank = weights_filterbank)
        self.model['U'] = None # Spatial filter of EEG

    def __copy__(self):
        copy_model = ETRCA(n_component = None,
                          n_jobs = self.n_jobs,
                          weights_filterbank = self.model['weights_filterbank'])
        copy_model.model = deepcopy(self.model)
        return copy_model

    def fit(self,
            freqs: Optional[List[float]] = None,
            X: Optional[List[ndarray]] = None,
            Y: Optional[List[int]] = None,
            ref_sig: Optional[List[ndarray]] = None):
        if Y is None:
            raise ValueError('eTRCA requires training label')
        if X is None:
            raise ValueError('eTRCA requires training data')
           
        template_sig = gen_template(X, Y) # List of shape: (stimulus_num,); 
                                          # Template shape: (filterbank_num, channel_num, signal_len)
        self.model['template_sig'] = template_sig

        # spatial filters
        #   U: (filterbank_num * stimulus_num * channel_num * n_component)
        #   X: (filterbank_num, channel_num, signal_len)
        filterbank_num = template_sig[0].shape[0]
        stimulus_num = len(template_sig)
        channel_num = template_sig[0].shape[1]
        # n_component = 1
        U_trca = np.zeros((filterbank_num, 1, channel_num, stimulus_num))
        possible_class = list(set(Y))
        possible_class.sort(reverse = False)
        for filterbank_idx in range(filterbank_num):
            X_train = [[X[i][filterbank_idx,:,:] for i in np.where(np.array(Y) == class_val)[0]] for class_val in possible_class]
            U = Parallel(n_jobs = self.n_jobs)(delayed(_trca_U)(X = X_single_class) for X_single_class in X_train)
            for stim_idx, u in enumerate(U):
                U_trca[filterbank_idx, 0, :, stim_idx] = u[:channel_num,0]
        U_trca = np.repeat(U_trca, repeats = stimulus_num, axis = 1)

        self.model['U'] = U_trca

    def predict(self,
            X: List[ndarray]) -> List[int]:
        weights_filterbank = self.model['weights_filterbank']
        if weights_filterbank is None:
            weights_filterbank = [1 for _ in range(X[0].shape[0])]
        if type(weights_filterbank) is list:
            weights_filterbank = np.expand_dims(np.array(weights_filterbank),1).T
        else:
            if len(weights_filterbank.shape) != 2:
                raise ValueError("'weights_filterbank' has wrong shape")
            if weights_filterbank.shape[0] != 1:
                weights_filterbank = weights_filterbank.T
        if weights_filterbank.shape[0] != 1:
            raise ValueError("'weights_filterbank' has wrong shape")

        template_sig = self.model['template_sig']
        U = self.model['U'] 

        r = Parallel(n_jobs=self.n_jobs)(delayed(partial(_r_cca_canoncorr_withUV, Y=template_sig, U=U, V=U))(X=a) for a in X)

        Y_pred = [int( np.argmax( weights_filterbank @ r_tmp)) for r_tmp in r]
        
        return Y_pred 

class ETRCAwithR(BaseModel):
    """
    eTRCA method with reference signals
    """
    def __init__(self,
                 n_component: Optional[int] = None,
                 n_jobs: Optional[int] = None,
                 weights_filterbank: Optional[List[float]] = None):
        if n_component is not None:
            warnings.warn("Although 'n_component' is provided, it will not considered in eTRCA")
        n_component = 1
        super().__init__(ID = 'eTRCA-R',
                         n_component = n_component,
                         n_jobs = n_jobs,
                         weights_filterbank = weights_filterbank)
        self.model['U'] = None # Spatial filter of EEG

    def __copy__(self):
        copy_model = ETRCAwithR(n_component = None,
                                n_jobs = self.n_jobs,
                                weights_filterbank = self.model['weights_filterbank'])
        copy_model.model = deepcopy(self.model)
        return copy_model

    def fit(self,
            freqs: Optional[List[float]] = None,
            X: Optional[List[ndarray]] = None,
            Y: Optional[List[int]] = None,
            ref_sig: Optional[List[ndarray]] = None):
        if Y is None:
            raise ValueError('eTRCA with reference signals requires training label')
        if X is None:
            raise ValueError('eTRCA with reference signals training data')
        if ref_sig is None:
            raise ValueError('eTRCA with reference signals requires sine-cosine-based reference signal')

        template_sig = gen_template(X, Y) # List of shape: (stimulus_num,); 
                                          # Template shape: (filterbank_num, channel_num, signal_len)
        self.model['template_sig'] = template_sig

        separated_trainSig = separate_trainSig(X, Y)
        ref_sig_Q, ref_sig_R, ref_sig_P = qr_list(ref_sig)

        U_all_stimuli = Parallel(n_jobs=self.n_jobs)(delayed(partial(_trcaR_cal_template_U, n_component = self.n_component))(X_single_stimulus = a, I = Q @ Q.T) for a, Q in zip(separated_trainSig, ref_sig_Q))
        U_trca = [u for u in U_all_stimuli]
        U_trca = np.concatenate(U_trca, axis = 2)
        U_trca = np.expand_dims(U_trca, axis = 1)
        U_trca = np.repeat(U_trca, repeats = len(U_all_stimuli), axis = 1)
        self.model['U'] = U_trca

    def predict(self,
            X: List[ndarray]) -> List[int]:
        weights_filterbank = self.model['weights_filterbank']
        if weights_filterbank is None:
            weights_filterbank = [1 for _ in range(X[0].shape[0])]
        if type(weights_filterbank) is list:
            weights_filterbank = np.expand_dims(np.array(weights_filterbank),1).T
        else:
            if len(weights_filterbank.shape) != 2:
                raise ValueError("'weights_filterbank' has wrong shape")
            if weights_filterbank.shape[0] != 1:
                weights_filterbank = weights_filterbank.T
        if weights_filterbank.shape[0] != 1:
            raise ValueError("'weights_filterbank' has wrong shape")

        template_sig = self.model['template_sig']
        U = self.model['U'] 

        r = Parallel(n_jobs=self.n_jobs)(delayed(partial(_r_cca_canoncorr_withUV, Y=template_sig, U=U, V=U))(X=a) for a in X)

        Y_pred = [int( np.argmax( weights_filterbank @ r_tmp)) for r_tmp in r]
        
        return Y_pred 

class MSETRCA(BaseModel):
    """
    ms-eTRCA method
    """
    def __init__(self,
                 n_neighbor: int = 2,
                 n_component: Optional[int] = None,
                 n_jobs: Optional[int] = None,
                 weights_filterbank: Optional[List[float]] = None):
        if n_component is not None:
            warnings.warn("Although 'n_component' is provided, it will not considered in eTRCA")
        n_component = 1
        super().__init__(ID = 'ms-eTRCA',
                         n_component = n_component,
                         n_jobs = n_jobs,
                         weights_filterbank = weights_filterbank)
        self.n_neighbor = n_neighbor
        self.model['U'] = None # Spatial filter of EEG

    def __copy__(self):
        copy_model = MSETRCA(n_neighbor = self.n_neighbor,
                             n_component = None,
                             n_jobs = self.n_jobs,
                             weights_filterbank = self.model['weights_filterbank'])
        copy_model.model = deepcopy(self.model)
        return copy_model

    def fit(self,
            freqs: Optional[List[float]] = None,
            X: Optional[List[ndarray]] = None,
            Y: Optional[List[int]] = None,
            ref_sig: Optional[List[ndarray]] = None):
        if freqs is None:
            raise ValueError('ms-eTRCA requires the list of stimulus frequencies')
        if Y is None:
            raise ValueError('ms-eTRCA requires training label')
        if X is None:
            raise ValueError('ms-eTRCA requires training data')
           
        template_sig = gen_template(X, Y) # List of shape: (stimulus_num,); 
                                          # Template shape: (filterbank_num, channel_num, signal_len)
        self.model['template_sig'] = template_sig

        # spatial filters
        #   U: (filterbank_num * stimulus_num * channel_num * n_component)
        #   X: (filterbank_num, channel_num, signal_len)
        filterbank_num = template_sig[0].shape[0]
        stimulus_num = len(template_sig)
        channel_num = template_sig[0].shape[1]
        n_neighbor = self.n_neighbor
        # n_component = 1
        d0 = int(np.floor(n_neighbor/2))
        _, freqs_idx, return_freqs_idx = sort(freqs)
        U_trca = np.zeros((filterbank_num, 1, channel_num, stimulus_num))
        possible_class = list(set(Y))
        possible_class.sort(reverse = False)
        for filterbank_idx in range(filterbank_num):
            X_train = [[X[i][filterbank_idx,:,:] for i in np.where(np.array(Y) == class_val)[0]] for class_val in possible_class]
            X_train = [X_train[i] for i in freqs_idx]

            trca_X1, trca_X2 = zip(*Parallel(n_jobs=self.n_jobs)(delayed(_trca_U_1)(a) for a in X_train))

            trca_X1_mstrca = []
            trca_X2_mstrca = []
            for class_idx in range(1,stimulus_num+1):
                if class_idx <= d0:
                    start_idx = 0
                    end_idx = n_neighbor
                elif class_idx > d0 and class_idx < (stimulus_num-d0+1):
                    start_idx = class_idx - d0 - 1
                    end_idx = class_idx + (n_neighbor-d0-1)
                else:
                    start_idx = stimulus_num - n_neighbor
                    end_idx = stimulus_num
                trca_X1_mstrca_tmp = [trca_X1[i] for i in range(start_idx, end_idx)]
                trca_X1_mstrca.append(np.concatenate(trca_X1_mstrca_tmp, axis=-1))
                trca_X2_mstrca_tmp = [trca_X2[i].T for i in range(start_idx, end_idx)]
                trca_X2_mstrca.append(np.concatenate(trca_X2_mstrca_tmp, axis=-1))

            U = Parallel(n_jobs = self.n_jobs)(delayed(_trca_U_2)(trca_X1 = trca_X1_single_class, trca_X2 = trca_X2_single_class.T) for trca_X1_single_class, trca_X2_single_class in zip(trca_X1_mstrca, trca_X2_mstrca))
            for stim_idx, u in enumerate(U):
                U_trca[filterbank_idx, 0, :, stim_idx] = u[:channel_num,0]
        U_trca = np.repeat(U_trca[:,:,:,return_freqs_idx], repeats = stimulus_num, axis = 1)

        self.model['U'] = U_trca

    def predict(self,
            X: List[ndarray]) -> List[int]:
        weights_filterbank = self.model['weights_filterbank']
        if weights_filterbank is None:
            weights_filterbank = [1 for _ in range(X[0].shape[0])]
        if type(weights_filterbank) is list:
            weights_filterbank = np.expand_dims(np.array(weights_filterbank),1).T
        else:
            if len(weights_filterbank.shape) != 2:
                raise ValueError("'weights_filterbank' has wrong shape")
            if weights_filterbank.shape[0] != 1:
                weights_filterbank = weights_filterbank.T
        if weights_filterbank.shape[0] != 1:
            raise ValueError("'weights_filterbank' has wrong shape")

        template_sig = self.model['template_sig']
        U = self.model['U'] 

        r = Parallel(n_jobs=self.n_jobs)(delayed(partial(_r_cca_canoncorr_withUV, Y=template_sig, U=U, V=U))(X=a) for a in X)

        Y_pred = [int( np.argmax( weights_filterbank @ r_tmp)) for r_tmp in r]
        
        return Y_pred 


class MSCCA_and_MSETRCA(BaseModel):
    """
    ms-CCA + ms-eTRCA
    """
    def __init__(self,
                 n_neighbor_mscca: int = 12,
                 n_neighber_msetrca: int = 2,
                 n_component: int = 1,
                 n_jobs: Optional[int] = None,
                 weights_filterbank: Optional[List[float]] = None):
        """
        Special parameter
        ------------------
        n_neighbor_mscca: int
            Number of neighbors considered for computing spatical filter of ms-CCA
        n_neighber_msetrca: int
            Number of neighbors considered for computing spatical filter of ms-eTRCA
        """
        super().__init__(ID = 'ms-CCA + ms-eTRCA',
                         n_component = n_component,
                         n_jobs = n_jobs,
                         weights_filterbank = weights_filterbank)
        self.n_neighbor_mscca = n_neighbor_mscca
        self.n_neighber_msetrca = n_neighber_msetrca
        
        self.model['U_mscca'] = None
        self.model['V_mscca'] = None

        self.model['U_msetrca'] = None
        
    def __copy__(self):
        copy_model = MSCCA_and_MSETRCA(n_neighbor_mscca = self.n_neighbor_mscca,
                                       n_neighber_msetrca = self.n_neighbor_mscca,
                                       n_component = self.n_component,
                                       n_jobs = self.n_jobs,
                                       weights_filterbank = self.model['weights_filterbank'])
        copy_model.model = deepcopy(self.model)
        return copy_model

    def fit(self,
            freqs: Optional[List[float]] = None,
            X: Optional[List[ndarray]] = None,
            Y: Optional[List[int]] = None,
            ref_sig: Optional[List[ndarray]] = None):
        if freqs is None:
            raise ValueError('ms-CCA+ms-eTRCA requires the list of stimulus frequencies')
        if ref_sig is None:
            raise ValueError('ms-CCA+ms-eTRCA requires sine-cosine-based reference signal')
        if Y is None:
            raise ValueError('ms-CCA+ms-eTRCA requires training label')
        if X is None:
            raise ValueError('ms-CCA+ms-eTRCA requires training data')

        # save reference
        self.model['ref_sig'] = ref_sig

        # generate template 
        template_sig = gen_template(X, Y) # List of shape: (stimulus_num,); 
                                           # Template shape: (filterbank_num, channel_num, signal_len)
        self.model['template_sig'] = template_sig
        
        self.fit_mscca(freqs, ref_sig, template_sig)
        self.fit_msetrca(freqs, X, Y)
        
    def fit_mscca(self,
                  freqs: Optional[List[float]] = None,
                  ref_sig: Optional[List[ndarray]] = None,
                  template_sig: Optional[List[ndarray]] = None):
        # spatial filters of template and reference: U3 and V3
        #   U3: (filterbank_num * stimulus_num * channel_num * n_component)
        #   V3: (filterbank_num * stimulus_num * harmonic_num * n_component)
        filterbank_num = template_sig[0].shape[0]
        stimulus_num = len(template_sig)
        channel_num = template_sig[0].shape[1]
        harmonic_num = ref_sig[0].shape[0]
        n_component = self.n_component
        n_neighbor = self.n_neighbor_mscca
        # construct reference and template signals for ms-cca
        d0 = int(np.floor(n_neighbor/2))
        U = np.zeros((filterbank_num, stimulus_num, channel_num, n_component))
        V = np.zeros((filterbank_num, stimulus_num, harmonic_num, n_component))
        _, freqs_idx, return_freqs_idx = sort(freqs)
        ref_sig_sort = [ref_sig[i] for i in freqs_idx]
        template_sig_sort = [template_sig[i] for i in freqs_idx]
        ref_sig_mscca = []
        template_sig_mscca = []
        for class_idx in range(1,stimulus_num+1):
            if class_idx <= d0:
                start_idx = 0
                end_idx = n_neighbor
            elif class_idx > d0 and class_idx < (stimulus_num-d0+1):
                start_idx = class_idx - d0 - 1
                end_idx = class_idx + (n_neighbor-d0-1)
            else:
                start_idx = stimulus_num - n_neighbor
                end_idx = stimulus_num
            ref_sig_tmp = [ref_sig_sort[i] for i in range(start_idx, end_idx)]
            ref_sig_mscca.append(np.concatenate(ref_sig_tmp, axis = -1))
            template_sig_tmp = [template_sig_sort[i] for i in range(start_idx, end_idx)]
            template_sig_mscca.append(np.concatenate(template_sig_tmp, axis = -1))
        for filterbank_idx in range(filterbank_num):
            U_tmp, V_tmp, _ = zip(*Parallel(n_jobs=self.n_jobs)(delayed(partial(canoncorr, force_output_UV = True))(X=template_sig_single[filterbank_idx,:,:].T, 
                                                                                                                    Y=ref_sig_single.T) 
                                                        for template_sig_single, ref_sig_single in zip(template_sig_mscca,ref_sig_mscca)))
            for stim_idx, (u, v) in enumerate(zip(U_tmp,V_tmp)):
                U[filterbank_idx, stim_idx, :, :] = u[:channel_num,:n_component]
                V[filterbank_idx, stim_idx, :, :] = v[:harmonic_num,:n_component]
        self.model['U_mscca'] = U[:, return_freqs_idx, :, :]
        self.model['V_mscca'] = V[:, return_freqs_idx, :, :]
    
    def fit_msetrca(self,
                    freqs: Optional[List[float]] = None,
                    X: Optional[List[ndarray]] = None,
                    Y: Optional[List[int]] = None):
        # spatial filters
        #   U: (filterbank_num * stimulus_num * channel_num * n_component)
        #   X: (filterbank_num, channel_num, signal_len)
        filterbank_num = X[0].shape[0]
        stimulus_num = len(freqs)
        channel_num = X[0].shape[1]
        n_neighbor = self.n_neighber_msetrca
        # n_component = 1
        d0 = int(np.floor(n_neighbor/2))
        _, freqs_idx, return_freqs_idx = sort(freqs)
        U_trca = np.zeros((filterbank_num, 1, channel_num, stimulus_num))
        possible_class = list(set(Y))
        possible_class.sort(reverse = False)
        for filterbank_idx in range(filterbank_num):
            X_train = [[X[i][filterbank_idx,:,:] for i in np.where(np.array(Y) == class_val)[0]] for class_val in possible_class]
            X_train = [X_train[i] for i in freqs_idx]

            trca_X1, trca_X2 = zip(*Parallel(n_jobs=self.n_jobs)(delayed(_trca_U_1)(a) for a in X_train))

            trca_X1_mstrca = []
            trca_X2_mstrca = []
            for class_idx in range(1,stimulus_num+1):
                if class_idx <= d0:
                    start_idx = 0
                    end_idx = n_neighbor
                elif class_idx > d0 and class_idx < (stimulus_num-d0+1):
                    start_idx = class_idx - d0 - 1
                    end_idx = class_idx + (n_neighbor-d0-1)
                else:
                    start_idx = stimulus_num - n_neighbor
                    end_idx = stimulus_num
                trca_X1_mstrca_tmp = [trca_X1[i] for i in range(start_idx, end_idx)]
                trca_X1_mstrca.append(np.concatenate(trca_X1_mstrca_tmp, axis=-1))
                trca_X2_mstrca_tmp = [trca_X2[i].T for i in range(start_idx, end_idx)]
                trca_X2_mstrca.append(np.concatenate(trca_X2_mstrca_tmp, axis=-1))

            U = Parallel(n_jobs = self.n_jobs)(delayed(_trca_U_2)(trca_X1 = trca_X1_single_class, trca_X2 = trca_X2_single_class.T) for trca_X1_single_class, trca_X2_single_class in zip(trca_X1_mstrca, trca_X2_mstrca))
            for stim_idx, u in enumerate(U):
                U_trca[filterbank_idx, 0, :, stim_idx] = u[:channel_num,0]
        U_trca = np.repeat(U_trca[:,:,:,return_freqs_idx], repeats = stimulus_num, axis = 1)

        self.model['U_msetrca'] = U_trca
        
        
    def predict_mscca(self,
                      X: List[ndarray]) -> List[ndarray]:
        ref_sig = self.model['ref_sig']
        # template_sig = self.model['template_sig']
        U = self.model['U_mscca']
        V = self.model['V_mscca']

        r1 = Parallel(n_jobs=self.n_jobs)(delayed(partial(_r_cca_canoncorr_withUV, Y=ref_sig, U=U, V=V))(X=a) for a in X)
        # r2 = Parallel(n_jobs=self.n_jobs)(delayed(partial(_r_cca_canoncorr_withUV, Y=template_sig, U=U, V=U))(X=a) for a in X)
        
        # Y_pred = [int( np.argmax( weights_filterbank @ (np.sign(r1_single) * np.square(r1_single) + 
        #                                                 np.sign(r2_single) * np.square(r2_single)))) for r1_single, r2_single in zip(r1, r2)]
        
        return r1
    def predict_msetrca(self,
                        X: List[ndarray]) -> List[ndarray]:
        template_sig = self.model['template_sig']
        U = self.model['U_msetrca'] 

        r = Parallel(n_jobs=self.n_jobs)(delayed(partial(_r_cca_canoncorr_withUV, Y=template_sig, U=U, V=U))(X=a) for a in X)

        # Y_pred = [int( np.argmax( weights_filterbank @ r_tmp)) for r_tmp in r]
        
        return r

    def predict(self,
                X: List[ndarray]) -> List[int]:
        weights_filterbank = self.model['weights_filterbank']
        if weights_filterbank is None:
            weights_filterbank = [1 for _ in range(X[0].shape[0])]
        if type(weights_filterbank) is list:
            weights_filterbank = np.expand_dims(np.array(weights_filterbank),1).T
        else:
            if len(weights_filterbank.shape) != 2:
                raise ValueError("'weights_filterbank' has wrong shape")
            if weights_filterbank.shape[0] != 1:
                weights_filterbank = weights_filterbank.T
        if weights_filterbank.shape[0] != 1:
            raise ValueError("'weights_filterbank' has wrong shape")

        r1 = self.predict_mscca(X)
        r2 = self.predict_msetrca(X)

        Y_pred = [int( np.argmax( weights_filterbank @ (np.sign(r1_single) * np.square(r1_single) + 
                                                        np.sign(r2_single) * np.square(r2_single)))) for r1_single, r2_single in zip(r1, r2)]
        return Y_pred
