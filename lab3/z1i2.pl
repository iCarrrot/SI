:-
[ library(clpfd)
, library(dcg/basics)
, library(pio)
, library(main)
].

lengthCheck(_,[],[]).
lengthCheck(Size, [Start], [Len]):-
    Start + Len #=< Size.
lengthCheck(Size, [Start1|[Start2|Rest]], [Len|LRest]):-
    Start1 #>= 0,
    Start1 + Len #< Start2,
    Start1 + Len #< Size,
    lengthCheck(Size, [Start2|Rest], LRest).

bitsCheck(_,[],_,_).
bitsCheck(Index, [B|Bits], Starts, Lengths):-
    Index1 is Index + 1,
    bitCheck(Index, B, 0,Starts, Lengths),
    bitsCheck(Index1, Bits, Starts, Lengths).

bitCheck(Index,B,Last,[],[]) :- 
    Index #>= Last #==> B#=0.

bitCheck(Index, Bit, Last, [Start|SS], [L|Lengths]):-
    E #= Start + L,
    Index #<Start #/\ Index #>= Last #==> Bit #= 0,
    Index #>= Start #/\  Index #< E #==> Bit #=1,
    
    bitCheck(Index, Bit, E, SS, Lengths).

rowCheck(Size,Starts,Lengths,Bits):-
    lengthCheck(Size,Starts,Lengths),
    bitsCheck(0,Bits,Starts,Lengths).

setStartsDomain(_,[]).
setStartsDomain(Size, [H|T]):-
    H in 0..Size,
    setStartsDomain(Size,T).

solveRows(_,[],_).
solveRows(Size, [H|T], [B|Bits]):-
    length(H, Len),
    length(Starts, Len),
    setStartsDomain(Size, Starts),
    rowCheck(Size,Starts,H,B),
    solveRows(Size,T,Bits).


setLen(_,[]).
setLen(Len, [H|T]):- 
    length(H, Len),
    setLen(Len, T).

setDomainList([]).
setDomainList([H|T]):-
    setDomain(H),
    setDomainList(T).

setDomain([]).
setDomain([H|T]):-
    H in 0..1,
    setDomain(T).




fullCheck(Rows, Cols, Bits):-
    length(Rows, RowLen),
    length(Cols, ColLen),
    length(Bits, RowLen),
    setLen(ColLen, Bits),
    setDomainList(Bits),
    transpose(Bits, BitsCol),
    solveRows(ColLen, Rows, Bits),
    solveRows(RowLen, Cols, BitsCol).


line([X|Xs])--> integer(X),whites, line(Xs).
line([])--> blanks.

lines(0,[])-->[].
lines(Size, [H|Rest])--> line(H), {Size1 is Size - 1}, lines(Size1, Rest).

gInput(Rows, Cols) -->
    integer(N),
    !, whites, 
    integer(M), blanks,
    lines(N,Rows),
    lines(M,Cols).

getData(Rows, Cols):-
    phrase_from_file(gInput(Rows,Cols), "zad_input.txt").

dict(1, "#").
dict(0, ".").


rowPrint(Stream, [H|T]):-  write(Stream,H),rowPrint(Stream,T).
rowPrint(Stream,[]):-nl(Stream).
picturePrint(Bits):-
    open("zad_output.txt", write, Stream),
    maplist(maplist(dict), Bits, Pic),
    maplist(rowPrint(Stream), Pic),
    close(Stream).

main(_):-
    getData(Rows,Cols),
    fullCheck(Rows,Cols, Bits),
    picturePrint(Bits),
    halt.

