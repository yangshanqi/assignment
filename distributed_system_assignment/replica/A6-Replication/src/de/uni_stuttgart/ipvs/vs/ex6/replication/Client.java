package de.uni_stuttgart.ipvs.vs.ex6.replication;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.SocketAddress;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.Collection;

import de.uni_stuttgart.ipvs.vs.ex6.communication.MessageWithSource;
import de.uni_stuttgart.ipvs.vs.ex6.communication.NonBlockingReceiver;
import de.uni_stuttgart.ipvs.vs.ex6.communication.ReadLockRequest;
import de.uni_stuttgart.ipvs.vs.ex6.communication.ReadRequest;
import de.uni_stuttgart.ipvs.vs.ex6.communication.UnlockRequest;
import de.uni_stuttgart.ipvs.vs.ex6.communication.Util;
import de.uni_stuttgart.ipvs.vs.ex6.communication.ValueResponse;
import de.uni_stuttgart.ipvs.vs.ex6.communication.VoteResponse;
import de.uni_stuttgart.ipvs.vs.ex6.communication.WriteLockRequest;
import de.uni_stuttgart.ipvs.vs.ex6.communication.WriteRequest;

public class Client<T> {

	protected WeightedVotingReplicationManager<T> replicationManager;

	final static int TIMEOUT = 1000;

	protected DatagramSocket socket;
	protected NonBlockingReceiver receiver;

	public Client(WeightedVotingReplicationManager<T> replicationManager) throws SocketException {
		this.replicationManager = replicationManager;
		this.socket = new DatagramSocket();
		this.receiver = new NonBlockingReceiver(socket);
	}

	/**
	 * Send {@link ReadLockRequest}s to all replicas and check whether a read quorum
	 * is reached.
	 * 
	 * @return responses from read locked replicas (i.e., those that voted YES)
	 * @throws QuorumNotReachedException
	 *             if received positive votes add up to less than the read threshold
	 */
	protected Collection<MessageWithSource<VoteResponse>> requestReadLock() throws QuorumNotReachedException {

		Collection<MessageWithSource<VoteResponse>> responses = null;

		// send requests to all replicas
		try {

			for (SocketAddress replica : replicationManager.getReplicaAddresses()) {
				byte buf[] = Util.objectToByteArray(new ReadLockRequest());
				DatagramPacket request = new DatagramPacket(buf, buf.length, replica);
				//socket.connect(replica);
				socket.send(request);
			}

			// wait for responses
			responses = NonBlockingReceiver
					.<VoteResponse>unpack(receiver.receiveMessages(TIMEOUT, replicationManager.getNumberOfReplicas()));

			try {
				responses = replicationManager.checkReadQuorum(responses);
			} catch (QuorumNotReachedException e) {
				// release read locks
				releaseLock(e.getLockedNodes());
				throw e;
			}

		} catch (UnknownHostException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		}

		return responses;

	}

	/**
	 * TODO
	 * 
	 * Part e) Implement this method (required for {@link set})
	 * 
	 * Send {@link WriteLockRequest}s to all replicas and check whether a write
	 * quorum is reached.
	 * 
	 * @return responses from write locked replicas (i.e., those that voted YES)
	 * @throws QuorumNotReachedException
	 *             if received positive votes add up to less than the write
	 *             threshold
	 */
	protected Collection<MessageWithSource<VoteResponse>> requestWriteLock() throws QuorumNotReachedException {

		// TODO: complete this method!
		
		Collection<MessageWithSource<VoteResponse>> responses = null;
		// send requests to all replicas
		
		try {

			for (SocketAddress replica : replicationManager.getReplicaAddresses()) {
				byte buf[] = Util.objectToByteArray(new WriteLockRequest());
				DatagramPacket request = new DatagramPacket(buf, buf.length, replica);
				socket.send(request);
			}

			// wait for responses
			responses = NonBlockingReceiver
					.<VoteResponse>unpack(receiver.receiveMessages(TIMEOUT, replicationManager.getNumberOfReplicas()));

			try {
				responses = replicationManager.checkWriteQuorum(responses);
			} catch (QuorumNotReachedException e) {
				// release read locks
				releaseLock(e.getLockedNodes());
				throw e;
			}

		} catch (UnknownHostException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		}

		return responses;


	}

	/**
	 * Send {@link UnlockRequest}s to the given replicas
	 * 
	 * @param lockedReplicas
	 *            replicas on which a lock from this client should be released
	 */
	protected void releaseLock(Collection<SocketAddress> lockedReplicas) {
		try {

			for (SocketAddress replica : lockedReplicas) {
				byte buf[] = Util.objectToByteArray(new UnlockRequest());
				DatagramPacket request = new DatagramPacket(buf, buf.length, replica);
				socket.send(request);
			}

			// wait for acknowledgments
			receiver.receiveMessages(TIMEOUT, lockedReplicas.size());

		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	/**
	 * Send a {@link ReadRequest} to a chosen replica and return the value from the
	 * replica's reply
	 * 
	 * @param lockedReplica
	 *            the replica to be read from
	 * @return the value contained in the replica's {@link ValueResponse} message
	 */
	protected T readReplica(SocketAddress lockedReplica) {

		Collection<MessageWithSource<ValueResponse<T>>> responses;

		try {

			byte buf[] = Util.objectToByteArray(new ReadRequest());
			DatagramPacket request = new DatagramPacket(buf, buf.length, lockedReplica);
			socket.send(request);

			// wait for responses
			responses = NonBlockingReceiver.<ValueResponse<T>>unpack(receiver.receiveMessages(TIMEOUT, 1));

			return responses.iterator().next().getMessage().getValue();

		} catch (IOException e) {
			e.printStackTrace();
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		}

		return null;

	}

	/**
	 * TODO
	 * 
	 * Part e) Implement this method (required for {@link set})
	 * 
	 * Send a {@link WriteRequest} to a set of replicas
	 * 
	 * @param lockedReplicas
	 *            the replicas to be written to
	 * @param value
	 *            the value to be written
	 */
	protected void writeReplicas(Collection<SocketAddress> lockedReplicas, T value, int version) {

		// TODO: complete this method!
		
		
		try {

			byte buf[] = Util.objectToByteArray(new WriteRequest(version,value));
			
			// for those which agree writing, send them request
			for (SocketAddress lockedReplica:lockedReplicas)
			{
				DatagramPacket request = new DatagramPacket(buf, buf.length, lockedReplica);
				socket.send(request);

			}

		} catch (IOException e) {
			e.printStackTrace();
		}

	}

	/**
	 * TODO
	 * 
	 * Part d) Implement the get method to read the replicated value using the
	 * Weighted Voting protocol.
	 * 
	 * @return the value read according to the Weighted Voting protocol
	 * @throws QuorumNotReachedException
	 *             if a read quorum can not be reached
	 */
	public VersionedValue<T> get() throws QuorumNotReachedException {

		// TODO: complete this method!
		Collection<MessageWithSource<VoteResponse>> voted_quorum = null;
		int max_version = -1;
		MessageWithSource<VoteResponse> max_version_copy=null;
		Collection<SocketAddress> vote_yes_address = new ArrayList<SocketAddress> ();
		
		try
		{
			//read lock
			voted_quorum=requestReadLock();
		}
		catch (QuorumNotReachedException e)
		{
			System.out.println("The request for reading is failed");
			return null;
		}
		
		for (MessageWithSource<VoteResponse> vote_yes_node:voted_quorum)
		{
			//get the max version and its address
			vote_yes_address.add(vote_yes_node.getSource());
			if (vote_yes_node.getMessage().getVersion()>max_version)
			{
				max_version=vote_yes_node.getMessage().getVersion();
				max_version_copy = vote_yes_node;
			}
			//VersionedValue<T> read_value = (VersionedValue<T>) readReplica(vote_yes_node.getSource());
		}
		
		//read the max version's data 
		T latest_value = readReplica(max_version_copy.getSource()); 
		releaseLock(vote_yes_address);
		return (new VersionedValue(max_version,latest_value));

	}

	/**
	 * TODO
	 * 
	 * Part e) Implement the set method to write the replicated value using the
	 * Weighted Voting protocol.
	 * 
	 * @param value
	 *            the value to be written
	 * @throws QuorumNotReachedException
	 *             if a write quorum can not be reached
	 */
	public void set(T value) throws QuorumNotReachedException {

		// TODO: complete this method!
		Collection<MessageWithSource<VoteResponse>> voted_quorum = null;
		Collection<SocketAddress> vote_yes_address = new ArrayList<SocketAddress> ();
		int max_version = -1;
		//MessageWithSource<VoteResponse> max_version_copy=null;
		
		try
		{
			//write lock
			voted_quorum=requestWriteLock();
		}
		catch (QuorumNotReachedException e)
		{
			System.out.println("The request for writting is failed");
		}
		
		for (MessageWithSource<VoteResponse> vote_yes_node:voted_quorum)
		{
			//get the max version
			vote_yes_address.add(vote_yes_node.getSource());
			if (vote_yes_node.getMessage().getVersion()>max_version)
				max_version=vote_yes_node.getMessage().getVersion();
			//	max_version_copy = vote_yes_node;		
			//VersionedValue<T> read_value = (VersionedValue<T>) readReplica(vote_yes_node.getSource());
		}
		//update the max version and write to all who agree
		max_version++;
		
		writeReplicas(vote_yes_address,value,max_version);
		
		releaseLock(vote_yes_address);

	}

}
