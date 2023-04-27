select eID , sum(elHour)
from Elist
where year(elDate)="$input_year" and month(elDate)="$input_month"
group by eID
