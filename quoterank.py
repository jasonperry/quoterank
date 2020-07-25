#!/usr/bin/env python3

import os

class ScoredQuote:
    def __init__(self, quote, author, votes):
        self.quote = quote
        self.author = author
        self.votes = votes
        self.score = sum(votes) # may change

    def add_vote(self, val):
        self.votes.append(val)
        self.score = sum(self.votes)

# end class ScoredQuote


class QuoteDB:
    def __init__(self, dbfile):
        self.maxscore = 0
        self.quotes = []
        if os.path.isfile(dbfile):
            self._readdb(dbfile)
        else:
            self._initdb(dbfile)
        self.length = len(self.quotes)

    def _initdb(self, filepath):
        f = open(filepath, 'w')
        f.close()
        print("Initialized empty database at " + filepath)

    def _readdb(self, filepath):
        # returns total, (quote, votelist) list
        f = open(filepath, 'r')
        count = 0
        while True:
            quoteline = f.readline()
            if not quoteline:
                break
            quote = quoteline.strip()
            author = f.readline().strip()
            voteline = f.readline().strip()
            votes = [ int(v) for v in voteline.split(',') ]
            self.quotes.append(ScoredQuote(quote, author, votes))
            count += 1
        f.close()
        self.quotes = sorted(self.quotes, key=lambda q: q.score, reverse=True)
        self.maxscore = sum(self.quotes[0].votes)
        print(f"Read {count} quotes from db file.")

    def writedb(self, filepath):
        f = open(filepath, 'w')
        for q in self.quotes:
            f.write(q.quote + "\n")
            f.write(q.author + "\n")
            # hack to get just the comma-separated list.
            f.write(str(q.votes)[1:-1] + "\n")
            f.close()
    
    def print_quotes(self, n = None):
        # "or" doesn't work here because 0 is false.
        n = len(self.quotes) if n == None else n
        print("-"*70)
        for i in range(n):
            q = self.quotes[i]
            print(f"#{i+1} (score={q.score}).\n{q.quote}\n -- {q.author}")
            print("-"*70 + "\n")

    def add_vote_interactive(self):
        print("Enter quote number to vote up:")
        index = int(input())
        self.quotes[index-1].add_vote(self.maxscore+1)
        self.maxscore = sum(self.quotes[index-1].votes)
        self.quotes = sorted(self.quotes, key=lambda q: q.score, reverse=True)
    
    def add_quote_interactive(self):
        print("Enter quote:")
        quote = input()
        print("Enter author:")
        author = input()
        print("Vote for it? [y/n]: ", end="")
        votestr = input()
        votes = []
        if votestr == 'y':
            votes.append(self.maxscore+1)
            self.maxscore += 1
            print(f"New quote gets score: {votetot}")
        self.quotes.append(ScoredQuote(quote, author, votes))
        self.quotes = sorted(self.quotes, key=lambda q: q.score, reverse=True)

# end class QuoteDB


def menu():
    print("----------------------------")
    print("1) Enter a new quote")
    print("2) See all quotes")
    print("3) See top n quotes")
    print("4) Vote up a quote")
    print("5) Search quotes")
    print("6) Write updated DB and quit")
    print("----------------------------")
    print("Choice: ", end='')
    choice = int(input())
    return choice


if __name__ == "__main__":
    dbfile = "./quotedb.txt"
    qdb = QuoteDB(dbfile)
    if qdb.length > 0:
        qdb.print_quotes(1)
    choice = menu()
    while choice != 6:
        if choice == 1:
            qdb.add_quote_interactive()
        elif choice == 2:
            qdb.print_quotes()
        elif choice == 3:
            print("Enter number of top quotes to display:", end="")
            n = int(input())
            qdb.print_quotes(n)
        elif choice == 4:
            qdb.add_vote_interactive()
        choice = menu()
    qdb.writedb(dbfile)
