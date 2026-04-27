program conditional

implicit none 

!Declare variables

real :: x,y, su
integer :: choice

!Ask the users to choose few option

Print *, 'Please choose and option'
Print *, '1 Addition'
Print *, '2 MUltiply'
Print *, '3 Divide'

x = 12
y = 23

Read *, choice

if (choice == 1) then
	su = x + y
	Print *, 'Addition ',su
end if

if (choice ==2) then
	su = x * y
	Print *, 'Multiply ',su
end if

if (choice ==3) then
	su = x/y
	Print *,'Divide ',su
end if

!Process the choice after displaying

!Give the answer


end program conditional
