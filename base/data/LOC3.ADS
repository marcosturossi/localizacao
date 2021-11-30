# CTCT ADS auto-generated

LOC3

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
0     2   1    
0     4   3    
0     8   1    
1     2   2    
1     3   0    
1     4   5    
1     8   2    
2     2   4    
2     3   1    
2     4   6    
2     8   4    
3     2   5    
3     5   0    
3     8   5    
4     3   2    
5     2   6    
5     5   1    
5     8   6    
6     5   2    

