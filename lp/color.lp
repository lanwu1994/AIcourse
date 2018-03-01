% CS-E4800 Artificial intelligence
% Round: Logic Programming
%
% Base Encoding for the ASP Exercise: Graph Coloring
%
% Some parts of the encoding have been deleted and indicated by
% question marks "???". You are supposed to fill in the missing
% details on the basis of descriptions given as well as general
% understanding of the problem.
%
% A number of graph instances is included for testing purposes.

% Parameters: the number of colors

#const n=3.


% Define the range of colors from 1 to n

color(1..n).


% Extract the nodes of the graph from the edge/2 relation

node(X) :- edge(X,Y).
node(Y) :- edge(X,Y).

% Choose a color C for each node X. By default the color can be C as
% long as there is no exceptions, i.e., X is colored by some other color
% than C. Use some auxiliary predicate to encode the exceptions.

hascolor(X,C) :- node(X),color(C),not other_color(X,C).
%, not alreadycolor(X,C).

% Add rules as needed
% X is colored by a color i .
other_color(X,C) :- node(X),color(C),hascolor(X,I),color(I),I!=C.


% Check the coloring condition for every edge of the graph:
% X and Y should have different colors.

:- edge(X,Y), color(C), hascolor(X,C),hascolor(Y,C).

% Extract solution (the following predicates are used in the evaluation)

#show hascolor/2.
#show edge/2.

