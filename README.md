# ChessBot
Potential Problems/Research Areas:
Possible Database (for first iteration of bot based on elo ratings): https://www.kaggle.com/datasets/datasnaek/chess
Lichess API: https://lichess.org/api#tag/Relations/operation/unfollowUser
Start with a well followed user, find all the followers and the followers of their followers and so on to build a databased of all users. Then loop through the list of these users to get all of their games.
1: Decide if we want create this as a python application or as a website
-	Research Jango/React
2: Parser to translate data with moves to translate pulled data into our engine
-	Look at already available API
3: The actual ML
-	Research feature vectors
Possible Backup Plan?
-	Create some form of a chess bot on our own
Vague Timeline:
By Start of April
-	UI and basic engine is done
-	Lichess data base created/downloaded
-	Architecture for the entire project
-	Basic proof of concepts for chess bot 
o	Basic chess bot (basic using the basic chess module) to understand the structure of how a chess bot works
o	Translate output form this into the UI

Mid April
-	Translating the proof of concept into the architecture to implement the Neural Network
End of May
-	Implement the Proof of Concept
