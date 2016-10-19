#! /usr/bin/python3
"""Iterative method for computing square root based on the Newton technique."""

def compute_next_iteration(previous_iteration, a):
  return (1 / 2) * (previous_iteration + a / previous_iteration)

def square_root(a):
  next_iteration = 1
  previous_iteration = 0
  while abs(next_iteration - previous_iteration) > 0.0000001:
    previous_iteration = next_iteration
    next_iteration = compute_next_iteration(previous_iteration, a)
    print(next_iteration - previous_iteration)
  print(next_iteration)


square_root(2) 

