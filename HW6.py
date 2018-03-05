import numpy as np
import scr.FigureSupport as figureLibrary
import scr.StatisticalClasses as Stat

class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin

    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        return 100*self._countWins - 250


class SetOfGames:
    def __init__(self, prob_head, n_games):
        self._gameRewards = [] # create an empty list where rewards will be stored
        self._gameLosses = [] #empty list of lost games
        self._value = self._gameRewards
        self._count_loss=0

    def simulation(self, n_games,prob_head):
        # simulate the games
        for n in range(n_games):
            # create a new game
            game = Game(id=n, prob_head=prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())

        for value in self._gameRewards:
            if value <0:
                self._count_loss+=1
                i=1
                self._gameLosses.append(i)
            elif value >0:
                i = 0
                self._gameLosses.append(i)
        return SetOfGamesOutcomes(self)


    def get_loss_list(self):
        return self._gameLosses


    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return sum(self._gameRewards) / len(self._gameRewards)

    def get_reward_list(self):
        """ returns all the rewards from all game to later be used for creation of histogram """
        return self._gameRewards

    def get_max(self):
        """ returns maximum reward"""
        return max(self._gameRewards)

    def get_min(self):
        """ returns minimum reward"""
        return min(self._gameRewards)

    #code from survivalmodelclasses


class SetOfGamesOutcomes:
    def __init__(self, simulated_cohort):
        self._simCohort = simulated_cohort
        self._sumStat_expect_reward = Stat.SummaryStat('expected game rewards', self._simCohort.get_reward_list())
        self._sumStat_expect_loss = Stat.SummaryStat('expected game losses', self._simCohort.get_loss_list())

    def get_ci_reward(self,alpha):
        return self._sumStat_expect_reward.get_t_CI(alpha)

    def get_ci_loss(self,alpha):
        return self._sumStat_expect_loss.get_t_CI(alpha)

# Calculate expected reward of 1000 games
trial = SetOfGames(prob_head=0.5, n_games=1000)
hw6=trial.simulation(n_games=1000, prob_head=0.5)

#print("The average expected reward is:", trial.get_ave_reward(alpha=0.05))
print ("95% CI of Expected Rewards" , hw6.get_ci_reward(alpha=0.05))

#trial2 = SetOfGames (prob_head=0.5, n_games=10)
#print ("Gambler w/ 10 attempts", trial2.get_ave_reward(alpha=0.05))
print ("95% CI of expected losses", hw6.get_ci_loss(alpha=0.05))

trial2 = SetOfGames (prob_head = 0.5, n_games = 10)
gambler = trial2.simulation(n_games=10, prob_head=0.5)

print ("95% PI of expected Rewards for Gambler", gambler.get_ci_reward(alpha=0.05))

trial3 = SetOfGames (prob_head = 0.5, n_games = 10000)
casino = trial3.simulation(n_games=10000, prob_head=0.5)

print ("95% CI of expected Rewards for Casino", casino.get_ci_reward(alpha=0.05))


#Given that you repeat the game many (1000) times,
# 95% of confidence intervals generated from each cohort of 20 flips each will cover the true mean reward

#Casino owner expected reward would be a 95% CI (-26.04, -22.24)
# We would use a CI for the casino perspective due to sufficiently large sample size (n=10000) which indicates a steady state simulation
#The CI for the casino is quite narrow, which would give more certainty in the expected reward paid out to each gambler
#The casino can be fairly certain that it will profit from the game due to the 95% CI being entirely negative, meaning that over the course
#of many games, the average gambler will lose money to the casino

#The expected reward for the Gambler would be a 95% prediction interval (-135.74, -4.26)
#We would use a PI for the gambler perspective due to small sample size (n=10) which indicates a transient state simulation
#The PI for the gambler is very wide, which would give less certainty in the expected reward paid out to the gambler
