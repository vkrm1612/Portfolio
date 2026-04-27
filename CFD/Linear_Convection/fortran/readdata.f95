program readdata

implicit none

!Declaration of variables

real :: x,y,z,a

open(10, file = 'mydata.txt')

read(10, *) x,y,z,a


print *, x,y,z,a

end program readdata
