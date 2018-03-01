% CS-E4800 Artificial intelligence
% Round: Logic Programming
%
% Base Encoding for the ASP Exercise: Sudoku
%
% Some parts of the encoding have been deleted and indicated by
% question marks "???". You are supposed to fill in the missing
% details on the basis of descriptions given as well as general
% understanding of the problem.

% A number of Sudoku instances is included for testing purposes.

% The dimension of the problem for (k*k) x (k*k) Sudoku instance
% (For instance, if k=3, we obtain the usual 9x9 Sudokus.)

#const k=2.

% Define the cells of the Sudoku puzzle
%clue(4,2,3). clue(3,1,4). clue(2,4,2). clue(2,3,3). clue(4,4,1).


number(1..k*k).
cell(X,Y) :- number(X),number(Y).

% Take the given clues into account

value(X,Y,N) :- clue(X,Y,N).

% For each cell (X,Y) and value N from the range 1..k*k, set the
% value of (X,Y) to be N by default, i.e., unless some other
% value than N has been picked for that cell. Formalize these
% exceptions using an auxiliary predicate.

value(X,Y,N) :- cell(X,Y), number(N),not other_value(X,Y,N).
% Add rules as needed
other_value(X,Y,N) :- cell(X,Y),number(N),number(N1), N1!=N,value(X,Y,N1).

% Constraints for columns (no number occurs more than once on a column).

:- value(X,Y,N), value(X,Y1,N), Y!=Y1.

% Constraints for rows (no number occurs more than once on a row).
:- value(X,Y,N), value(X1,Y,N), X!=X1.

% As regards the regions of size k*k in the puzzle, we can calculate
% their coordinates as pairs <b_x+d_x,b_y+d_y> where base values b_x
% and b_y are numbers in the set {0, k, 2k, (k-1)*k} and d_x and d_y
% are numbers in the range 1..k.

base(k*K) :- K=0..k-1.
diff(1..k).

% Constraints for each region identified by (BX,BY) and a number N:
% The number must not appear twice within the region.


% 1.dont't allow two same number in the same region (different row)
:- value(BX+I,BY+J,N), value(BX+A,BY+B,N), B!=J,diff(A),diff(B),
   base(BX), base(BY), number(N), diff(I),diff(J).

% Add similar constraints as needed
% 2.dont't allow two same number in the same region (different column)
:- value(BX+I ,BY+J,N), value(BX+A,BY+B,N),A!=I,diff(A),diff(B),
   base(BX), base(BY), number(N), diff(I),diff(J).


% Extract solution (the following predicates are used in the evaluation)

#show value/3.
#show clue/3.
