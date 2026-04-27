program format 

implicit none 

double precision, dimension(4) :: matrix
integer :: i


do i=1,4
	matrix(i) = cos(0.1 * i)
end do


print *, matrix

end program format
