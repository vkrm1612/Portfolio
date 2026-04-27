program vol

implicit none 

double precision :: rad1, rad2, vol1, vol2

print *, 'please enter rad1 and rad2'

read *,  rad1, rad2


call volume(rad1,vol1)
call volume(rad2,vol2)



print *, abs(vol1 - vol2)





end program vol



!----------------------------------------------------------------


subroutine volume(rad,vol)

implicit none 

double precision :: rad , vol , pi

pi = 4.0 * atan(1.0)

vol = (4.0/3.0) * pi * rad**3


end subroutine volume
