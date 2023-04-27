select regID, regCome, sName, pID
from reg_not_done left join Elist using(regID)
where el_ID is NULL