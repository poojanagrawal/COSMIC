SRC_DIR=METISSE/src

#com
FC=gfortran
DEBUG=-g3 -fbacktrace -fcheck=all -fbounds-check
WARN=-Wall -pedantic -Wno-tabs -Wextra
# -Wconversion

#Optimization flag
OPT=-O3

#NOT USED
#Tells gfortran to compile using OpenMP
OMP=-fopenmp


FFLAGS1= -ffree-form -shared -fPIC
FFLAGS2= -ffixed-form -fimplicit-none 
FFLAGS3= -shared -fPIC


track_support.o: $(SRC_DIR)/track_support.f90
z_support.o: $(SRC_DIR)/z_support.f90 track_support.o 
#sse_support.o: $(SRC_DIR)/sse_support.f90 track_support.o z_support.o 
#remnant_support.o: $(SRC_DIR)/remnant_support.f90 track_support.o sse_support.o
#interp_support.o: $(SRC_DIR)/interp_support.f90 track_support.o z_support.o sse_support.o
  
#alloc_track.o: $(SRC_DIR)/alloc_track.f90 track_support.o
#dealloc_track.o: $(SRC_DIR)/dealloc_track.f90 track_support.o
#assign_commons.o: $(SRC_DIR)/assign_commons.f90 track_support.o remnant_support.o
#metisse_mlwind.o: $(SRC_DIR)/metisse_mlwind.f90 track_support.o
#deltat.o: $(SRC_DIR)/deltat.f90 track_support.o
zcnsts_METISSE.o: $(SRC_DIR)/zcnsts_METISSE.f90 z_support.o track_support.o
#star.o: $(SRC_DIR)/star.f90 track_support.o interp_support.o sse_support.o 
#hrdiag.o: $(SRC_DIR)/hrdiag.f90 track_support.o interp_support.o remnant_support.o sse_support.o
#comenv_lambda.o: $(SRC_DIR)/comenv_lambda.f90 track_support.o


#%.o : $(SRC_DIR)/%.f
#	$(FC) $(OMP) $(FFLAGS2) -c $<

SRCE1 = \
evolv2_wrapper.f evolv2.f benchmarkevolv2.f bpp_array.f checkstate.f comenv.f comprad.f concatkstars.f corerd.f deltat.f dgcore.f evolv1.f gntage.f hrdiag.f instar.f int64.f kick.f mix.f mlwind.f mrenv.f ran3.f rl.f star.f tausworth.f zcnsts.f zfuncs.f

OBJT1 = $(SRCE1:.f=.o)

%.o : %.f
	$(FC) $(FFLAGS3) -c $^ 

%.o : $(SRC_DIR)/%.f90
	$(FC) $(OMP) $(FFLAGS1) -c $<

evolv2 : $(OBJT1) track_support.o z_support.o zcnsts_METISSE.o
	$(FC) -o evolv2.so $^
#gfortran -shared -o evolv2.so *.o

clean:
	#rm -f $(BSE_DIR)/$(SSE_METISSE) $(BSE_DIR)/$(BSE_METISSE)
	rm -f *.mod *.o *.so


