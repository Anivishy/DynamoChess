# Feedback on sprint 1

## Some useful git commands
I used these commands to get a quick read on what everyone did. Then I delved into specific files for a closer look.
* git log --all --graph --oneline --pretty=format:"%C(auto)%<|(20,trunc)%an%<(10)%h%<(60,trunc)%s%d"
* git log --all --numstat --oneline --author <author>

## Overall score: 10/10

I've been very impressed with the progress you've made on the chess bot. Just getting it to play in the first place
is a worthy first sprint. Now that you've gotten to the hard part, I'm eager to see how you're going to tackle it!

Your git structure is pretty confusing (try a git log --all --graph --oneline to see what I mean). See if you can
all learn how to avoid merge commits (they're not currently contributing to the clarity of the log), and carefully
curate the commits on each branch before putting it up for code review.

## Specific callouts

* Ankit, you don't have many commits, but it looks like the ones you have put up have a lot of content. I'd love to
  understand what your discoveries have been so far!
* Teja, I don't see much activity from you. What's going on? I'm marking your contribution down to 6/10, but if I've
  somehow missed the work you've done, please let me know!

## Update

* Teja, thanks for pointing out the Jupyter notebook in which you sketched out the minimax algorithm. I've updated
  your score to 10/10.
