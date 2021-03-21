#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


def generate(p=None,
             x_pair=None,
             condition='Random'
             ):
    """
    Generate exp data.
    Returns the DataFrame contains the stimulus

    Parameters
    ----------
    p : list
        1-D list of series probabilities.
    x_pair : array
        values for probabilities, (x1, x2)
    condition : str
        exp condition: random

    Returns
    -------
    df : DataFrame
    """
    if p is None:
        p = np.array([0.01, 0.05, 0.1, 0.25, 0.4, 0.5, 0.6, 0.75, 0.9, 0.95, 0.99])
    if x_pair is None:
        x_pair = np.array([(25, 0), (50, 0), (75, 0), (100, 0), (150, 0), (200, 0), (400, 0), (800, 0),
                  (50, 25), (75, 50), (100, 50), (150, 50), (150, 100), (200, 100), (200, 150)])

    df = pd.DataFrame()
    df['p'] = np.repeat(p, len(x_pair))
    df['x1'] = np.tile(x_pair[:, 0], len(p))
    df['x2'] = np.tile(x_pair[:, 1], len(p))
    df['condition'] = condition

    while True:
        if condition == 'Random':
            df = df.sample(frac=1)
        else:
            raise ValueError("condition must be random")
        df.index = range(len(df))
        df['block'] = df.index // 33 + 1
        if df.groupby('block').p.mean().max() - df.groupby('block').p.mean().min() < 0.15:
            break
        elif condition in ['large', 'small']:
            break
    return df


def generate_train(p=None,
             x_pair=None,
             condition='Random'
             ):
    """
    Generate exp data for training
    Returns the DataFrame contains the stimulus

    Parameters
    ----------
    p : list
        1-D list of series probabilities.
    x_pair : array
        values for probabilities, (x1, x2)
    condition : str
        exp condition: random

    Returns
    -------
    df : DataFrame
    """
    if p is None:
        p = np.array([0.25, 0.5, 0.75])
    if x_pair is None:
        x_pair = np.array([[200, 0], [100, 50]])

    df = pd.DataFrame()
    df['p'] = np.repeat(p, len(x_pair))
    df['x1'] = np.tile(x_pair[:, 0], len(p))
    df['x2'] = np.tile(x_pair[:, 1], len(p))
    df['condition'] = condition
    df = df.sample(frac=1)
    df.index = range(len(df))

    return df


if __name__ == '__main__':
    df = generate()
    df.to_csv('trial.csv')