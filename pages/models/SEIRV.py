import numpy as np
from scipy.integrate import odeint
import plotly.express as px
import pandas as pd


def define_SEIRV(y, t, mu, kappa, beta, gamma, sigma, N):
    '''
    Function defining the SEIRV model.
    '''

    S, E, I, R, V = y
    dS = mu*N - (beta*S*I/N) - mu*S - kappa*S
    dE = (beta*S*I/N) - sigma*E - mu*E
    dI = sigma*E - mu*I - gamma*I
    dR = gamma*I - mu*R
    dV = kappa*S - mu*V
    
    return [dS, dE, dI, dR, dV]


def solve_SEIRV(i0, mu, beta, sigma, gamma, kappa, T, N):
    '''
    Function to solve the SEIRV model using odeint from scipy.integrate.
    '''

    # Initial conditions
    S0 = N - i0     # Everyone except for initial infected population is sucseptible
    E0 = 0          # Number of initial exposed people
    I0 = i0         # Number of initial infected people
    R0 = 0          # Number of initial recovered people
    V0 = 0          # Number of initial vaccinated people
    y0 = [S0, E0, I0, R0, V0]

    # Array of integers from day 0 up to and including T 
    timespan = np.arange(0, T+1, 1)
    
    y = odeint(define_SEIRV, y0, timespan, args=(mu, kappa, beta, gamma, sigma, N))

    y_df = pd.DataFrame({
        'Time': timespan,
        'Susceptible': y[:, 0],
        'Exposed': y[:, 1],
        'Infective': y[:, 2],
        'Recovered': y[:, 3],
        'Vaccinated': y[:, 4]
    })

    return y_df


def make_plot(y_df):
    
    fig = px.line(y_df, x='Time', y=['Susceptible', 'Exposed', 'Infective', 'Recovered', 'Vaccinated'],
                  labels={'value': 'Number of people', 'Time': 'Time (days)'})
    fig.update_traces(mode="lines", hovertemplate=None)
    fig.update_layout(hovermode="x unified")
    return fig

