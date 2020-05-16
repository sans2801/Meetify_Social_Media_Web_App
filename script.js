function responsive()
{
	var a=document.getElementById("navbar");
	if(a.className=="navbar")
	{
		a.className+=" resposive";
	}

	else
	{
		a.className="navbar";
	}

}