'''Yay ranked choice voting!

'''

class Vote:
    def __init__(self, name, rank_list, choice=0):
        self.name = name
        self.rank_list = rank_list
        self.choice = choice

    def get_option_name(self):
        if self.choice is None:
            return None
        else:
            return self.rank_list[self.choice]

    def increment_choice(self, option_names=None):
        if self.choice is not None:
            self.choice += 1
        if self.choice == len(self.rank_list):
            self.choice = None

    def __repr__(self):
        return f"Vote({self.name}, {self.rank_list}, {self.choice})"


class Option:
    def __init__(self, name, votes=None):
        self.name = name
        if votes is None:
            self.votes = []
        else:
            self.votes = votes

    def get_num_votes(self):
        return(len(self.votes))

    def __lt__(self, other):
        return len(self.votes) < len(other.votes)

    def __repr__(self):
        return f"Option({self.name}, {self.votes})"

class Contest:
    '''Maintains options as a sorted list and dictionary.

    Also tracks votes and ensures votes are only cast once.

    '''
    def __init__(self, options, votes=None):
        self._options_list = options
        self._options_dict = {}
        for opt in options:
            self._options_dict[opt.name] = opt
        self._options_list.sort(reverse=True)
        self._votes = {}
        if votes:
            self.assign_votes(votes)

    def assign_votes(self, votes):
        for vote in iter(votes):
            key = vote.get_option_name()
            if vote in self._votes:
                raise ValueError("Vote already cast.")
            elif key in self._options_dict:
                self._votes[vote.name] = vote
                self._options_dict[key].votes.append(vote)
        self._options_list.sort(reverse=True)

    def get_num_votes(self):
        return len(self._votes)

    def get_leader(self):
        return self._options_list[0]

    def pop(self):
        '''Pop lowest option out of contest.
        
        '''
        option = self._options_list.pop()
        self._options_dict.pop(option.name)
        for vote in option.votes:
            self._votes.pop(vote.name)
        return option

    def __str__(self):
        string = ""
        for option in self._options_list:
            string += f"{option.name}: {option.get_num_votes()}\n"
        return string

    def __repr__(self):
        return f"Contest({self._options_list}, {self._votes})"

def main():
    options = [
        Option("Jim"),
        Option("Pam"),
        Option("Michael"),
        Option("Dwight"),
    ]
    votes = [
        Vote("Field", ["Dwight", "Pam", "Jim"]),
        Vote("Aditi", ["Jim", "Pam"]),
        Vote("Peter", ["Michael", "Dwight", "Jim", "Pam"]),
        Vote("Natalie", ["Jim", "Michael", "Dwight"]),
        Vote("Owen", ["Dwight", "Michael", "Pam", "Jim"]),
        Vote("Haley", ["Pam"]),
        Vote("Kristen", ["Pam", "Jim", "Dwight"]),
        Vote("Sam", ["Michael", "Pam", "Jim"]),
        Vote("Stacy", ["Dwight"]),
    ]

    contest = Contest(options, votes)
    print(f"{contest}")

    # ranked choice algorithm
    while contest.get_leader().get_num_votes() <= contest.get_num_votes() // 2:
        # drop lowest
        last = contest.pop()

        # distribute votes
        for vote in last.votes:
            vote.increment_choice(contest)

        contest.assign_votes(last.votes)
        print(f"{contest}")




if __name__ == "__main__":
    main()