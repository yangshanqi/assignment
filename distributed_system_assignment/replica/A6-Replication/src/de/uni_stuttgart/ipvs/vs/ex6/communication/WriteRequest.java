package de.uni_stuttgart.ipvs.vs.ex6.communication;

import de.uni_stuttgart.ipvs.vs.ex6.replication.VersionedValue;

public class WriteRequest<T> extends Message {

	private static final long serialVersionUID = -6775582881163280754L;

	final protected VersionedValue<T> versionedValue;

	public WriteRequest(VersionedValue<T> versionedValue) {
		this.versionedValue = versionedValue;
	}

	public WriteRequest(int version, T value) {
		this.versionedValue = new VersionedValue<T>(version, value);
	}

	public VersionedValue<T> getVersionedValue() {
		return versionedValue;
	}



}
