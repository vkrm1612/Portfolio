program precision

implicit none 

integer, parameter :: ikind=selected_real_kind(p=18)
real(kind = ikind) :: x,y,z 

y = 10.0
x = 3.0

z = y/x 


print *, z


end program precision
