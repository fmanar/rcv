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

    def get_choice(self):
        '''Get choice (candidate/contest pool key).'''
        if self.index is None:
            return None
        else:
            return self.rank[self.index]
    
    def incr_choice(self):
        '''Move to the next choice.'''
        self.index += 1
        if self.index == len(self.rank):
            self.index = None

class Contest:
    '''Keep candidates in ordered dict, sorted on vote count.
    
    Dict key is candidate.
    Dict value is list of vote. 

    '''
    def __init__(self, candidates):
        self.pool = OrderedDict()
        for key in candidates:
            self.pool[key] = []

    def cast_votes(self, votes, verbose=False):
        '''Assign votes.

        For each vote, if the current choice isn't in the pool, increments
        the vote until the choice is in the pool or the vote is exhausted.
        Finally, sort pool.

        Args:
            votes (list of Vote): the input votes

        '''
        # process each vote
        for vote in votes:
            choice = vote.get_choice()
            # make sure choice is in pool
            while choice and choice not in self.pool:
                vote.incr_choice()
                choice = vote.get_choice()
            # add vote to this candidates list
            if choice:
                if verbose:
                    print(f"Vote {vote.name} cast on {choice}")
                self.pool[choice].append(vote)
            elif verbose:
                print(f"Vote {vote.name} exhausted")
        # sort pool
        self.pool = OrderedDict(sorted(self.pool.items(), key=lambda item: len(item[1]), reverse=True))

    def drop_losers(self, verbose=False):
        '''Remove lowest candidates.

        Probably one lowest candidate, but on tie drop everyone.

        Args:
            verbose (bool): print out who is being dropped

        Returns:
            (list of Vote): votes of the dropped candidates

        '''
        dropped_candidates = []
        min_votes = None
        for candidate, votes in reversed(self.pool.items()):
            if min_votes is None:
                min_votes = len(votes)
            elif len(votes) > min_votes:
                break
            dropped_candidates.append(candidate)
        dropped_votes = []
        for candidate in dropped_candidates:
            dropped_votes += self.pool[candidate]
            del self.pool[candidate]
            if verbose:
                print(f"Eliminating {candidate}")
        return dropped_votes

    def elect(self, votes, verbose=False):
        self.cast_votes(votes, verbose)
        if verbose:
            print(f"{self}")
        while len(self.pool) > 1:
            votes = self.drop_losers(verbose=verbose)

            self.cast_votes(votes, verbose)
            if verbose:
                print(f"{self}")
        winner = next(iter(self.pool))
        if verbose:
            print(f"{winner} wins!")
        return winner
        
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
    contest = Contest(data["candidates"])

    # extract and cast votes
    votes = []
    for vote_dict in data["votes"]:
        votes.append(Vote(**vote_dict))
    contest.elect(votes, verbose=True)

    # print out what choice each person got
    print("\nVote final casting:")
    for vote in votes:
        if vote.index is None:
            print(f"vote {vote.name} was exhausted")
        else:
            print(f"vote {vote.name} got choice {vote.index}")

if __name__ == "__main__":
    main()