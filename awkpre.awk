# Preprocess macro file insertion
	{
	for ( i=1; i <= NF; i++)
		{
		CF = $i
		if ( CF ~ "^&&" ) 	# Macro start
			{
			CF = "data/" substr(CF,3)
			while (getline IR <CF >0)
				print IR
			next
			}
		}
	print
	}
	
