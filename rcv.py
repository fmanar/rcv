'''Yay ranked choice voting!

But how to handle ties?

Change votes to an object.
'''
from collections import OrderedDict

class Vote:
    def __init__(self, name, rank):
        self.name = name
        self.rank = rank
        self.index = 0

    def get_candidate(self):
        '''Get candidate (candidate/contest pool key).'''
        if self.index is None:
            return None
        else:
            return self.rank[self.index]
    
    def incr_candidate(self):
        '''Move to the next candidate.'''
        self.index += 1
        if self.index == len(self.rank):
            self.index = None

class Contest:
    '''Keep candidates in ordered dict, sorted on vote count.
    
    Dict key is candidate.
    Dict value is list of vote. 

    '''
    def __init__(self, candidates, verbose=False):
        self.pool = OrderedDict()
        for candidate in candidates:
            self.pool[candidate] = []
            if verbose:
                print(f"Candidate {candidate} created")

    def cast_votes(self, votes, verbose=False):
        '''Assign votes.

        For each vote, if the current candidate isn't in the pool, increments
        the vote until the candidate is in the pool or the vote is exhausted.
        Finally, sort pool.

        Args:
            votes (list of Vote): the input votes

        '''
        # process each vote
        for vote in votes:
            candidate = vote.get_candidate()
            # make sure candidate is in pool
            while candidate and candidate not in self.pool:
                vote.incr_candidate()
                candidate = vote.get_candidate()
            # add vote to this candidates list
            if candidate:
                if verbose:
                    print(f"Vote {vote.name} cast on {candidate}")
                self.pool[candidate].append(vote)
            elif verbose:
                print(f"Vote {vote.name} exhausted")
        # sort pool
        self.pool = OrderedDict(sorted(self.pool.items(), key=lambda item: len(item[1]), reverse=True))

    def get_losers(self, verbose=False):
        '''Return lowest candidates.

        Probably one lowest candidate, but on tie return everyone in tie.

        Args:
            verbose (bool): print out losers

        Returns:
            (list of str): loser candidates (keys in self.pool)

        '''
        losers = []
        min_votes = None
        for candidate, votes in reversed(self.pool.items()):
            if min_votes is None:
                min_votes = len(votes)
            elif len(votes) > min_votes:
                break
            losers.append(candidate)
            if verbose:
                print(f"Candidate {candidate} loses")
        return losers

    def elect(self, votes, verbose=False):
        self.cast_votes(votes, verbose)
        if verbose:
            print(f"\nTallies:\n{self}")
        while len(self.pool) > 1:
            losers = self.get_losers(verbose=verbose)
            if len(losers) == len(self.pool):
                break
            votes = []
            for loser in losers:
                votes += self.pool.pop(loser)
            self.cast_votes(votes, verbose)
            if verbose:
                print(f"\nTallies:\n{self}")
        winners = list(self.pool.keys())
        if verbose and len(winners) > 1:
            string = "Tie between"
            for candidate in winners:
                string += f" {candidate}" 
            print(string)
        elif verbose:
            print(f"{winners[0]} wins!")
        return winners
        
    def __str__(self):
        string = ""
        for candidate, votes in self.pool.items():
            string += f"{candidate}: {len(votes)}\n"
        return string

def main():
    data = {
        "candidates": ["jim", "pam", "michael", "dwight"],
        "votes": [
            {"name": "a", "rank": ["dwight", "pam", "jim"]},
            {"name": "b", "rank": ["jim", "pam"]},
            {"name": "c", "rank": ["michael", "dwight", "jim", "pam"]},
            {"name": "d", "rank": ["jim", "michael", "dwight"]},
            {"name": "e", "rank": ["dwight", "michael", "pam", "jim"]},
            {"name": "f", "rank": ["pam"]},
            {"name": "g", "rank": ["pam", "jim", "dwight"]},
            {"name": "h", "rank": ["michael", "pam", "jim"]},
            {"name": "i", "rank": ["dwight"]},
            {"name": "j", "rank": ["dwight", "pam"]},
            {"name": "k", "rank": ["jim", "michael"]},
            {"name": "l", "rank": ["pam"]},
            {"name": "m", "rank": ["michael", "pam"]},
            {"name": "n", "rank": ["jim", "dwight"]},
        ],
    }

    # contest and votes list
    contest = Contest(data["candidates"], verbose=True)

    # extract and cast votes
    votes = []
    for vote_dict in data["votes"]:
        votes.append(Vote(**vote_dict))
    contest.elect(votes, verbose=True)

    # print out what candidate each person got
    print("\nVote final casting:")
    for vote in votes:
        if vote.index is None:
            print(f"Vote {vote.name} was exhausted")
        else:
            print(f"Vote {vote.name} got index {vote.index}")

if __name__ == "__main__":
    main()