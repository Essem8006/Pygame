# Agentic behaviour in python
Ispired by Sebastian Lague

## Main
The agents in question are followers who will attempt to move towards any other agent in front of them. This often results in loops and interconnected trails that adapt over time. Due to the fact they are 'moving towards' and not 'following' agents of the other colour they often take the same path but in opposite directions which enforces the presence of routes rather than resulting in agents all streaming in the same direction.

## Avoidence
The same happens here but with 2 sets of agents that while moving towards agents of the same colour will attempt to avoid agents of the other colour.

## Todo
* Fix main's bottom right bias
* Fix problem closing avoidence on long run