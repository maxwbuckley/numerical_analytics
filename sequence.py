#! /usr/bin/python3
"""This is a program for computing the values in a given sequence."""

import matplotlib
import matplotlib.pyplot as plt
import timeit
import decimal
import pandas


DECIMAL_PRECISION = [16, 32, 64]

class SequenceGenerator():
  def __init__(self, is_decimal=False, precision=None):
    """Initializes sequence generator.

    Args:
      is_decimal: boolean of wheter to use decimal.Decimal rather than float.
      precision: integer of how many digits of precision to use.
    Raises:
      ValueError if is_decimal is True without passing a precision value.
    """
    # Default value
    self.decimal = False
    if is_decimal and not precision:
      raise ValueError("You cannot use decimal without specifying an integer "
                       "precision value") 
    elif is_decimal:
      self.decimal = True
      self.precision = precision
    self.values = [self.numeric()(4.0), self.numeric()(4.25)]


  def numeric(self):
    """Returns the numeric type we want for computations.
    
    Either decimal or float depending on the generator settings
    """ 
    if self.decimal: return decimal.Decimal
    return float

  def get_value(self, n):
    """Returns the nth value in the sequence.

    Args:
      n: integer, the nth value of x_i that we need.
    Returns:
      float the value of x_i at position n. Returned as a float regardless of
          whether computation is done in Decimal for ease of plotting later.
    """
    while n >= len(self.values):
      if self.decimal:
        # Precision is set module wide so need to reset for each series.
        decimal.getcontext().prec = self.precision 
      new_value = (
          self.numeric()(108) - (self.numeric()(815) -self.numeric()(1500)/
          self.values[-2])/self.values[-1])
      # We store the decimal value as appropriate.
      self.values.append(new_value)
    return float(self.values[n])


def plot_output(output, title, x_axis_label, y_axis_label):
  """Plots the output with labels.
  
  Args:
    output: dictionary of output
    title: string title to be put on graph.
    x_axis_label: string label for x (horizontal) axis.
    y_axis_label: string label for y (vertical) axis.
  """
  df = pandas.DataFrame(output)
  df.reindex_axis(sorted(df.columns), axis=1) 
  df.plot()
  plt.title(title)
  plt.ylabel(y_axis_label)
  plt.xlabel(x_axis_label)
  plt.show()


def setup_generator_dict():
  """Sets up a dictionary of string keys mapped to SequenceGenerator objects.

  Returns:
    a dict mapping string keys to SequenceGenerator objects.
  """
  generator_dict = {}
  generator_dict['float'] = SequenceGenerator()  
  generator_dict.update ({
      'decimal_precision_%s' % n: SequenceGenerator(
          is_decimal=True, precision=n) for n in DECIMAL_PRECISION})
  return generator_dict


def convergence_experiment():
  """Runs the experiment to test the convergence of the series."""
  generator_dict = setup_generator_dict()
  output = {}
  for i in range(40):
    #default_time = timeit.Timer(lambda: default_generator.get_value(i))
    for key in generator_dict.keys():
      output.setdefault(key, []).append(
          generator_dict[key].get_value(i))
  title = ('Approximations for the ith value of X for different precision '
           'number systems')
  # These are intentionally switched to put the value of X on the y axis.
  x_lab = 'i'
  y_lab = 'X value'
  plot_output(output, title, x_lab, y_lab)


def timing_experiment():
  """Runs the experiment to test the timings."""
  repetitions = 100000
  generator_dict = setup_generator_dict()
  output = {}
  for i in range(40):
    for key in generator_dict.keys():
      output.setdefault(key, []).append(timeit.timeit(
          lambda: generator_dict[key].get_value(i), number=repetitions))
  title = ('Runtime calculating the ith value of X for different number' 
           'representations.')
  x_lab = 'i'
  y_lab = 'Runtime for %d repetitions' % repetitions
  plot_output(output, title, x_lab, y_lab)


if __name__ == '__main__':
 convergence_experiment()
 timing_experiment()
