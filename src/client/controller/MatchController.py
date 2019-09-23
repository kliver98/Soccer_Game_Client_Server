'''
Created on 22/09/2019

@author: Usuario
'''

from client.model import Match as m

class MatchController():
    """Class that handle all events that connects with model"""
    
    def __init__(self):
        """Builder that starts relation with model"""
        self.match = m.Match()
    
    def is_collided_with(self, player, sprite):
        """Method that check if a player with the ball collided together"""
        return self.match.is_collided_with(player, sprite)