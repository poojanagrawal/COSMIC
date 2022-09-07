from ctypes import *
import numpy as np
import os

#print('cwd=',os.getcwd())
#print('list=',os.listdir())

libc = cdll.LoadLibrary(os.path.abspath("evolv2.so"))


def evolv2(m1, m2, tb, e, alpha, vk, theta, phi, omega):

    m1 = m1
    m2 = m2
    
    metallicity = 0.01
    sigma = 0

    z = byref(c_double(metallicity))
    zpars = np.zeros(20).ctypes.data_as(POINTER(c_double))
    alpha = byref(c_double(alpha))
    acc_lim = byref(c_double(-1))
    q3 = byref(c_double(0))
    sigma = byref(c_double(sigma))
    q4 = byref(c_double(0))
    natal_kick = np.zeros((2,5))
    natal_kick[0,0] = vk
    natal_kick[0,1] = phi
    natal_kick[0,2] = theta
    natal_kick[0,3] = omega
    natal_kick[0,4] = 3
    natal_kick = natal_kick.T.flatten().ctypes.data_as(POINTER(c_double))
    libc.evolv2_global_(z,zpars,alpha,acc_lim,q3,q4,natal_kick)
    kstar = np.array([1,1]).ctypes.data_as(POINTER(c_double))
    mass = np.array([m1,m2]).ctypes.data_as(POINTER(c_double))
    mass0 = np.array([m1,m2]).ctypes.data_as(POINTER(c_double))
    epoch = np.array([0.0,0.0]).ctypes.data_as(POINTER(c_double))
    ospin = np.array([0.0,0.0]).ctypes.data_as(POINTER(c_double))
    tb = byref(c_double(tb))
    ecc = byref(c_double(e))
    tphysf = byref(c_double(13700.0))
    dtp = byref(c_double(0.0))
    rad = np.array([0.0,0.0]).ctypes.data_as(POINTER(c_double))
    lumin = np.array([0.0,0.0]).ctypes.data_as(POINTER(c_double))
    massc = np.array([0.0,0.0]).ctypes.data_as(POINTER(c_double))
    radc = np.array([0.0,0.0]).ctypes.data_as(POINTER(c_double))
    menv = np.array([0.0,0.0]).ctypes.data_as(POINTER(c_double))
    renv = np.array([0.0,0.0]).ctypes.data_as(POINTER(c_double))
    B_0 = np.array([0.0,0.0]).ctypes.data_as(POINTER(c_double))
    bacc = np.array([0.0,0.0]).ctypes.data_as(POINTER(c_double))
    tacc = np.array([0.0,0.0]).ctypes.data_as(POINTER(c_double))
    tms = np.array([0.0,0.0]).ctypes.data_as(POINTER(c_double))
    bhspin = np.array([0.0,0.0]).ctypes.data_as(POINTER(c_double))
    tphys = byref(c_double(0.0))
    bkick = np.zeros(20).ctypes.data_as(POINTER(c_double))
    kick_info = np.zeros(34).ctypes.data_as(POINTER(c_double)) # Fortran treat n-D array differently than numpy
    bpp_index_out = byref(c_int64(0))
    bcm_index_out = byref(c_int64(0))
    kick_info_out = np.zeros(34).ctypes.data_as(POINTER(c_double))
    t_form = byref(c_double(0.0))
    m_form = np.array([0.0,0.0])
    e_form = byref(c_double(0.0))
    p_form = byref(c_double(0.0))
    bpp_out=np.zeros([1000,43]).flatten().ctypes.data_as(POINTER(c_double))

    libc.evolv2_(kstar,mass,tb,ecc,z,tphysf,
    dtp,mass0,rad,lumin,massc,radc,
    menv,renv,ospin,B_0,bacc,tacc,epoch,tms,
    bhspin,tphys,zpars,bkick,kick_info,
    bpp_index_out,bcm_index_out,kick_info_out,
    bpp_out)

    bpp = bpp_out._arr.reshape(43,1000)[:,0:bpp_index_out._obj.value].T

    return bpp

m1=1.0
m2=1.0 
tb=100.0 
e=0.0
alpha=1.0
vk=100 
theta=0.0 
phi=0.0 
omega=0.0

dat_out = evolv2(m1, m2, tb, e, alpha, vk, theta, phi, omega)
print(m1, m2, tb)
print(dat_out)
