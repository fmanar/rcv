'''Yay ranked choice voting!

But how to handle ties?
'''
def get_loser(contest):
    min_votes = None
    for option, votes in contest.items():
        if min_votes is None or len(votes) < min_votes:
            loser = option
            min_votes = len(votes)
    return loser

def cast_votes(contest, votes):
    for vote in votes:
        option = None
        while vote and option not in contest:
            option = vote.pop(0)
        if option in contest:
            contest[option].append(vote)

def print_contest(contest):
    for option, votes in contest.items():
        print(f"{option}: {len(votes)} votes")

def main():
    options = ["jim", "pam", "michael", "dwight"]
    votes = [
        ["dwight", "pam", "jim"],
        ["jim", "pam"],
        ["michael", "dwight", "jim", "pam"],
        ["jim", "michael", "dwight"],
        ["dwight", "michael", "pam", "jim"],
        ["pam"],
        ["pam", "jim", "dwight"],
        ["michael", "pam", "jim"],
        ["dwight"],
        ["dwight", "pam"],
        ["jim", "michael"],
        ["pam"]
    ]

    # create dictionary from options
    contest = {}
    for option in options:
        contest[option] = []
    
    # put votes in
    cast_votes(contest, votes)
    print_contest(contest)

    # ranked choice algorithm
    while len(contest) > 1:
        # drop lowest
        loser = get_loser(contest)
        print(f"dropping {loser}\n")

        # distribute votes
        cast_votes(contest, contest[loser])
        del contest[loser]
        print_contest(contest)

if __name__ == "__main__":
    main()