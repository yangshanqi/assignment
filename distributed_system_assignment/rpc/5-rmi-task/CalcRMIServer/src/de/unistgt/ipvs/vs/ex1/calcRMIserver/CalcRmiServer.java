package de.unistgt.ipvs.vs.ex1.calcRMIserver;

import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;

import de.unistgt.ipvs.vs.ex1.calculationImpl.CalculationImplFactory;
import de.unistgt.ipvs.vs.ex1.calculation.ICalculationFactory;
/**
 * Implement the run-method of this class to complete
 * the assignment. You may also add some fields or methods.
 */
public class CalcRmiServer extends Thread {
	private String regHost;
	private String objName;
	private Registry registry;
	
	public CalcRmiServer(String regHost, String objName) {
		this.regHost = regHost;
		this.objName = objName;	
	}
	
	@Override
	public void run() {
		if (regHost == null || objName == null) {
			System.err.println("<registryHost> and/or <objectName> not set!");
			return;
		}
		
		// TODO
		
		try {
			
			CalculationImplFactory calcImplFactory = new CalculationImplFactory();
			ICalculationFactory stub = (ICalculationFactory) UnicastRemoteObject.exportObject(calcImplFactory,0);
			registry = LocateRegistry.createRegistry(1111);
			registry.rebind(objName, stub);
			System.out.println("The server has registered successfully");
		}catch(RemoteException e){
			e.printStackTrace();
		}
	}

}
