# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 17:12:00 2017

@author: joseph.chen
"""

import random

class FishShrimpCrab(object):
    
    def __init__(self):
        self.dice = [1,2,3,4,5,6]
        
    def shake(self):
        result = []
        for _ in range(3):
            result.append(random.sample(self.dice,1)[0])
        return result
    
    def odds(self, bet, result):
        '''
        bet: {"combination","single","any"}
        '''
        pay = 0
        for bet_type in bet.keys():
            if bet_type=="any":
                if max(result)==min(result):
                    pay += 33
                else:
                    pay += 0
            elif bet_type=="single":
                bet_choice = bet[bet_type]
                if (bet_choice in result):
                    if result.count(bet_choice)==1:
                        pay += 2
                    elif result.count(bet_choice)==2:
                        pay += 3
                    elif result.count(bet_choice)==3:
                        pay += 8
                else:
                    pay += 0
            elif bet_type=="combination":
                bet_choice = bet[bet_type]
                if all(x in result for x in bet_choice):
                    result = sorted(result)
                    if result[0]!=result[1] and result[1]!=result[2]:
                        pay += 6
                    else:
                        pay += 11
                else:
                    pay += 0
        return pay
    
    def play(self, N=1, bet={"single":2}):
        total_pay = 0
        for n in range(N):
            result = self.shake()
            pay = self.odds(bet, result)
            #print(pay)
            total_pay += pay
        return total_pay
    
    
if __name__=="__main__":
    game = FishShrimpCrab()
    bet_amount = 1
    Nsim = 50000000
    total_bet = bet_amount*Nsim
    #total_pay = game.play(Nsim, bet={"combination":[3,4]})
    #total_pay = game.play(Nsim, bet={"any":None})
    total_pay = game.play(Nsim, bet={"single":6})
    print("RTP: {}".format(float(total_pay)/total_bet))