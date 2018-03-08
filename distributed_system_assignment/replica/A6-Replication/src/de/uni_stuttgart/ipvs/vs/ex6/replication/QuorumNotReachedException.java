package de.uni_stuttgart.ipvs.vs.ex6.replication;

import java.net.SocketAddress;
import java.util.Collection;
import java.util.Collections;

public class QuorumNotReachedException extends Exception {

	private static final long serialVersionUID = -4478852665389008679L;

	final protected int threshold;
	final protected int achievedVotes;
	final protected Collection<SocketAddress> lockedNodes;

	/**
	 * @param threshold
	 *            required number of positive votes
	 * @param achievedVotes
	 *            achieved number of positive votes
	 * @param lockedNodes
	 *            {@link SocketAddress}es of the locked replicas (i.e., those that
	 *            voted YES)
	 */
	public QuorumNotReachedException(int threshold, int achievedVotes, Collection<SocketAddress> lockedNodes) {
		super("Received " + achievedVotes + " positive votes from " + lockedNodes.size() + " nodes, but at least "
				+ threshold + " were needed.");
		this.threshold = threshold;
		this.achievedVotes = achievedVotes;
		this.lockedNodes = Collections.unmodifiableCollection(lockedNodes);
	}

	public int getThreshold() {
		return threshold;
	}

	public int getAchievedVotes() {
		return achievedVotes;
	}

	public Collection<SocketAddress> getLockedNodes() {
		return lockedNodes;
	}

}
