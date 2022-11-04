# Quoridor

## What is Quoridor?
Quoridor is a 2 or 4 players board game which whose board consists of 81 square pieces (9x9). Each player is represented by a pawn which begins at the center space of one edge of the board. Besides, there are 20 walls that will be divided equally among the players at the start of the game, and once placed, cannot be moved or removed.

<p align="center">
<img src="./images/board.jpg" width=25%>
</p>

The objective is to be the first player to move their pawn to any piece on the opposite side of the game board from which it begins.


## What are the rules?
1. Pawns can only move in 4 main directions (but not diagonally) 
<p align="center">
<img src="./images/legal_moves_1.png" width=25% hspace=2.5%> <img src="./images/illegal_moves_1.jpeg" width=25% hspace=2.5%>
</p>

2. If adjacent to another pawn, the pawn may jump over that pawn
<p align="center">
<img src="./images/legal_moves_3.jpg" width=25%>
</p>

3. Pawns can't jump over the wall
<p align="center">
<img src="./images/illegal_moves_2.jpg" width=25%>
</p>

4. If an adjacent pawn has a third pawn or a wall on the other side of it, the player may move to either space that is immediately adjacent (left or right) to the first pawn
<p align="center">
<img src="./images/legal_moves_4.jpg" width=25%>
</p>

5. The walls should be placed in a way that there remains at least one path that any pawn can use to reach the other side of the board
<p align="center">
<img src="./images/illegal_wall.jpg" width=25%>
</p>


## How to run?

### Python
1. Clone the repository:

	`git clone https://github.com/kiarashvosough1999/Quoridor.git`
    
2. Go to the cloned directory and then *python* sub-directory:

	`cd Quoridor/python/`
    
3. Create a virtual environment and then activate it:
	
    `python3 -m venv quoridor ; source quoridor/bin/activate`
    
4. Install the dependencies:
	
	`pip3 install -r  requirements.txt`
    
5. Run the program:

	`python3 main.py`
