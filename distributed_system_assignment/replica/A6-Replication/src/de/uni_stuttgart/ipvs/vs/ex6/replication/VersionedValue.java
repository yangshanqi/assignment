package de.uni_stuttgart.ipvs.vs.ex6.replication;

import java.io.Serializable;

public class VersionedValue<T> implements Serializable {

	private static final long serialVersionUID = -8144267149616335154L;

	final protected int version;
	final protected T value;

	public VersionedValue(int version, T value) {
		this.version = version;
		this.value = value;
	}

	public VersionedValue(VersionedValue<T> other) {
		this.version = other.version;
		this.value = other.value;
	}

	public int getVersion() {
		return version;
	}

	public T getValue() {
		return value;
	}
}
