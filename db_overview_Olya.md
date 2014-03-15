DB Overview
===========

Users
-----
(user_ID, first_name, last_name, car_number(optional), is_inspector(true , false), is_admin(true, false), password_hash)

Locations
------------
(name_loc, adress, description)

Places
--------------
(name_loc,place_ID, order, price, conditional(+/-))

Reservation
---------------
(user_ID, place_ID, time_start, time_end, payment)   
