select regID, pType, sName , max(elDate)
from elist_for_empl join Elist using(regID) join Employee using(eID)
where eSurename = '$input_surename' and eBirth = '$input_date' and elDate > '$today_d'
group by regID