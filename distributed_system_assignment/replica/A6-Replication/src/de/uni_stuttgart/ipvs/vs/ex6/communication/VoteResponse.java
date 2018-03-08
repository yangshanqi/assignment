package de.uni_stuttgart.ipvs.vs.ex6.communication;

public class VoteResponse extends Message {

	private static final long serialVersionUID = 5733333023880711578L;

	public enum Vote {
		YES, NO
	};

	final protected Vote vote;
	final protected int version;
	final protected int nVotes;

	public Vote getState() {
		return vote;
	}

	public int getVersion() {
		return version;
	}

	public int getVotes() {
		return nVotes;
	}

	public VoteResponse(Vote vote, int version, int nVotes) {
		this.vote = vote;
		this.version = version;
		this.nVotes = nVotes;
	}

}
