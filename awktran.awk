# Translate %XX to equiv character
BEGIN	{
	HEX = "0123456789ABCDEF"
	}
	{
	SZ=length($0)
	for ( i=1; i<=SZ; i++)
		{
		CH = substr($0,i,1)
		if (CH == "%")
			{
			CH1 = substr($0,++i,1) 
			CH2 = substr($0,++i,1) 
			CH1 = index(HEX,CH1) - 1
			CH2 = index(HEX,CH2) - 1
			CH = (CH1*16)+CH2
			}
		printf("%c",CH)
		}
	printf("\n");
	}
	
