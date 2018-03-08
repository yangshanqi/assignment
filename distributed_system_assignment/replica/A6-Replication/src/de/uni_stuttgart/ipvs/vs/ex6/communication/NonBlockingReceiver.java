package de.uni_stuttgart.ipvs.vs.ex6.communication;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.SocketAddress;
import java.net.SocketException;
import java.net.SocketTimeoutException;
import java.util.Collection;
import java.util.Vector;

/**
 * Convenience class for receiving multiple messages within a timeout interval.
 * Messages not arriving before the timeout are assumed to be lost or
 * originating from a crashed node.
 */
public class NonBlockingReceiver {

	protected DatagramSocket socket;

	public NonBlockingReceiver(DatagramSocket socket) {
		this.socket = socket;
	}

	/**
	 * TODO
	 * 
	 * Part c) Extend the method receiveMessages to return all DatagramPackets that
	 * were received during the given timeout period or until the number of
	 * expectedMessages were received, whichever condition is met first.
	 * 
	 * Hints: you can use DatagramSocket.setSoTimeout() to set a timeout on receive
	 * operations, and catch a SocketTimeoutException to detect a timeout. Note that
	 * the method should return after timeoutMillis at the latest, regardless of how
	 * many messages arrive and when. Socket timeouts can be cancelled by calling
	 * setSoTimeout(0).
	 * 
	 * @param timeoutMillis
	 *            timeout in milliseconds
	 * @param expectedMessages
	 *            maximum number of messages to receive
	 * @return received DatagramPackets
	 * @throws IOException
	 */
	public Vector<DatagramPacket> receiveMessages(int timeoutMillis, int expectedMessages) throws IOException {
		//long now = System.currentTimeMillis();
		//long endTime = now + timeoutMillis;
		
			
		Vector<DatagramPacket> received_messages = new Vector<DatagramPacket>();	
		
		try
		{
			socket.setSoTimeout(timeoutMillis);
			for(int count=0;count<=expectedMessages;count++)
			{
				byte buf[] = new byte[4096]; 
				DatagramPacket inPacket = new DatagramPacket(buf,buf.length);	
				socket.receive(inPacket);
				received_messages.add(inPacket);
			}
			// If there are enough messsages got, just return.
			return received_messages;
		}
		catch (SocketTimeoutException e)
		{
			return received_messages;
		}

		// TODO: complete this method!
		 
	}

	/**
	 * Convert a set of DatagramPackets to a set of MessageWithSource instances
	 * containing the packets' payloads and sources
	 * 
	 * @param datagrams
	 *            DatagramPackets to extract payloads and sources from
	 * @return MessageWithSources with corresponding payloads and sources
	 * @throws IOException
	 * @throws ClassNotFoundException
	 */
	public static <T> Collection<MessageWithSource<T>> unpack(Collection<DatagramPacket> datagrams)
			throws IOException, ClassNotFoundException {

		Vector<MessageWithSource<T>> messages = new Vector<MessageWithSource<T>>(datagrams.size());

		for (DatagramPacket datagram : datagrams) {
			SocketAddress source = datagram.getSocketAddress();

			@SuppressWarnings("unchecked")
			T value = (T) Util.datagramPacketToObject(datagram);

			MessageWithSource<T> message = new MessageWithSource<T>(source, value);
			messages.add(message);
		}

		return messages;
	}

}
