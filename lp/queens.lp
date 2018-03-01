% CS-E4800 Artificial intelligence
% Round: Logic Programming
%
% Base Encoding for the ASP Exercise: n-Queens
%
% Some parts of the encoding have been deleted and indicated by
% question marks "???". You are supposed to fill in the missing details
% on the basis of descriptions given as well as general understanding of
% the problem.

% Parameters: the number of queens by default

#const n=12.

% Define the range of coordinate values from 1 to n. Both columns and
% rows will be referred to using these values: predicates col/1 and row/1

coord(1..n,1..n).
col(X) :- coord(X,Y).
row(Y) :- coord(X,Y).

% Choose the row Y for the queen placed on column X. The idea is to
% place the queen at (X,Y) by default unless it has been placed on
% some other row in that column. Encode the exceptions using
% an appropriate auxiliary predicate.

queen(X,Y) :- col(X),row(Y),not other_queen(X,Y) .
% Add rules as needed
other_queen(X,Y) :- col(X),row(Y),row(Z),queen(X,Z),Y!=Z.

% It is forbidden to put two queens on the same row Y

:- queen(X1,Y), queen(X2,Y), X1<X2.

% Similarly, it is forbidden to put two queens on the same diagonal.
% Two queens are on a same diagonal if the difference in their column
% positions equals to the difference in their row positions. In ASP,
% absolute values can be expressed using bars: |...|

:- queen(X,Y), queen(X1,Y1),Y<Y1,|X1-X|==Y1-Y.

% Extract solution (the following predicate is used in the evaluation)

#show queen/2.
