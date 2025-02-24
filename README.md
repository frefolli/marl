# Notes

# Bidirectional Tracks

Add a route, then `center` its alignment and set it as `template route`. Then you can right-click and select `Edge Operations > Add Reverse Direction to Edge` to creare the reverse connected edge.
Always remember to hit F5 to re-render the scenario.

# Traffic Light Phases

All phases should either a Green XOR a Yellow Phase.
For example:
- rrrGGGrrrGGG
- rrryyyrrryyy
- GGGrrrGGGrrr
- yyyrrryyyrrr

This leads to a continous sequence of $1G -> 1y -> 2r$.
