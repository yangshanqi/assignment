package de.unistgt.ipvs.vs.ex1.calcSocketServer;
import de.unistgt.ipvs.vs.ex1.calculation.ICalculation;
import de.unistgt.ipvs.vs.ex1.calculationImpl.CalculationImpl;

import java.io.InputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.util.regex.Pattern;
import java.util.regex.Matcher;


public class ClientServiceThread extends Thread {
	
	private Socket client;
	private InputStream instream;
	private OutputStream outstream;
	private ICalculation cal;
	private int result;
	private boolean notEnd;
	int calmode=0;
	
	public ClientServiceThread(Socket clientSocket)
	{
		this.client = clientSocket;
		result = 0;
	}
	
	public void run()
	{
		try {
			cal =  new CalculationImpl();

			instream = client.getInputStream();
			outstream = client.getOutputStream();

            ObjectOutputStream oosOut = new ObjectOutputStream(outstream);
            ObjectInputStream oisIn = new ObjectInputStream(instream);
            
            //send the ready message immediately  
			oosOut.writeObject("<08:RDY>");                               			
			notEnd = true;
			
			while (notEnd)
			{
				String inMessage = (String)oisIn.readObject();
				oosOut.writeObject("<07:OK>");
				
				//extract the content between '<' and '>'
				String patternMessage ="\\<(.*?)\\>";                      
				Pattern pt = Pattern.compile(patternMessage);
				Matcher mt = pt.matcher(inMessage);
				if (mt.find()) {
					inMessage =  mt.group(0);				
	                inMessage= inMessage.trim();
				
	                //get the first and last character to compare with the format<number:  ....  >
				    char first = inMessage.charAt(0);           
				    char last = inMessage.charAt(inMessage.length()-1);
				    char fourth = inMessage.charAt(3);
				    if (first != '<' | last != '>' | fourth !=':')
					oosOut.writeObject("<20£ºINVAILD MESSAGE>");          
				
				    String content = inMessage.substring(4,inMessage.length()-1);
				    content = content.trim();
				    String[] op = content.split("\\s+");
				
					for (int x = 0; x<op.length; x++)                         
					{
						
					    //if there is a valid content, such like addition, then set the current calculation mode with this operator
						if (op[x].toUpperCase().equals("ADD"))       
						{
							calmode = 1;
							oosOut.writeObject("<OK ADD>");
						}
						else if (op[x].toUpperCase().equals("SUB"))
						{
							calmode = 2;
							oosOut.writeObject("<OK SUB>");
						}
						else if (op[x].toUpperCase().equals("MUL"))
						{
							calmode = 3;
							oosOut.writeObject("<OK MUL>");
						}
						
						//If the request is result, then get the result and terminate the loop. And sent the result to the client. 
						else if (op[x].toUpperCase().equals("RES"))           
						{
						    result = cal.getResult();
							oosOut.writeObject("<OK RES " + result + " >");
							notEnd = false;
							                                       
						}
						
						//If there is a operand, then it is executed with current calculation mode.
						else if (op[x].matches("[0-9]+")|op[x].matches("-[0-9]+"))  
						{
							int num = Integer.parseInt(op[x]);
							switch (calmode) {
							case 0:
								oosOut.writeObject("<ERR " + op[x] + ">");
							    break;
							case 1: 
								cal.add(num);
								oosOut.writeObject("<OK "+op[x]+">");
							    break;
							case 2:
								cal.subtract(num);
								oosOut.writeObject("<OK "+op[x]+">");
								break;
							case 3:
								cal.multiply(num);
								oosOut.writeObject("<OK "+op[x]+">");
								break;
							}
						}
						
						//If there is no match information, then send error to the client
						else
						{
							oosOut.writeObject("<ERR "+ op[x] +">");  
						}
						
					}
					//After it has processed every message, send <FIN>
					oosOut.writeObject("<FIN>");  
			    }
			}		
								
				oosOut.close();
				oisIn.close();
				client.close();
			
	}catch (Exception e)
		{
		     e.printStackTrace();
		}

	}
}
