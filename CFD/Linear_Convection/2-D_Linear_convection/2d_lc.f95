program lc


implicit none 

integer :: i,j

real :: nx, ny, nt, dt, c, dx, dy, k, t

real :: U(21,21), UN(21,21)


double precision, dimension(21) :: x
double precision, dimension(21) :: y


nx = 21
ny = 21
nt = 50
dt = 0.01
c = 1
dx = 2/(nx -1)
dy = 2/(ny-1)
i=1

do k=0,2,dx

x(i) = k
y(i) = k 

end do

U = 1

do j = int(0.5 / dy) + 1, int(1.0 / dy) + 1
     do i = int(0.5 / dx) + 1, int(1.0 / dx) + 1
        u(i, j) = 2.0
     end do
  end do

do t=0,nt
UN = U
do i=2,nx-1
do j=2,ny-1

U(i,j) = UN(i,j) - c*(dt/dx)*(UN(i,j) - UN(i-1,j)) - c*dt/dy*(UN(i,j) - UN(i,j-1))

end do
end do
end do

open(10, file = 'resu.txt')

do i = 1,21
    write(10, '(21F10.4)', advance='no') (U(i, j), j = 1, 21)
    write(10, *)
end do


close(10)

end program 




















