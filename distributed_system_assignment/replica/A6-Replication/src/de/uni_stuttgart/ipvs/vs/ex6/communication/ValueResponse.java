package de.uni_stuttgart.ipvs.vs.ex6.communication;

public class ValueResponse<T> extends Message {

	private static final long serialVersionUID = -2206514474206726748L;

	final protected T value;

	public ValueResponse(T value) {
		this.value = value;
	}

	public T getValue() {
		return value;
	}

}
