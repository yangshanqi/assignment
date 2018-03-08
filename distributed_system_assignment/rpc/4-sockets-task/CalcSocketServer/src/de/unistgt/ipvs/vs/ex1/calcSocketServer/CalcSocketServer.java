package de.unistgt.ipvs.vs.ex1.calcSocketServer;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * Extend the run-method of this class as necessary to complete the assignment.
 * You may also add some fields, methods, or further classes.
 */
public class CalcSocketServer extends Thread {
	private ServerSocket srvSocket;
	private int port;
    
	public CalcSocketServer(int port) {
		this.srvSocket = null;
		this.port      = port;
	}
	
	@Override
	public void interrupt() {
		try {
			if (srvSocket != null) srvSocket.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	@Override
	public void run() {
		if (port <= 0) {
			System.err.println("SocketServer listen port not specified!");
			System.exit(-1);
		}

		// TODO
		// Start listening server socket ..
		
        try
        {
        	srvSocket = new ServerSocket(port);
        	System.out.println("Server is waiting for connection.");
        	
        	while(true)
        	{   
        		Socket client = srvSocket.accept();
        		ClientServiceThread newThread =new ClientServiceThread (client);
        		newThread.run();
        		
        	}
        	
        }catch (Exception e)
    	{
    		e.printStackTrace();
    	}
	}
}
