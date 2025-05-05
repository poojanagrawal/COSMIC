subroutine get_bhxrl(mass1,mass2,radius2,teff2,mdot_w2,sep,X,Lx)
    implicit none

    ! Input:
    ! mass1 =  mass of the black hole (Msun)
    ! mass2 = mass of the companion(Msun)
    ! radius2 = radius of the companion (RSun)
    ! teff2 = effective temperature of the companion
    ! mdot_w2 = wind mass loss rate of the companion
    ! sep = orbital separation (Rsun)
    ! X = hydrogen abundance = zpars(11)
    ! for calculating eddington luminosity
    !
    ! Output:
    ! Lx = X-ray luminosity of accreting BHs
    !
    ! calculations adapted from Sen+2024, https://arxiv.org/pdf/2406.08596
    ! and Sen+2021, https://arxiv.org/pdf/2106.01395

    integer, parameter :: dp = selected_real_kind(p=15)
    integer, parameter :: high = 3, mid = 2, low = 1

    real(dp), intent(in):: mass1,mass2,radius2,teff2,sep,X,mdot_w2
    real(dp), intent(out):: Lx(4)

    real(dp), parameter :: Lsun = 3.8418d+33            !luminosity of sun in CGS
    real(dp), parameter :: cgrav = 6.67428d-8            !gravitational constant in CGS
    real(dp), parameter :: Msun = 1.9892d+33             !mass of sun in CGS
    real(dp), parameter :: Rsun = 6.96d+10               !radius of sun in CGS
    real(dp), parameter :: clight_sq = 8.98755178737d+20    !speed of light in CGS
    real(dp), parameter :: msunyr_cgs = msun/3.154e+7   ! msun/yr to gm/sec
    
    real(dp) :: vorb1,Gamma2, v_esc, v_inf, v_wind, v_rel, Ledd, RISCO, &
             mdot_acc, mdot_edd, mdot_net, mdot_ratio, mdot_net_csq, &
            alpha, Racc, delta, q1, delta3, disk_crit2, wind_multiplier
        
    Lx = 0.d0
    ! return if companion is not a OB Star on MS
    if (Teff2<12500) return

    !differentiate between O star and B star
    if (Teff2 > 22000) then
        ! Gamma2 is the eddington factor
        Gamma2 = 0.2
        wind_multiplier = 2.6d0
    else
        Gamma2 = 0.1
        wind_multiplier = 1.3d0
    endif
    
    !escape speed from OB star
    v_esc = sqrt((2*cgrav*(1-Gamma2)*mass2*msun)/(radius2*rsun))                                    ! v_esc = sqrt(2*cgrav*(1-Gamma2)*mass2*msun/radius2/rsun)
    
    ! terminal velocity
    v_inf = wind_multiplier *v_esc
    
    !wind speed from OB star
    ! Eqn 1 of Sen+2021, beta = 1 for MS stars
    v_wind = v_inf*(1-radius2/sep)
    ! ~ 2000 * 1000 m/sec
    
    !orbital velocity of the BH with respect to the O star
    vorb1 = sqrt(cgrav*(mass1+mass2)*msun/sep*rsun)

    !relative velocity of the stellar wind with respect to
    ! the BH for a circular orbit
    v_rel = sqrt(v_wind*v_wind + vorb1*vorb1)
    
    !accretion disk formation criteria

    Ledd = 65335*mass1*Lsun/(1+X)             !Eqn 24                                    
    RISCO = 6*cgrav*mass1*msun/clight_sq        !Eqn 29
    mdot_edd = Ledd*RISCO/(cgrav*mass1*msun)            !Eqn 28
    
    !Rdisc/RISCO, from eqn 10 of Sen+2021
    q1 = (mass1+mass2)/mass1
    disk_crit2 = 2*clight_sq*(vorb1**6)/(27*q1*q1*v_rel**8)
                  !j_acc/3 of Shapiro+1976, eta=1/3
    
!    disk_crit1 = disk_crit2*9              !j_acc of Shapiro+1976
        
    if (disk_crit2>1) then
        !X-ray luminosity from a Keplerian accretion disk
        
        delta = (radius2*v_esc*v_esc)/(2.d0*sep*v_wind*v_wind)     !eqn 27
        delta3 = (1+delta)**(3.0/2)
        alpha = (4.d0*delta*delta*mass1*mass1*mdot_w2*msunyr_cgs)
        alpha = alpha/(delta3*mass2*mass2*mdot_edd)
        Lx(4)= Ledd*alpha/(1+sqrt(1+alpha))**2
    else
        !X-ray luminosity without an accretion disk
        
        Racc = 2*cgrav*mass1*msun/(v_rel*v_rel) ! Eq 8 of Sen+2021
        mdot_acc = (mdot_w2*msunyr_cgs*Racc*Racc*v_rel)/(4.d0*sep*rsun*sep*rsun*v_wind)                    ! Eq 12 of Sen+2021
        mdot_net = mdot_acc*(RISCO/3*Racc)**0.4   ! eqn 32
        ! event horizon for a non-spinning BH is Risco/3. In the paper Risco is used, but we use event horizon here
        
        mdot_net_csq = mdot_net*clight_sq
        mdot_ratio = mdot_net/mdot_edd
        if (mdot_ratio.gt.1d-6) then
            Lx(high) = interpolate(mdot_ratio,high)*mdot_net_csq
            Lx(mid) = interpolate(mdot_ratio,mid)*mdot_net_csq
            Lx(low) = interpolate(mdot_ratio,low)*mdot_net_csq
        elseif((mdot_ratio.gt.1d-7).and.(mdot_ratio.le.1d-6)) then
            Lx(high) = interpolate(mdot_ratio,high)*mdot_net_csq
            Lx(mid) = mdot_net_csq*6d-5
            Lx(low) = mdot_net_csq*1d-5
        else
            Lx(high) = mdot_net_csq*4d-5
            Lx(mid) = mdot_net_csq*5d-6
            Lx(low) = mdot_net_csq*1d-6
        endif
    endif
    contains

    function interpolate(xval,crit) result(yval)

    real(dp), intent(in) :: xval
    integer, intent(in) :: crit
    real(dp) :: yval
    integer :: bot, top, mid, n
    real(dp) :: x1, x2, y1, y2
    real(dp), pointer :: xdata(:), ydata(:)
   
    
    include 'epsilon.h'

    if (crit == high) then
        xdata => mdot_ratio_high
        ydata => epsilon_high
    elseif(crit==mid) then
        xdata => mdot_ratio_mid
        ydata => epsilon_mid
    elseif(crit==low)then
        xdata => mdot_ratio_low
        ydata => epsilon_low
    else
        print*,"incorrect option"
        return
    endif

    n = size(xdata)
    ! Handle out-of-bounds extrapolation
    if (xval <= xdata(1)) then
        bot = 1
        top = 2
    else if (xval >= xdata(n)) then
        bot = n-1
        top = n
    else
        ! Binary search
        bot = 1
        top = n
        do while (top - bot > 1)
          mid = (bot + top) / 2
          if (xval < xdata(mid)) then
            top = mid
          else
            bot = mid
          end if
        end do
    end if

    ! Linear interpolation
    x1 = xdata(bot)
    x2 = xdata(top)
    y1 = ydata(bot)
    y2 = ydata(top)

    yval = y1 + (xval-x1)*(y2-y1)/(x2-x1)
    ! for numerical raesons we interpolate in log quantities
    ! convert back to non-log
    yval = 10**yval
    
  end function

end subroutine
