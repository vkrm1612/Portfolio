program linear_convection

implicit none

real :: nx, nt, dx, dt, i, j

integer, parameter :: ikind =3

double precision,  dimension(20) :: x
double precision, dimension(20) :: un
double precision, dimension(20) :: u


nx = 20
nt = 50
dx = 2 / (nx -1)
dt = 0.01
j = 1


do i=0,2,dx

x(j) = i

j = j+1

end do

do i=1,nx

if (x(i) >= 0.5 .and. x(i) <= 1) then 
	u(i) = 2
else

u(i) = 1

end if

end do

do i=1,nt
un = u
do j=2,nx

u(j) = un(j) - 1 * (dt/dx) * (un(j) - un(j-1))

end do
end do


open(10 , file = 'resu.txt')


do i=1,20

write(10,*) u(i), x(i)
end do

end program linear_convection

