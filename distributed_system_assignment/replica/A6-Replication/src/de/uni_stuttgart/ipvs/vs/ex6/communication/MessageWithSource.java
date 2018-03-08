package de.uni_stuttgart.ipvs.vs.ex6.communication;

import java.net.SocketAddress;
import java.util.Collection;
import java.util.Vector;

/**
 * Convenience wrapper for message of type T with associated source address
 *
 * @param <T> type of contained message
 */
public class MessageWithSource<T> {

	final T message;
	final SocketAddress source;

	public MessageWithSource(SocketAddress source, T message) {
		this.source = source;
		this.message = message;
	}

	/**
	 * @return the contained message
	 */
	public T getMessage() {
		return message;
	}

	/**
	 * @return the message sender's SocketAddress
	 */
	public SocketAddress getSource() {
		return source;
	}

	/**
	 * Extract the set of SourceAddresses from a set of MessageWithSource objects
	 * 
	 * @param messagesWithSources set of MessageWithSource instances
	 * @return Collection of SocketAddresses containing the message sources
	 */
	public static <T> Collection<SocketAddress> getSources(
			Collection<MessageWithSource<T>> messagesWithSources) {
		if (messagesWithSources == null)
			return null;

		Collection<SocketAddress> sources = new Vector<SocketAddress>(messagesWithSources.size());
		for (MessageWithSource<T> messageWithSource : messagesWithSources)
			sources.add(messageWithSource.getSource());
		
		return sources;
	}

}
