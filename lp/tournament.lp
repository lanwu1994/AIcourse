% CS-E4800 Artificial intelligence
% Round: Logic Programming
%
% Base Encoding for the ASP Exercise: Tournament Scheduling
%
% Some parts of the encoding have been deleted and indicated by
% question marks "???". You are supposed to fill in the missing details
% on the basis of descriptions given as well as general understanding of
% the problem.

% Parameters: the number of teams (silently assumed to be even)

#const n=8.

% Declare the domains for the teams, fields, and weeks

team(1..n).
field(1..n/2).
week(1..n-1).

% Define matches (an ordered pair of teams)

match(X,Y) :- team(X),team(Y),X<Y.

% Choose the week W for the match between T1 and T2 by default,
% unless the match is organized some other week. Encode exceptions
% using an appropriate auxiliary predicate.

thisweek(T1,T2,W) :- match(T1,T2),week(W),not other_week(T1,T2,W).

% Add rules as needed 
other_week(T1,T2,W) :- match(T1,T2),week(W),week(W1),W!=W1,thisweek(T1,T2,W1).

% Choose the field F for the match between T1 and T2 by default,
% unless the match takes place in some other field. Encode exceptions
% using an appropriate auxiliary predicate.

thisfield(T1,T2,F) :- match(T1,T2),field(F),not other_field(T1,T2,F).

% Add rules as needed
other_field(T1,T2,F) :- match(T1,T2),field(F),field(F1),F!=F1,thisfield(T1,T2,F1).

% Every slot (F,W) in the schedule, identified by a field F and a week W,
% must have a match scheduled

occupied(W,F) :- week(W), field(F),thisweek(T1,T2,W),thisfield(T1,T2,F).

% ONE slot (F,W) cannot be occupied by two match.
:- occupied(W,F), thisfield(T1,T2,F),thisweek(T1,T2,W),thisfield(T3,T4,F),thisweek(T3,T4,W),
	(T1,T2)!=(T3,T4).

% A team may have only one match per week

opponent(T1,W,T2) :- thisweek(T1,T2,W).
opponent(T2,W,T1) :- thisweek(T1,T2,W).
%:- opponent(T,W,T1),T>T1.
:- opponent(T,W,T1), opponent(T,W,T2),T1!=T2.
:- opponent(T1,W,T), opponent(T2,W,T),T1!=T2.
:- opponent(T,W,T1), opponent(T2,W,T),T1!=T2.

% Combine the schedule into a single relation for the ease of understanding

match(T1,T2,F,W) :- thisfield(T1,T2,F),thisweek(T1,T2,W),occupied(W,F), T1<T2.

% Symmetry breaking
%On the tournament quiz question: define total orders on
%1. The matches (fields) within a week
%2. The weeks based on the matches that are played on a given week
%then forbid the case order(W1) > order(W2) if W1 < W2 and similarly for the matches.


:- match(T1,T2,F,W), match(T3,T4,F1,W),T1<T3,F>F1.

:- match(1,T2,1,W),match(1,T4,1,W1),T2<T4,W>W1.







% Extract solution (the following predicates are used in the evaluation)


#show match/4.
#show team/1.
