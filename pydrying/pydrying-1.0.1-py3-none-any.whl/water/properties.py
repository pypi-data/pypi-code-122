# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 09:03:38 2022

@author: Hedy
"""
from numpy import sqrt
def pvsat(Temperature):
    """
    Pressure of saturated liquid, mixture or steam
    INPUT
    Temperature in °C
    Lower boundary: Tmin = 273.16; % [K] minimum temperature is triple point
    Upper boundary: Tc = 647.096; % [K] critical point temperature
    OUTPUT
    pressure p in [Pa]
    Based on IAPWS-IF97
    Reference: http://www.iapws.org/
    Author : Romdhana Hedi
    Affiliation : AgroParisTech
    Contact : romdhana@agroparistech.fr
    """
    eps = Temperature + 273.15 -0.238555575678490/(Temperature -377.0253484479800)
    A = (eps + 1167.05214527670)*eps -724213.167032060
    B = (12020.8247024700 -17.0738469400920*eps)*eps -3232555.03223330
    C = (14.9151086135300*eps -4823.26573615910)*eps + 405113.405420570
    beta = 2*C/(-B + sqrt(B*B - 4*A*C))
    return (beta*beta*beta*beta) * 1e6