package de.unistgt.ipvs.vs.ex4.distributed_debugging_algorithm;

//you are not allowed to change this class structure
public class VectorClock {

	protected int[] vectorClock;
	private int processId;
	private int numberOfProcesses;

	public VectorClock(int processId, int numberOfProcesses) {
		vectorClock = new int[numberOfProcesses];
		this.numberOfProcesses = numberOfProcesses;
		this.processId = processId;
	}

	VectorClock(VectorClock other) {
		vectorClock = other.vectorClock.clone();
		processId = other.processId;
		numberOfProcesses = other.numberOfProcesses;

	}

	public void increment() {
		// TODO
		/*
		 * Complete a code to increment the local clock component  
		 */
		this.vectorClock[this.processId]=this.vectorClock[this.processId]+1;

	}

	public int[] get() {
		// TODO 
		// Complete a code to return the vectorClock value
		return this.vectorClock;

	}

	public void update(VectorClock other) {
		// TODO
		/*
		 * Implement Supermum operation
		 */
		System.out.println("other vetorclock:"+other.vectorClock+"  this vectorclock"+this.vectorClock);
		for (int i=0; i<vectorClock.length; i++)
		{
			{if (other.vectorClock[i]>this.vectorClock[i])
				this.vectorClock[i] = other.vectorClock[i];}
		}
		System.out.println("other vetorclock:"+other.vectorClock+"  this vectorclock"+this.vectorClock);

	}

	public boolean checkConsistency(int otherProcessId, VectorClock other) {
		//TODO
		/*
		 * Implement a code to check if a state is consist regarding two vector clocks (i.e. this and other). 
		 * See slide 41 from global state lecture.
		 */
		if (other.vectorClock[this.processId]>this.vectorClock[this.processId])
			return false;
		if (this.vectorClock[otherProcessId]>other.vectorClock[otherProcessId])
			return false;
		return true;

		
	}

}
