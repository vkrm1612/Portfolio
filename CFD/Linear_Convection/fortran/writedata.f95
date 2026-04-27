program writedata 

implicit none 

real :: x,y,z

x = 23
y = 45
z = 95

open(12, file = 'writtendata.txt')


write(12,*) x,y,z


print *, 'your data has been written'


end program writedata
