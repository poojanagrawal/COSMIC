      SUBROUTINE gntage(mc,mt,kw,zpars,m0,aj,id)
      IMPLICIT NONE
      INCLUDE 'const_bse.h'
      
      real*8 mc,mt,zpars,m0,aj
      integer kw ,id
      
      if ((using_METISSE).and.(kw<7)) then
            
          !WRITE(*,*) 'Calling METISSE_gntage'
          CALL METISSE_gntage(mc,mt,kw,zpars,m0,aj,id)
          
      elseif ((using_SSE).or.(kw.ge.7)) then
          !WRITE(*,*) 'Calling SSE_gntage'
          CALL SSE_gntage(mc,mt,kw,zpars,m0,aj,id)
      endif
      
      END
