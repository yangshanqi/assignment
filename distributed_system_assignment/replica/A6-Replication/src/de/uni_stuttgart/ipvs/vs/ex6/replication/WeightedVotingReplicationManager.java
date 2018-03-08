package de.uni_stuttgart.ipvs.vs.ex6.replication;

import java.net.SocketAddress;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Vector;

import de.uni_stuttgart.ipvs.vs.ex6.communication.MessageWithSource;
import de.uni_stuttgart.ipvs.vs.ex6.communication.VoteResponse;
import de.uni_stuttgart.ipvs.vs.ex6.communication.VoteResponse.Vote;

public class WeightedVotingReplicationManager<T> {

	protected Collection<Replica<T>> replicas;
	protected Collection<SocketAddress> replicaAddresses;

	protected int readThreshold;
	protected int writeThreshold;

	/**
	 * TODO
	 * 
	 * Part a) Complete the constructor by initializing read and write thresholds.
	 * You may choose arbitrary values as long as they satisfy the conditions for
	 * Weighted Voting.
	 * 
	 * Construct a WeightedVotingReplicationManager, determine read and write
	 * thresholds based on provided replicas and their numbers of votes
	 * 
	 * @param replicas
	 *            the set of replicas to manage for a given replicated value
	 */
	public WeightedVotingReplicationManager(Collection<Replica<T>> replicas) {
		this.replicas = replicas;

		replicaAddresses = new Vector<SocketAddress>(replicas.size());
		for (Replica<T> replica : replicas)
			replicaAddresses.add(replica.getSocketAddress());

		// TODO: complete this method!
		int total_q = 0;
		for (Replica<T> replica : replicas)
		{
			total_q = total_q+replica.getVotes();
		}
		
		if (total_q%2==0)
		{
			writeThreshold= total_q/2+1;
			readThreshold=total_q/2;
		}
		else
		{
			writeThreshold = (int)Math.ceil(total_q/2);
			readThreshold = writeThreshold;
		}
		System.out.println("writeThreshold:"+writeThreshold);
		System.out.println("readThreshold:"+readThreshold);

	}

	/**
	 * @return unmodifiable view on the SocketAddresses of all replica
	 */
	public Collection<SocketAddress> getReplicaAddresses() {
		return Collections.unmodifiableCollection(replicaAddresses);
	}

	/**
	 * @return number of managed replicas
	 */
	public int getNumberOfReplicas() {
		return replicas.size();
	}

	public int getReadThreshold() {
		return readThreshold;
	}

	public int getWriteThreshold() {
		return writeThreshold;
	}

	/**
	 * TODO
	 * 
	 * Part a) Implement the method checkQuorum to check whether a sufficient number
	 * of positive votes were received. If a sufficient number was received, this
	 * method should return the replies from the locked replicas (i.e., those that
	 * voted YES). Otherwise, a {@link QuorumNotReachedException} must be thrown.
	 * 
	 * This method is used by {@link checkReadQuorum} and {@link checkWriteQuorum}.
	 * 
	 * @throws QuorumNotReachedException
	 * @param replies
	 *            collection of received {@link VoteResponse} messages (wrapped in
	 *            {@link MessageWithSource})
	 * @param threshold
	 *            number of votes that are required to reach the quorum
	 */
	protected Collection<MessageWithSource<VoteResponse>> checkQuorum(
			Collection<MessageWithSource<VoteResponse>> replies, int threshold) throws QuorumNotReachedException {

		// TODO: complete this method!
		Collection<MessageWithSource<VoteResponse>> vote_yes_group = new ArrayList<MessageWithSource<VoteResponse>> ();
		Collection<SocketAddress> vote_yes_address = new ArrayList<SocketAddress> ();
		int achievedVotes=0;
		
		//SocketAddress temp_address=null;
		for (MessageWithSource<VoteResponse> temp_physical: replies)
		{
			VoteResponse temp_response= temp_physical.getMessage();
			if (temp_response.getState().equals(Vote.YES))
			{
				//for keep the address and counting the achieved votes 
				//if it is necessary to raise exception
				//temp_address=temp_physical.getSource();
				vote_yes_address.add(temp_physical.getSource());
				
				vote_yes_group.add(temp_physical);
				achievedVotes=achievedVotes+temp_response.getVotes();				
			}
		}
		if (achievedVotes>=threshold){
			return vote_yes_group;
		}
		else
		{
			throw new QuorumNotReachedException(threshold,achievedVotes,vote_yes_address);
		}


	}

	// Uses checkQuorum to compare received positive votes against readThreshold
	public Collection<MessageWithSource<VoteResponse>> checkReadQuorum(
			Collection<MessageWithSource<VoteResponse>> replies) throws QuorumNotReachedException {
		return checkQuorum(replies, readThreshold);
	}

	// Uses checkQuorum to compare received positive votes against writeThreshold
	public Collection<MessageWithSource<VoteResponse>> checkWriteQuorum(
			Collection<MessageWithSource<VoteResponse>> replies) throws QuorumNotReachedException {
		return checkQuorum(replies, writeThreshold);
	}

}
