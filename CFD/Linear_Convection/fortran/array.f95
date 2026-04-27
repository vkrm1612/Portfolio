program array 

implicit none 

integer, parameter :: ikind =3

real,allocatable,  dimension(:) :: x

integer :: elements


elements = 4

allocate(x(elements))

x(1) = 2.0
x(2) = 5.0
x(3) = 11.0

x(4) = 4.0

print *, x

deallocate(x)

end program array
