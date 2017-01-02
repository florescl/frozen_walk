import itertools
import random
import math
import numpy as np
import random
from fractions import Fraction
import sys, getopt
from random import randrange
from collections import defaultdict

dim = 100
n_times = 10000

n_particles = 1000
p_abs = 0.00005
p_refl = 0.95

#need to change for other mass fractions being frozen

def __MAIN__():

   #p_abs = sys.argv[1]
   #p_refl = sys.argv[2]

   #file = open("far" + str(p_abs) + str(p_refl), "wb")
   #sys.stdout = file

   
   particle_distrib = [0 for x in xrange(-dim, dim)]
   particle_distrib_refl = [0 for x in xrange(-dim,dim)]
   particle_distrib_abs = [0 for x in xrange(-dim,dim)]
   nrw = [0 for x in xrange(-dim,dim)]
      
   odometer = [0 for x in xrange(-dim,dim)]
   odometer_sum = [0 for x in xrange(-dim,dim)]

   #this would have to be changed if i change the ratio of frozen stuff to 1/3
   
   particle_distrib[0] = 2*0.0625
   particle_distrib[1] = 0.0625 + 0.03125
   particle_distrib[-1] = 0.0625 + 0.03125
   particle_distrib[-2] = 0.25 + 0.0625
   particle_distrib[2] = 0.25 + 0.0625
   particle_distrib[-3] = 0.03125
   particle_distrib[3] = 0.03125

   particle_distrib_refl[0] = 2*0.0625
   particle_distrib_refl[1] = 0.0625 + 0.03125
   particle_distrib_refl[-1] = 0.0625 + 0.03125
   particle_distrib_refl[-2] = 0.25 + 0.0625
   particle_distrib_refl[2] = 0.25 + 0.0625
   particle_distrib_refl[-3] = 0.03125
   particle_distrib_refl[3] = 0.03125

   particle_distrib_abs[0] = 2*0.0625
   particle_distrib_abs[1] = 0.0625 + 0.03125
   particle_distrib_abs[-1] = 0.0625 + 0.03125
   particle_distrib_abs[-2] = 0.25 + 0.0625
   particle_distrib_abs[2] = 0.25 + 0.0625
   particle_distrib_abs[-3] = 0.03125
   particle_distrib_abs[3] = 0.03125
   
  
   step = 1
   bdry_gl = 120
   
   bdry_array = [0 for x in range(0, n_times)]
   
   while(step < n_times):
      bdry, how_much_moves_bdry, how_much_moves_bdryminus, how_much_stays_bdry, how_much_stays_bdryminus = find_bdry(particle_distrib)
      bdry_abs = find_bdry_2(particle_distrib_abs)
      bdry_refl = find_bdry_2(particle_distrib_refl)
      
      #bdry_array[step] = bdry

      new_distrib = move_mass(particle_distrib, bdry, how_much_moves_bdry, how_much_moves_bdryminus, how_much_stays_bdry, how_much_stays_bdryminus)
      new_distrib_abs = move_mass_abs(particle_distrib_abs, bdry_abs, p_abs)
      new_distrib_refl = move_mass_refl(particle_distrib_refl, bdry_refl, p_refl)
      '''
      print 'abs', assert_sum(new_distrib_abs)
      print 'refl', assert_sum(new_distrib_refl)
      print 'f', assert_sum(new_distrib)
      '''
      #odometer = get_odometer(particle_distrib, how_much_moves_bdry, how_much_moves_bdryminus, bdry)

      bdry_gl = bdry
      interchange(particle_distrib, new_distrib)
      interchange(particle_distrib_refl, new_distrib_refl)
      interchange(particle_distrib_abs, new_distrib_abs)

      step+=1
      
   summ = 0
   summ2 = 0
      
   for pos in range(-dim,dim):
      print pos, particle_distrib[pos], particle_distrib_abs[pos], particle_distrib_refl[pos]

      #file.close()



def move_mass_abs(array, b, p):
   #absorb it with probability p
   #let it move with probability 1-p

   new_array =[ 0 for x in xrange(-dim,dim)]

   coin = random.random()
   #print 'coin', coin
   
   if coin < p:
      new_array[b] = array[b]
      new_array[b-1] = 0.5*array[b-2]
      new_array[-b] = array[-b]
      new_array[1-b] = 0.5*array[2-b]
      for j in range(-b+2, b-2):
         new_array[j] = array[j+1]*0.25 + 0.25*array[j-1] + 0.5*array[j]

         
   else:
      new_array[b+1] = array[b]*0.5
      new_array[-b-1] = array[-b]*0.5
      new_array[b] = array[b-1]*0.5
      new_array[-b] = array[b-1]*0.5
      for j in range(-b+1, b-1):
         new_array[j] = array[j+1]*0.5 + 0.5*array[j-1]


   return new_array
   


def move_mass_refl(array, b, p):
   #reflect it with prob p
   #let it move with prob 1-p

   new_array =[ 0 for x in xrange(-dim,dim)]
   
   coin = random.random()
   #print 'coin', coin
   if coin < p:
      new_array[b] = array[b]
      new_array[b-1] = 0.5*(array[b-2] + array[b])
      new_array[b+1] = 0.5*array[b]
      new_array[-b] = array[-b]
      new_array[1-b] = 0.5*(array[2-b] + array[-b])
      new_array[-1-b] = 0.5*array[-b]
      
      for j in range(-b+2, b-2):
         new_array[j] = array[j+1]*0.25 + 0.25*array[j-1] + 0.5*array[j]

      

   else:
      new_array[b+1] = array[b]*0.5
      new_array[-b-1] = array[-b]*0.5
      new_array[b] = array[b-1]*0.5
      new_array[-b] = array[b-1]*0.5
      
      for j in range(-b+1, b-1):
         new_array[j] = array[j+1]*0.5 + 0.5*array[j-1]
      
   return new_array


def find_bdry_2(array):
   bdry = 0
   
   for site in range(0, dim-1):
      if((array[site] > 0) and (array[site+1] == 0)):
         bdry = site   
      else:
         continue

   return bdry



def get_odometer(particle_distrib, how_much_moves_bdry, how_much_moves_bdryminus, bdry):
      odometer = [0 for x in xrange(-dim,dim)]
      
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

#this needs some refinement

def assert_sum(particle_distrib):
   sum_i = 0
   for i in range(-dim, dim):
      sum_i+= particle_distrib[i]

   print 'sum', sum_i
      #if sum_i == 1.0:
      #print 'assertion ok'
      #else:
      #print 'assertion not ok'
      
def move_mass(particle_distrib, bdry, how_much_moves_bdry, how_much_moves_bdryminus, how_much_stays_bdry, how_much_stays_bdryminus):


   new_particle_distrib =[ 0 for x in xrange(-dim,dim)]

   new_particle_distrib[bdry] = how_much_stays_bdry + how_much_moves_bdryminus*0.5
   new_particle_distrib[bdry+1]= how_much_moves_bdry*0.5

   new_particle_distrib[bdry-1]= how_much_stays_bdryminus + how_much_moves_bdry*0.5 + 0.5*particle_distrib[bdry-2] 
   new_particle_distrib[bdry-2]= how_much_moves_bdryminus*0.5 +0.5*particle_distrib[bdry-3]

   new_particle_distrib[-bdry] = how_much_stays_bdry + how_much_moves_bdryminus*0.5
   new_particle_distrib[-bdry-1] = how_much_moves_bdry*0.5

   new_particle_distrib[-bdry+1] = how_much_stays_bdryminus + how_much_moves_bdry*0.5 + 0.5*particle_distrib[bdry-2] 
   new_particle_distrib[-bdry+2]= how_much_moves_bdryminus*0.5 +0.5*particle_distrib[bdry-3]

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

   if particle_distrib[bdry] <0.25:
      how_much_stays_bdry = particle_distrib[bdry]
      how_much_moves_bdry = 0
      how_much_stays_bdryminus=0.25-particle_distrib[bdry]
      how_much_moves_bdryminus = particle_distrib[bdry-1] - how_much_stays_bdryminus
     
   else:
      how_much_stays_bdry = 0.25
      how_much_moves_bdry = particle_distrib[bdry] -0.25
      how_much_moves_bdryminus=particle_distrib[bdry-1]
      how_much_stays_bdryminus = 0
      
   return (bdry, how_much_moves_bdry, how_much_moves_bdryminus, how_much_stays_bdry, how_much_stays_bdryminus)

def find_bdry_third(particle_distrib):
   bdry = 0

   
   for site in range(0, dim-1):
      if((particle_distrib[site] > 0) and (particle_distrib[site+1] == 0)):
         bdry = site   
      else:
         continue

      
   if particle_distrib[bdry] <0.33:
      how_much_stays_bdry = particle_distrib[bdry]
      how_much_moves_bdry = 0
      how_much_stays_bdryminus=0.33-particle_distrib[bdry]
      how_much_moves_bdryminus = particle_distrib[bdry-1] - how_much_stays_bdryminus
     
   else:
      how_much_stays_bdry = 0.33
      how_much_moves_bdry = particle_distrib[bdry] - 0.33
      how_much_moves_bdryminus=particle_distrib[bdry-1]
      how_much_stays_bdryminus = 0

   return (bdry, how_much_moves_bdry, how_much_moves_bdryminus, how_much_stays_bdry, how_much_stays_bdryminus)
    
if __name__ == '__main__':
  __MAIN__()
