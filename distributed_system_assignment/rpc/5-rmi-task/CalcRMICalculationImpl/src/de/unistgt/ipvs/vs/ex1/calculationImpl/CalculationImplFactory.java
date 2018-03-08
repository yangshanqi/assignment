package de.unistgt.ipvs.vs.ex1.calculationImpl;
import java.rmi.RemoteException;

import de.unistgt.ipvs.vs.ex1.calculation.ICalculation;
import de.unistgt.ipvs.vs.ex1.calculation.ICalculationFactory;
/**
 * Change this class (implementation/signature/...) as necessary to complete the assignment.
 * You may also add some fields or methods.
 */
public class CalculationImplFactory implements ICalculationFactory {
	// TODO
	public ICalculation getSession() throws RemoteException
	{
		CalculationImpl calc = new CalculationImpl();
		return (ICalculation)calc;		
	}

}