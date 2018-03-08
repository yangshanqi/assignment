package de.unistgt.ipvs.vs.ex1.calcRMIclient;

import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.Collection;
import java.util.Iterator;
import java.util.regex.Pattern;
import java.util.regex.Matcher;


import de.unistgt.ipvs.vs.ex1.calculation.ICalculation;
import de.unistgt.ipvs.vs.ex1.calculation.ICalculationFactory;

/**
 * Implement the getCalcRes-, init-, and calculate-method of this class as
 * necessary to complete the assignment. You may also add some fields or methods.
 */
public class CalcRmiClient {
	private ICalculation calc = null;
	private Registry registry;
	private ICalculationFactory  calcFactory;
	private int result;

	public CalcRmiClient() {
		this.calc = null;
		this.result = 0;
	}

	public int getCalcRes() {
		// TODO
		try {
			result = calc.getResult();
		}catch(RemoteException e) {
			e.printStackTrace();
		}
		return result;
	}

	public boolean init(String url) {
		// TODO
		try {
			
		    //get the host and object			
			String[] getSplit = url.split("/+");
			String host = getSplit[1];
			String obj = getSplit[2];
			System.out.println(obj);			
			registry = LocateRegistry.getRegistry(host);  
			calcFactory = (ICalculationFactory) registry.lookup(obj);
			calc = calcFactory.getSession();
			
	    }catch (RemoteException e) {
			e.printStackTrace();
		}catch (NotBoundException e) {
			e.printStackTrace();
		}
		return false;
	};

	public boolean calculate(CalculationMode calcMode, Collection<Integer> numbers) {
		// TODO
		Iterator it = numbers.iterator();
		if (calcMode == CalculationMode.ADD) {
			while (it.hasNext()) {
				try {
					int num =(Integer)it.next();
					calc.add(num);
				}catch(RemoteException e) {
					e.printStackTrace();
				}
			}
		}
		else if (calcMode == CalculationMode.SUB) {
			while (it.hasNext()) {
				try {
					int num =(Integer)it.next();
					calc.subtract(num);
				}catch(RemoteException e) {
					e.printStackTrace();
				}
			}
		}
		else if (calcMode == CalculationMode.MUL) {
			while (it.hasNext()) {
				try {
					int num =(Integer)it.next();
					calc.multiply(num);
				}catch(RemoteException e) {
					e.printStackTrace();
				}
			}
		}
		
		return false;
	}
}
