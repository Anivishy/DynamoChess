its about time i organize my thoughts

important things are **bolded**

i've tried two very distinct approaches to this so far

##### **supervised learning**

so first i filtered the dataset based on elo and trained a value function which needs to predict who will win given a position
1.0 = white wins, -1.0 black wins, 0.0 draw

training a model on 2200 elo games (16000 of them) :
i noticed the value of each position resulting from all legal moves from a position are very similar
bad positions do not have worse values than the actual move played most of the time

this could be because the people try to play optimal moves
moves that are obviously bad to people wouldn't be represented in the dataset
since the targets are based on the GAMES result, there may not be enough meaningful data in just 16000 games
maybe thats why online sources use LOTS of DATA to utilize the assumption that objectively better positions should in general win more

**current ideas / things to try**
the ultimate solution needs to work well with low compute and not too much time

1
i wonder if i can filter games by an elo GAP. if there is a big enough elo gap then the better moves should be more clear
and result in more wins

2
i could use some heuristics as more inputs as well
first get the model to play like the data? value of 1 for moves made in data, -1 for nonmoves

4
try training a policy network instead of value network - or a value network that values moves not positions

5
input previous board as well?

6
preprocess the data by finding the move distribution of each position. only the move that is played the most should be counted
as a positive target. the rest should be negative. that way i dont need to create more data in real-time

7
flip the board so that the model needs to only learn from whites perspective

**next "big" method to try**
iterate through every game and move and build probability distribution of moves from each unique state.
train model on the probability of each legal move being played for each position from the dataset
this should be much faster as it cuts down the data while still having the same effect
also take each heuristic as an input to the model
also only do it from white perspective to use all the parameters effectively

**best idea so far?**
train value model on decent heuristic at depth > 1, then **continuously train the model on its own predictions at higher depth**
if the heuristic is good enough, moves should have "objective" evaluations early and without so much data
however training a neural network on its targets influenced by its own predictions may be unstable
i believe its worth a try

##### **reinforcement learning**

i first tried mimicing AlphaZero. basically a current value network generates many self play games using MCTS.
I believe the main issue with my implementation was that it was too slow at generating games. AlphaZero generated 25000 games
each training cycle. It only took four hours of training so **I'm assuming mine is just wayyyy too slow**.
AlphaZero is able to run each main step of the approach concurrently and parallelizes the self play game generation.

my theory on why so much data is required is because these methods rely purely on the outcomes of the self play games
so it takes a lot of games for the objectively better positions/moves to come out

But I think i will only come back to reinforcement learning after being able to train models using a supervised approach.
