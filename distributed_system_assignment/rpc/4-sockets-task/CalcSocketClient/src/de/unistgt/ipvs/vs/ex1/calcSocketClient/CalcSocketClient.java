package de.unistgt.ipvs.vs.ex1.calcSocketClient;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.Socket;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Implement the connectTo-, disconnect-, and calculate-method of this class
 * as necessary to complete the assignment. You may also add some fields or methods.
 */
public class CalcSocketClient {
	private int    rcvdOKs;		// --> Number of   valid message contents
	private int    rcvdErs;		// --> Number of invalid message contents
	private int    calcRes;		// --> Calculation result (cf. 'RES')
	private Socket server;
	private ObjectOutputStream oosOut;
	private ObjectInputStream oisIn;
	
	public CalcSocketClient() {
		this.rcvdOKs   = 0;
		this.rcvdErs   = 0;
		this.calcRes   = 0;
	}
	
	// Do not change this method ..
	public int getRcvdOKs() {
		return rcvdOKs;
	}

	// Do not change this method ..
	public int getRcvdErs() {
		return rcvdErs;
	}

	// Do not change this method ..
	public int getCalcRes() {
		return calcRes;
	}

	public boolean connectTo(String srvIP, int srvPort) {
		// TODO
		try {
			server = new Socket(srvIP, srvPort);
			oosOut = new ObjectOutputStream(server.getOutputStream());
			oisIn = new ObjectInputStream(server.getInputStream());
			
			if ((String)oisIn.readObject() == "<08:RDY>")            //need while true?
				return true;
			else
				return false;
		}
		catch (IOException | ClassNotFoundException e)
		{
			e.printStackTrace();
			return false;
		}
	}

	public boolean disconnect() {
		// TODO
		try {
			oosOut.close();
			oisIn.close();
			server.close();
			return true;
		}
		catch (IOException e) {
			e.printStackTrace();
			return false;
		}
	}

	public boolean calculate(String request) throws IOException {
		// TODO
		oosOut.writeObject(request);
		boolean notEnd = true;
		String inMessage = "";

		try {
			inMessage = (String) oisIn.readObject();
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		}
		
		
		//If there is a valid message, extract it and begin counting.
		Pattern pt = Pattern.compile("\\<(.*?)\\>");
		Matcher mt =pt.matcher(inMessage);

		
		if (mt.find()) {
			if (mt.group(1).equals("07:OK")) {				
				rcvdOKs += 1;
				while (notEnd) {
					try {
						inMessage = (String) oisIn.readObject();						
					} catch (ClassNotFoundException e) {
						e.printStackTrace();
					}
					
					//If there is "FIN", it means that server has process all valid message. The client can send another request. 
					if (inMessage.contains("FIN")) {
						notEnd = false;
					}

					//If there is message which contains "RES", it will extract the result.
					else if (inMessage.contains("RES")) {
						String[] content = inMessage.split("\\s");
						calcRes = Integer.parseInt(content[2]);
						rcvdOKs += 1;
					}

					//According to the content of the message from server, it counts the number of OKs and errs.
					else if (inMessage.contains("OK")) {
						rcvdOKs += 1;
					}

					else if (inMessage.contains("ERR")) {
						rcvdErs += 1;
					}						
				}
			} else {
				System.err.println("The server sends wrong beginning message. The communication cann't start.");
				return false;
			}
		} else {
			System.err.println("There is no valid message. There must be something wrong");
			return false;
		}
		return true;
	}
}
