package de.uni_stuttgart.ipvs.vs.ex6.replication;

import java.net.SocketException;
import java.util.ArrayList;
import java.util.List;

// !!! DO NOT EDIT !!!

public class Main {

	public static void main(String[] args) throws SocketException, QuorumNotReachedException {

		int n = 6; // number of replicas
		double[] availability = { 0.9, 0.9, 0.7, 0.7, 0.7, 0.3 }; // replicas have different availabilities...
		int[] votes = { 4, 4, 2, 2, 2, 1 }; // ... and different numbers of votes accordingly
		double x_init = 2.0; // all replica have the same initial value

		List<Replica<Double>> replicas = new ArrayList<Replica<Double>>(n);

		// create replicas
		for (int i = 0; i < n; i++) {
			Replica<Double> replica = new Replica<Double>(i, votes[i], availability[i], x_init);
			replica.start();
			replicas.add(replica);
		}

		// initialize replication manager
		WeightedVotingReplicationManager<Double> replicationManager = new WeightedVotingReplicationManager<Double>(
				replicas);

		// initialize clients
		Client<Double> client1 = new Client<Double>(replicationManager);
		Client<Double> client2 = new Client<Double>(replicationManager);

		try {

			double x = client1.get().getValue();
			System.out.println("Client 1 read x = " + x);

			double update = x + 2.0;
			client1.set(update);
			System.out.println("Client 1 wrote x = " + update);

			x = client2.get().getValue();
			System.out.println("Client 2 read x = " + x);

		} catch (Exception e) {
			System.err.println("Exception occured: " + e.getMessage());
			e.printStackTrace();
		} finally {
			System.exit(0);
		}

	}

}
