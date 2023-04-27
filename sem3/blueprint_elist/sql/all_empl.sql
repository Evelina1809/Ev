select eID, eProf, eSurename
from Employee left join Elist using(eID)
where eDLayoff is NULL and elDate != '$input_date' or elDate is NULL