function isEmail(emailid) 
{
	var pattern = new RegExp(/^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i);
	return pattern.test(emailid);
}

function isPin(pin) 
{
	var reg = /^[0-9]+$/;	
	return reg.test(pin);
}

function isPassword(password) 
{
	var pattern = new RegExp(/^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$/);
	return pattern.test(password);
}


function isName(str) 
{
	str=str.trim();
	var reg = /^[a-zA-Z\s]+$/;
	return reg.test(str);
}

function isValidURL(url)
{
	//regular expression for URL
	//var pattern = /^(http|https)?:\/\/[a-zA-Z0-9-\.]+\.[a-z]{2,4}/;
	var pattern = /^(([\w]+:)?\/\/)?(([\d\w]|%[a-fA-f\d]{2,2})+(:([\d\w]|%[a-fA-f\d]{2,2})+)?@)?([\d\w][-\d\w]{0,253}[\d\w]\.)+[\w]{2,4}(:[\d]+)?(\/([-+_~.\d\w]|%[a-fA-f\d]{2,2})*)*(\?(&?([-+_~.\d\w]|%[a-fA-f\d]{2,2})=?)*)?(#([-+_~.\d\w]|%[a-fA-f\d]{2,2})*)?$/;
	if(pattern.test(url))
	{
		return true;
	} 
	else 
	{
		return false;
	}
}

function isNumber(no)
{
	 var regexp1=new RegExp("[a-zA-z]");
	 return regexp1.test(no);
}

function phonenumber(inputtxt)  
    {  
	  // var isnum = /^\+?\d+$/.test(inputtxt);
	   //var  isnum = /[0-9 -()+]+$/.test(inputtxt);
	  var  isnum =/^[+]*[(]{0,1}[0-9]{1,3}[)]{0,1}[-\s\.\/0-9]*$/.test(inputtxt);
	  
	   //alert('ok');
	   // var phoneno = /^\d{16}$/;  
      if(isnum)  
      {  
	      /*var regexp1=new RegExp("[a-zA-z]");
		  if(regexp1.test(inputtxt))
		  {
			   //alert('ok');
			  return false;  
		  }
		  else
		  {
			  return true;   
		  }*/
		  return true;
      }  
      else  
      {  
		//alert("message");  
		return false;  
      }  
    }	
	
	function iMobile(inputtxt)
{
    if(!isNaN(inputtxt))
        {
		    var len=inputtxt.length;
		    if(len>=10)
		        {
		            return true;
		        
		        }
		    else{	
		        	return false;
		    	}
        }
    else{
        return false;
        
    }
}
function isFristCharacterSpace(string)
{
	//regular  for avoiding frist character space
	//string1=string.trim() 
	//alert(string[0])
	//string.charAt(0)==' '
	string=string.trim();
	if(string=='')
	{
		return false;
	}
	else
	{
		return true;
	}
}


function isNull(string)
{
	//regular  for avoiding frist character space
	//string1=string.trim() 
	//alert(string[0])
	//string.charAt(0)==' '
	string=string.trim();
	if(string=='')
	{
		return false;
	}
	else
	{
		return true;
	}
}


function strWordCounter(string)
{
	var regex = /\s+/gi;
	var wordCount = string.trim().replace(regex, ' ').split(' ').length;
	var totalChars = string.length;
	var charCount = string.trim().length;
	var charCountNoSpace = string.replace(regex, '').length;
	
	return wordCount;
}


//start Array validation 


//end Array validation 