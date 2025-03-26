-- this is an example of sql query of getting passenger trips from https://sql-academy.org/ru/sandbox
SELECT pt.id, pt.trip, pt.passenger, pt.place, p.name FROM Pass_in_trip pt INNER JOIN Passenger p