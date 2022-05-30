import time
import threading
import sys
import warnings
from pprint import pprint
import tqdm
from typing import List, Optional
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt
from scipy.fft import fft2, ifft2, rfft2, irfft2, set_global_backend, fft, ifft, fftn, ifftn
import pyfftw
import h5py

from michael960lib.math import fourier
from michael960lib.common import overrides, experimental, deprecated
from michael960lib.common import ModifyingReadOnlyObjectError, IllegalActionError 

from torusgrid.grids import ComplexGridND
from torusgrid.dynamics import FancyEvolver, EvolverHistory, StateFunction

from ..core import KuramotoStateFunction, KuramotoBase


class KuramotoWriter:
    def __init__(self, fname: str, kura: KuramotoBase, initial_age=0):
        self.fname = fname
        self.kura = kura
        self.file = h5py.File(fname, 'w')

        self.file.create_dataset('omega', dtype='f', data=kura.omega.tolist())
        for key in kura.omega_params:
            self.file['omega'].attrs[key] = kura.omega_params[key]

        self.file.create_dataset('weight', dtype='f', data=kura.weight.tolist())
        for key in kura.weight_params:
            self.file['weight'].attrs[key] = kura.weight_params[key]

        self.file.create_dataset('theta', dtype='f', data=[kura.theta.tolist()], 
                chunks=(1, *kura.shape), maxshape=(None, *kura.shape))
        for key in kura.theta_params:
            self.file['theta'].attrs[key] = kura.theta_params[key]


        self.file.create_dataset('shape', dtype='i8', data=list(kura.shape))
        self.file.attrs['K'] = kura.K
        self.time = datetime.now()
        self.file.attrs['time'] = self.time.strftime('%Y.%m.%d-%H:%m:%S')
        self.file.create_dataset('t', dtype='f', data=[initial_age], chunks=(1,), maxshape=(None,))
        self._chunk_ind = 0

    def set_datetime_format(self, fmt='%Y.%m.%d-%H:%m:%S'):
        self.file.attrs['time'] = self.time.strftime(fmt)

    def append(self, t: float, theta: np.ndarray):
        self._chunk_ind += 1
        self.file['theta'].resize(self._chunk_ind+1, axis=0)
        self.file['theta'][self._chunk_ind] = theta.tolist()
        self.file['t'].resize(self._chunk_ind+1, axis=0)
        self.file['t'][self._chunk_ind] = t

    def get_file(self):
        return self.file
    
    def check_well_formed(self): 
        r = True
        return r

    def close(self):
        self.file.close()

class KuramotoReader:
    def __init__(self, fname: str):
        self.fname = fname
        self.file = h5py.File(fname, 'r')

        self.K = self.file.attrs['K']
        self.shape = tuple(self.file['shape'])
        self.N = np.prod(self.shape)


   
        self.theta_params = dict(self.file['theta'].attrs)
        self.theta = self.file['theta']
        self.theta_seed = self.theta_params.get('seed', '?')

        self.omega_params = dict(self.file['omega'].attrs)
        self.omega = np.array(self.file['omega'])
        self.omega_dist = self.omega_params.get('type', '?')
        self.omega0 = self.omega_params.get('mean', np.NAN)
        self.gamma = self.omega_params.get('scale', np.NaN)
        self.omega_seed = self.omega_params.get('seed', '?')

        self.weight_params = dict(self.file['weight'].attrs)
        self.weight = np.array(self.file['weight'])
        self.wk = fftn(self.weight)

        self.nu = self.weight_params.get('nu', np.NaN)
        self.weight_type = self.weight_params.get('type', '?')

        self.t = np.array(self.file['t'])
        self.Nt = len(self.t)
        self.t_max = self.t[-1]
        self.dt = self.file.attrs['dt']
        self.dT = self.t[-1] - self.t[-2]

        self.datetime = self.file.attrs.get('time', '?')

        self._Z = ComplexGridND(self.shape)
        self._Z.initialize_fft()

    def get_theta_label(self):
        return self.file['theta'].attrs.get('label', '?')

    def get_omega_label(self):
        return self.file['omega'].attrs.get('label', '?')

    def get_weight_label(self):
        return self.file['weight'].attrs.get('label', '?')


    def get_dimensions(self):
        return len(self.shape)

    def get_local_Z(self, index: int):
        theta = self.theta[index]
        self._Z.set_psi(np.exp(1j*theta))
        self._Z.fft()
        self._Z.psi_k *= self.wk
        self._Z.ifft()
        return self._Z.psi

    def get_global_Z(self, index: int):
        theta = self.theta[index]
        return np.sum(np.exp(1j*theta)) / self.N

    def get_correlation_function(self, index: int, shift=True):
        theta = self.theta[index]
        self._Z.set_psi(np.exp(1j*theta))
        Z0 = self.get_global_Z(index)

        self._Z.fft()
        self._Z.psi_k *= np.conj(self._Z.psi_k)
        self._Z.ifft()

        corr = self._Z.psi / self.N - np.abs(Z0)**2
        
        if shift:
            shift = tuple(n//2 for n in self.shape)
            axes = np.arange(self.get_dimensions())
            corr = np.roll(corr, shift, axis=axes)

        return corr


