package de.uni_stuttgart.ipvs.vs.ex6.communication;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.DatagramPacket;

public class Util {

	/**
	 * Serialize an Object to a byte array for transmission
	 * 
	 * @param object Object instance to be serialized
	 * @return byte array of serialized object
	 * @throws IOException
	 */
	public static byte[] objectToByteArray(Object object) throws IOException {
		ByteArrayOutputStream baos = new ByteArrayOutputStream(4096);
		ObjectOutputStream oosOut = new ObjectOutputStream(baos);
		oosOut.writeObject(object);
		oosOut.close();
		return baos.toByteArray();
	}

	/**
	 * Deserialize an Object from a DatagramPacket's payload
	 * 
	 * @param packet DatagramPacket containing the serialized Object
	 * @return deserialized Object
	 * @throws IOException
	 * @throws ClassNotFoundException
	 */
	public static Object datagramPacketToObject(DatagramPacket packet) throws IOException, ClassNotFoundException {
		ByteArrayInputStream bais = new ByteArrayInputStream(packet.getData(), packet.getOffset(), packet.getLength());
		ObjectInputStream oisIn = new ObjectInputStream(bais);
		Object receivedObject = oisIn.readObject();
		return receivedObject;
	}

}
