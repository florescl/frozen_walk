import itertools
import random
import math
#import numpy as np
import random
from fractions import Fraction

from random import randrange
from collections import defaultdict

dim = 400
n_times = 50000
alpha = 0.7

def __MAIN__():
   particle_distrib = [0 for x in range(-dim, dim)]
   odometer = [0 for x in range(-dim,dim)]
   odometer_sum = [0 for x in range(-dim,dim)]

   particle_distrib[-1] = 0.5*alpha/2
   particle_distrib[1] = 0.5*alpha/2
   particle_distrib[0] = 0.5-alpha/4
   particle_distrib[-2] = particle_distrib[2] = 0.5*(0.5 - alpha/4)

   
   #particle_distrib[0] = 2*0.0625
   #particle_distrib[1] = 0.0625 + 0.03125
   #particle_distrib[-1] = 0.0625 + 0.03125
   #particle_distrib[-2] = 0.25 + 0.0625
   #particle_distrib[2] = 0.25 + 0.0625
   #particle_distrib[-3] = 0.03125
   #particle_distrib[3] = 0.03125
      
   step = 1
   bdry_gl = 120
   
   bdry_array = [0 for x in range(0, n_times)]
   
   while(step < n_times):
      bdry, how_much_moves_bdry, how_much_moves_bdryminus, how_much_stays_bdry, how_much_stays_bdryminus = find_bdry(particle_distrib)

      new_distrib = move_mass(particle_distrib, bdry, how_much_moves_bdry, how_much_moves_bdryminus, how_much_stays_bdry, how_much_stays_bdryminus)

      if bdry_gl != bdry:
         print(step, bdry)

      bdry_gl = bdry
      interchange(particle_distrib, new_distrib)
      step+=1

 
def get_odometer(particle_distrib, how_much_moves_bdry, how_much_moves_bdryminus, bdry):
      odometer = [0 for x in range(-dim,dim)]
      
      for j in range(-dim,dim):
            odometer[j] = particle_distrib[j]

      odometer[bdry] = how_much_moves_bdry
      odometer[bdry-1] = how_much_moves_bdryminus
      odometer[dim-bdry] = how_much_moves_bdry
      odometer[dim-bdry+1] = how_much_moves_bdryminus

      return odometer

def assert_pos(particle_distrib):
      ok = 1
      
      for j in range(-dim, dim):
            if particle_distrib[j] <0:
                  ok=0
      return ok
                  

def interchange(particle_distrib, new_distrib):
    for j in range(-dim, dim):
        particle_distrib[j] = new_distrib[j]


def assert_sum(particle_distrib):
   sum_i = 0
   for i in range(-dim, dim):
      sum_i+= particle_distrib[i]

   print ('sum', sum_i)

      
def move_mass(particle_distrib, bdry, how_much_moves_bdry, how_much_moves_bdryminus, how_much_stays_bdry, how_much_stays_bdryminus):

   new_particle_distrib =[ 0 for x in range(-dim,dim)]

   new_particle_distrib[bdry] = how_much_stays_bdry + how_much_moves_bdryminus*0.5
   new_particle_distrib[bdry+1]= how_much_moves_bdry*0.5

   new_particle_distrib[bdry-1]= how_much_stays_bdryminus + how_much_moves_bdry*0.5 + 0.5*particle_distrib[bdry-2] 
   new_particle_distrib[bdry-2]= how_much_moves_bdryminus*0.5 + 0.5*particle_distrib[bdry-3]


   new_particle_distrib[-bdry] = how_much_stays_bdry + how_much_moves_bdryminus*0.5
   new_particle_distrib[-bdry-1] = how_much_moves_bdry*0.5

   new_particle_distrib[-bdry+1] = how_much_stays_bdryminus + how_much_moves_bdry*0.5 + 0.5*particle_distrib[bdry-2] 
   new_particle_distrib[-bdry+2]= how_much_moves_bdryminus*0.5 + 0.5*particle_distrib[bdry-3]

   for j in range(-bdry+3, bdry-2):
      new_particle_distrib[j] = particle_distrib[j+1]*0.5 + 0.5*particle_distrib[j-1]

   return new_particle_distrib


def find_bdry(particle_distrib):
   bdry = 0

   for site in range(0, dim-1):
      if((particle_distrib[site] > 0) and (particle_distrib[site+1] == 0)):
         bdry = site   
      else:
         continue

   if particle_distrib[bdry] < alpha/2:
      how_much_stays_bdry = particle_distrib[bdry]
      how_much_moves_bdry = 0
      how_much_stays_bdryminus= alpha/2-particle_distrib[bdry]
      how_much_moves_bdryminus = particle_distrib[bdry-1] - how_much_stays_bdryminus
     
   else:
      how_much_stays_bdry = alpha/2
      how_much_moves_bdry = particle_distrib[bdry] - alpha/2
      how_much_moves_bdryminus=particle_distrib[bdry-1]
      how_much_stays_bdryminus = 0
      
   return (bdry, how_much_moves_bdry, how_much_moves_bdryminus, how_much_stays_bdry, how_much_stays_bdryminus)

    
if __name__ == '__main__':
  __MAIN__()
