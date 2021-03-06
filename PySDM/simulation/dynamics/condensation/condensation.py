"""
Created at 24.10.2019

@author: Piotr Bartman
@author: Sylwester Arabas
"""

from .products.condensation_timestep import CondensationTimestep
from ...particles import Particles
import numpy as np


default_rtol_x = 1e-8
default_rtol_thd = 1e-8


class Condensation:
    def __init__(self, particles: Particles, kappa,
                 rtol_x=default_rtol_x,
                 rtol_thd=default_rtol_thd,
                 do_advection: bool = True,
                 do_condensation: bool = True,
                 ):
        self.particles = particles
        self.environment = particles.environment
        self.kappa = kappa
        self.rtol_x = rtol_x
        self.rtol_thd = rtol_thd

        self.do_advection = do_advection
        self.do_condensation = do_condensation

        self.substeps = particles.backend.array(particles.mesh.n_cell, dtype=int)
        self.substeps[:] = np.maximum(1, int(particles.dt))

        self.products = [CondensationTimestep(self), ]

    def __call__(self):
        if self.do_advection:
            self.environment.sync()
        if self.do_condensation:
            self.particles.condensation(
                kappa=self.kappa,
                rtol_x=self.rtol_x,
                rtol_thd=self.rtol_thd,
                substeps=self.substeps
            )

