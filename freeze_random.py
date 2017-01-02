import itertools
import random
import math
import numpy as np
import random

from random import randrange
from collections import defaultdict
from heapq import nlargest

n_particles = 10000
n_times = 30000
dim = 400
n_simulations = 4

def __MAIN__():


    particle_array_average = [0 for x in xrange(-dim, dim)]

    for n_sim_ind in range(0, n_simulations):
          
        particle_array = [0 for x in xrange(-dim,dim)]    
        particle_array[0] = n_particles

        for i in range(0,n_particles):
            if random.random() < 0.5:
                # does this take into account the move from origin?
                particle_array[1]+=1
            else:
                particle_array[-1]+=1

        particle_array[0] = 0

        bdry_left_global = 0
        bdry_right_global = 0

    
        for n_times_ind in range(1,n_times):

            bdry_left, bdry_right, how_much_stays_bdry_left, how_much_stays_bdry_right, how_much_stays_bdry_leftminus, how_much_stays_bdry_rightminus = find_bdry(particle_array)
            #print bdry_left, bdry_right
            
            bdry_left_global = bdry_left
            bdry_right_global = bdry_right

            new_distrib = move_mass(particle_array, bdry_left, bdry_right, how_much_stays_bdry_left, how_much_stays_bdry_right, how_much_stays_bdry_leftminus, how_much_stays_bdry_rightminus)

            interchange(particle_array, new_distrib)
        
        add_p(particle_array_average, particle_array)

        #print bdry_left_global, bdry_right_global
    
    for t in range(bdry_left_global+5, bdry_right_global-4):
        print t, float(particle_array_average[t])


def add_p(particle_array_average, particle_array):
    
    for ind in range(-dim, dim):
        particle_array_average[ind]+=particle_array[ind]

def assert_sum(particle_array):
    summ = 0
    for ind in range(-dim,dim):
        summ+=particle_array[ind]

    print 'summ', summ

def interchange(particle_distrib, new_distrib):
    for j in range(-dim, dim):
        particle_distrib[j] = new_distrib[j]

def move_mass(particle_array, bdry_left, bdry_right, how_much_stays_bdry_left, how_much_stays_bdry_right, how_much_stays_bdry_leftminus, how_much_stays_bdry_rightminus ):

    # check what happens at the boundaries
   new_particle_array = [0 for x in xrange(-dim,dim)]
   new_particle_array[bdry_left] = how_much_stays_bdry_left
   new_particle_array[bdry_right] = how_much_stays_bdry_right
   new_particle_array[bdry_right-1] = how_much_stays_bdry_rightminus
   new_particle_array[bdry_left+1] = how_much_stays_bdry_leftminus

   for j in range(bdry_left+2, bdry_right-1):
       if particle_array[j] > 0:
           for i in range(0, particle_array[j]):
               if random.random() < 0.5:
                   new_particle_array[j+1]+=1
               else:
                   new_particle_array[j-1]+=1

   
   if  particle_array[bdry_left] - how_much_stays_bdry_left > 0:
       for ind in range(0, particle_array[bdry_left] - how_much_stays_bdry_left):
           if random.random() < 0.5:
               new_particle_array[bdry_left+1]+=1
           else:
               new_particle_array[bdry_left-1]+=1


   if  particle_array[bdry_right] - how_much_stays_bdry_right > 0:
       for index in range(0, particle_array[bdry_right] - how_much_stays_bdry_right):
           if random.random() < 0.5:
               print bdry_right+1
               new_particle_array[bdry_right+1]+=1
           else:
               new_particle_array[bdry_right-1]+=1


   if particle_array[bdry_right-1] - how_much_stays_bdry_rightminus>0:
       for i2 in range(0, particle_array[bdry_right-1] - how_much_stays_bdry_rightminus):
           if random.random() < 0.5:
               new_particle_array[bdry_left]+=1
           else:
               new_particle_array[bdry_left+2]+=1

   
   if particle_array[bdry_left+1] - how_much_stays_bdry_rightminus > 0:
       for i3 in range(0, particle_array[bdry_left+1] - how_much_stays_bdry_rightminus):
           if random.random() < 0.5:
               new_particle_array[bdry_right]+=1
           else:
               new_particle_array[bdry_right-2]+=1


   return new_particle_array


 
def find_bdry(particle_array):

   bdry_right = dim
   bdry_left = dim
   how_much_stays_bdry_left = 0
   how_much_stays_bdry_right = 0
   how_much_stays_bdry_leftminus = 0
   how_much_stays_bdry_rightminus = 0

   site_r = dim
   ok = 0
   
   while(ok ==0):
       if((particle_array[site_r] == 0) and (particle_array[site_r-1] > 0)):
           bdry_right = site_r-1
           ok=1
       else:
           site_r-=1

   ok1 = 0
   site_l = -dim
   while(ok1 == 0):
       if((particle_array[site_l] == 0) and (particle_array[site_l+1] > 0)):
           bdry_left = site_l+1
           ok1=1
       else:
           site_l+=1


   how_much_stays_bdry_left, how_much_stays_bdry_left_minus = left(particle_array, bdry_left)
   how_much_stays_bdry_right, how_much_stays_bdry_right_minus = right(particle_array, bdry_right)

   return (bdry_left, bdry_right, how_much_stays_bdry_left, how_much_stays_bdry_right, how_much_stays_bdry_leftminus, how_much_stays_bdry_rightminus)      


def left(particle_array, bdry_left):

    how_much_stays_bdry_left = 0
    how_much_stays_bdry_leftminus = 0
    

    if particle_array[bdry_left] > int(n_particles/4):
        how_much_stays_bdry_left = int(n_particles/4)
        how_much_stays_bdry_left_minus = 0
    else:
        if particle_array[bdry_left] < int(n_particles/4):
            how_much_stays_bdry_left = particle_array[bdry_left]
            how_much_stays_bdry_leftminus = int(n_particles/4) - how_much_stays_bdry_left
        else:
            how_much_stays_bdry_left = particle_array[bdry_left] 
            how_much_stays_bdry_leftminus = 0

    return how_much_stays_bdry_left, how_much_stays_bdry_leftminus


def right(particle_array, bdry_right):

    how_much_stays_bdry_right = 0
    how_much_stays_bdry_rightminus = 0
    

    if particle_array[bdry_right] > int(n_particles/4):
        how_much_stays_bdry_right = int(n_particles/4)
        how_much_stays_bdry_rightminus = 0
    else:
        if particle_array[bdry_right] < int(n_particles/4):
            how_much_stays_bdry_right = particle_array[bdry_right]
            how_much_stays_bdry_rightminus = int(n_particles/4) - how_much_stays_bdry_right
        else:
            how_much_stays_bdry_right = particle_array[bdry_right] 
            how_much_stays_bdry_rightminus = 0

    return how_much_stays_bdry_right, how_much_stays_bdry_rightminus


if __name__ == '__main__':
  __MAIN__()


