# CTCT ADS auto-generated

SR1

State size (State set will be (0,1....,size-1)):
# <-- Enter state size, in range 0 to 2000000, on line below.
7

Marker states:
# <-- Enter marker states, one per line.
# To mark all states, enter *.
# If no marker states, leave line blank.
# End marker list with blank line.
0

Vocal states:
# <-- Enter vocal output states, one per line.
# Format: State  Vocal_Output.  Vocal_Output in range 10 to 99.
# Example: 0 10
# If no vocal states, leave line blank.
# End vocal list with blank line.

Transitions:
# <-- Enter transition triple, one per line.
# Format: Exit_(Source)_State  Transition_Label  Entrance_(Target)_State.
# Transition_Label in range 0 to 999.
# Example: 2 0 1 (for transition labeled 0 from state 2 to state 1).
0     1   1    
0     2   3    
0     5   1    
0     6   1    
0     8   3    
1     1   0    
1     2   2    
1     5   0    
1     6   0    
1     8   2    
2     1   3    
2     2   5    
2     3   0    
2     5   3    
2     6   3    
2     8   5    
3     1   2    
3     2   4    
3     3   1    
3     5   2    
3     6   2    
3     8   4    
4     1   5    
4     3   2    
4     5   5    
5     2   6    
5     3   3    
5     6   4    
5     8   6    
6     3   4    

