select * from Registration
	where year(regCome)="$input_year" and month(regCome)="$input_month";
