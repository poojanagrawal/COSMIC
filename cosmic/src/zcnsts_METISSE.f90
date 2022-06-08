subroutine zcnsts_METISSE(z,zpars)
!    use track_support
!    use z_support
!    use remnant_support

    integer, parameter :: dp = selected_real_kind(p=15)

    real(dp), intent(in) :: z
    real(dp), intent(out) :: zpars(20)

    print*, 'METISSE Zcnsts', z
    zpars = 0.0
end subroutine zcnsts_METISSE

