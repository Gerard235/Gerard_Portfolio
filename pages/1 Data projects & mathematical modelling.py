import streamlit as st
import sys
import plotly.express as px
import plotly.io as pio
import numpy as np
import pandas as pd
from PIL import Image

from models.SEIRV import *

sys.path.append("./gerard_portfolio")

st.set_page_config(layout="wide", initial_sidebar_state="auto", page_title="Data projects")

def Data_Projects_page():
    st.title("Gerard's web portfolio")
    with st.expander("Workforce modelling with Markov chains"):
        st.markdown(r'''
                    Markov models are a well-known approach to studying an organisation's workforce. In a Markov model the workforce under consideration is distributed by some categorisation (e.g., by pay, skill, job type, or length of service). As an equation the model can be written as 

                    $$
                    \begin{align}
                    n(t+1) &= n(t) \,P + e
                    \end{align}
                    $$ 
                    where $n$ are row vectors with the workforce distributed by a categorisation at a given timestep, $P$ is a probability or proportion matrix that transitions or proportions the categorised headcounts at $t$ to a distribution at $t+1$, and $e$ is a vector of entrants into each category.

                    For example, consider a workforce with three pay grades described by
                    $$
                    \begin{align*}
                    n(t+1) &=\begin{bmatrix} 8 & 10 & 4 \end{bmatrix}
                    \begin{bmatrix}
                    0.5 &  0.5 & 0 \\
                    0.1 & 0.7 & 0.1 \\
                    0 & 0.25 & 0.5
                    \end{bmatrix}
                    + \begin{bmatrix} 4 & 5 & 0 \end{bmatrix}
                    \end{align*}
                    $$ 

                    In this example there are 8, 10 and 4 people at pay grades one, two and three respectively. Of the 8 people at pay grade one, according to the first row of the transition matrix at the next timestep half will stay at this grade, half will move up a grade, and none will move up two grades. There are 10 people at pay grade 2, and at the next timestep one person wil move down, one will move up, seven will stay at the same pay grade and the system loses 1 person (alternatively we could introduce a new category, to account for separations). There are also four people at the third pay grade, a quarter of these will go down a pay grade, half will remain, and a quarter leave. Finally, there are four entrants into pay grade one and five into pay grade two.

                    Equation $(1)$ is exact when the inputs are known, such as for historical data. The equation becomes a model when one forecasts future timesteps, since the exact inputs are unknown and have to be estimated. To make this easier, it is usually assumed that $P$ is fixed, that is the proportions moving between groups is constant over time; this is known as the Markov assumption. 
                    
                    For example, I created Markov models of the Australian Public Service's (ongoing) workforce, based on the data at this [link](https://www.apsc.gov.au/initiatives-and-programs/workforce-information/workforce-data/aps-data-release-and-statistical-bulletins). The chart below shows the results of a simple Markov model, constructed based on data as at December 2019 and December 2020. The model can be interpreted as indicating the evolution of the APS (ongoing) workforce if promotions, engagements and separations continue in similar fashion to 2019/2020. Double-click on a classification to see just its curve. You can multiply the number of yearly entrants with the sliders below.
                    ''')
        
        def iterable_Markov_calc(state_t0, engmt, prob_matr, iterations, start_year=2019):
            # This function iterates the Markov model for as many times as specified by iterations. It expects as input the initial or the adjusted probability matrix.
            
            state_t0 = np.asarray(state_t0)
            state_t0 = np.hstack((state_t0, [[0]]))
            state_nth = np.copy(state_t0)
            results = np.zeros((iterations+1, 15))
            results[:, 0] = np.arange(start_year, start_year+iterations+1)
            results[0,1:] = state_t0
            
            if type(engmt) == pd.core.frame.DataFrame:  
                engmt_in = np.asarray(engmt)
                engmt_in = np.hstack((engmt_in, [[0]]))
                
                for i in range(iterations):
                    state_nth = np.matmul(state_nth, prob_matr) + engmt_in
                    results[i+1, 1:] = state_nth
            
            return results

        # Initial model for 10 years. 
        adj_prob_matr = np.load('media/simple_prob_matrix.npy', allow_pickle=True)
        state_Dec2019 = pd.DataFrame({'Trainee':[304], 'Graduate':[914], 'APS1':[269], 'APS2':[1491], 'APS3':[10721], 'APS4':[25553], 'APS5':[19505], 'APS6':[31693], 'EL1':[25457], 'EL2':[11125], 'SES1':[2033], 'SES2':[547], 'SES3':[120]})
        engmt_Dec2020 = pd.DataFrame({'Trainee':[477], 'Graduate':[1347], 'APS1':[70], 'APS2':[368], 'APS3':[1478], 'APS4':[1341], 'APS5':[1315], 'APS6':[1639], 'EL1':[811], 'EL2':[333], 'SES1':[55], 'SES2':[24], 'SES3':[4]})    
        
        col1, col2 = st.columns([0.85, 0.15], gap="small")
        for classification in engmt_Dec2020.columns:
            with col2:
                st.slider(f'{classification} (had {engmt_Dec2020[classification][0]} entrants in 2019)', min_value=0.0, max_value=3.0, value=1.0, step=0.1, key=f'mult_{classification}')
        engmt_Dec2020_mod = pd.DataFrame({'Trainee':[477*(st.session_state[f'mult_Trainee'])], 'Graduate':[1347*(st.session_state[f'mult_Graduate'])], 'APS1':[70*(st.session_state[f'mult_APS1'])], 'APS2':[368*(st.session_state[f'mult_APS2'])], 'APS3':[1478*(st.session_state[f'mult_APS3'])], 'APS4':[1341*(st.session_state[f'mult_APS4'])], 'APS5':[1315*(st.session_state[f'mult_APS5'])], 'APS6':[1639*(1+st.session_state[f'mult_APS6'])], 'EL1':[811*(st.session_state[f'mult_EL1'])], 'EL2':[333*(st.session_state[f'mult_EL2'])], 'SES1':[55*(st.session_state[f'mult_SES1'])], 'SES2':[24*(st.session_state[f'mult_SES2'])], 'SES3':[4*(st.session_state[f'mult_SES3'])]})    
        results = iterable_Markov_calc(state_t0=state_Dec2019, engmt=engmt_Dec2020_mod, prob_matr=adj_prob_matr, iterations=10, start_year=2019)
        # Tidy up results
        results = np.round(results, decimals=0)
        df_results = pd.DataFrame(results, columns=['Year', 'Trainee', 'Graduate', 'APS1', 'APS2', 'APS3', 'APS4', 'APS5', 'APS6', 'EL1', 'EL2', 'SES1', 'SES2', 'SES3', 'Wasteage'], dtype=np.int32)
        df_results['Year'] = df_results['Year'].astype("string")
        df_results.drop(['Wasteage'], axis=1, inplace=True)
        df_results_long = pd.melt(df_results, id_vars=['Year'], var_name='Classification', value_name='Headcount')
        # Plotly filled area chart of the results
        fig1 = px.area(df_results_long, x="Year", y="Headcount", color="Classification", width=2400, height=800, 
                    title="Simple Markov model of ongoing APS employees") # Stacked column chart
        fig1.update_traces(mode="markers+lines", hovertemplate=None)
        fig1.update_layout(hovermode="x unified")
        with col1:
            st.plotly_chart(fig1, use_container_width=True)



    with st.expander("Modelling EV adoption with Fisher-Pry models"):
        st.markdown(r'''
                    Electric vehicles (EVs) are an emerging technology with the potential to replace combustion engine vehicles. Inspired by biological models of competition, if we assume that the rate of change in the fraction of EVs (denoted $f$) is proportional to the fraction of EVs and the remaining fraction of the market yet to be substituted, we have the ordinary differential equation
                    $$
                    \begin{align}
                    \frac{df}{dt} &= b f(1 - f) 
                    \end{align}
                    $$
                    Noting that this ODE is separable, with the help of an integral table it can be solved as follows
                    $$
                    \begin{align*}
                    \int \frac{1}{f(1-f)} \,df &= \int b \,dt \\
                    \ln\frac{f}{1-f} &= a + bt \tag{2}\\
                    \frac{f}{1-f} &= e^{(a + bt)} \\ 
                    f &= e^{(a + bt)} - fe^{(a + bt)} \\
                    f + fe^{(a + bt)} &= e^{(a + bt)} \\
                    f(1 + e^{(a + bt)}) &= e^{(a + bt)} \\
                    f &= \frac{e^{(a + bt)}}{1+e^{(a + bt)}} \\
                    &= \frac{1}{1 + e^{-(a + bt)}} \tag{3}
                    \end{align*}
                    $$
                    
                    Applying this model to technological substitution was introduced by Fisher and Pry in their relatively accessible _A Simple Substitution Model of Technological Change_.
                    
                    To apply this model we can use the equation at $(2)$ to determine the parameters $(a, b)$. In particular, collect data measuring $f$ and transform that according to the left hand side of the equation, then as indicated by the right hand side we need to fit a straight line to this. For example, the proportion of EVs (Electric and plug-in hybrid) in the Australian Capital Territory can be calculated from the data at this [link](https://www.data.act.gov.au/Transport/Total-vehicles-registered-in-the-ACT/x4hp-vihn). The semilog plot of $f/(1-f)$ is
                    

                    ''')
        fig0 = pio.read_json("media/EV_fig0_json")
        fig0.update_layout(yaxis=dict(title=dict(text='f/(1-f)'), title_font=dict(size=20)), xaxis=dict(title=dict(text='Date'),title_font=dict(size=16)))
        st.plotly_chart(fig0, use_container_width=True)
        st.markdown(r'''
                    In particular, focus on the blue points from mid-2019 where it appears that EV adoption is taking effect. Fitting a straight line to this region is plotted below and returned the parameters $(a,b)=(-6.291, 0.054)$.
                    ''')
        fig1 = pio.read_json("media/EV_fig1_json")
        fig1.update_layout(xaxis=dict(range=[0, 44]), yaxis=dict(range=[-6.3, -4]))
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown(r'''
                    These parameters give the model plotted as a line below. The data has been plotted as circles too and it is evident that the model is a good fit. The model suggests that EVs might make up $50\%$ of cars in the second half of 2029. It is likely that this estimate is sooner than should be expected since population growth has not been factored into this model and cars have a long lifespan.
                    ''')
        fig2 = pio.read_json("media/EV_fig2_json")
        st.plotly_chart(fig2, use_container_width=True)

    with st.expander("Modelling infectious diseases with SEIRV models"):
            st.markdown(r'''
                        Infectious disease modelling informs decision making during disease outbreaks. It is likely this topic is now a canonical example in courses on mathematical modeling. 
                        The following set of ordinary differential equations is known as the SEIRV model: susceptible, exposed, infected, recovered, vaccinated. 
                        $$
                        \begin{align*}
                        \frac{dS}{dt} &= \mu N - \frac{\beta S I}{N} - \mu S - \kappa S &\quad \frac{dE}{dt}&=\frac{\beta S I }{N} - \sigma E - \mu E &\quad \frac{dI}{dt} &= \sigma E - \mu I - \gamma I \\
                        \frac{dR}{dt}&=\gamma I - \mu R &\quad \frac{dV}{dt} &= \kappa S - \mu V 
                        \end{align*}
                        $$
                        An easier introduction to this model is to consider the following diagram, showing the movement of people between groups:
                        ''')
            st.image(Image.open("media/seirv_flow.png"), caption='SEIRV flow diagram')
            st.markdown(r'''
                        In this model people start out as susceptible to the disease, there is a rate at which people are exposed, and if so a period before becoming infectious and then a recovery rate for moving into the recovered group. 
                        Some of the simplifications in this formulation of the model are worth noting: the rate of births is equal to deaths, and the rate of dying is the same for each group (\mu), only people who are susceptible are vaccinated (at a rate of \kappa), and people who have recovered cannot be re-infected. 
                        Such a model will be appropriate for modelling some diseases but would need refinement for others.

                        With the following parameters the SEIRV model formulated here results in the following forecast
                        ''')
            col1, col2, col3 = st.columns(3)
            with col1:
                i0 = st.number_input('Set the initial number of infections', value=100, min_value=0, max_value=25_000_000, step=10_000)
                beta = st.number_input('Set the transmission parameter', value=0.6, min_value=0.0, max_value=1.0,  step=0.1)
            with col2:
                sigma = 1 / st.number_input('Set the latent period (number of days)', value=3, min_value=0, max_value=14, step=1)
                gamma = 1 / st.number_input('Set the recovery period (number of days)', value=7, min_value=0, max_value=21, step=1)
            with col3:
                kappa = st.number_input('Set the percentage of the susceptible population vaccinated per day', value=0.3, min_value=0.0, max_value=100.0, step=0.1) / 100
            mu = 1 / (75*365)           # Birth / death rate (per day)
            T = 365                     # Number of days over which to model
            N = 25_000_000              # Total population size
            y_df = solve_SEIRV(i0, mu, beta, sigma, gamma, kappa, T, N)
            seirv_fig = make_plot(y_df)
            st.plotly_chart(seirv_fig, use_container_width=True)
            st.markdown(r'''
            The Python code to produce this plot is 
                        ''')
            st.code('''
            import numpy as np
            from scipy.integrate import odeint
            import plotly.express as px
            import pandas as pd


            def define_SEIRV(y, t, mu, kappa, beta, gamma, sigma, N):

                # Function defining the SEIRV model.

                S, E, I, R, V = y
                dS = mu*N - (beta*S*I/N) - mu*S - kappa*S
                dE = (beta*S*I/N) - sigma*E - mu*E
                dI = sigma*E - mu*I - gamma*I
                dR = gamma*I - mu*R
                dV = kappa*S - mu*V
                
                return [dS, dE, dI, dR, dV]


            def solve_SEIRV(i0, mu, beta, sigma, gamma, kappa, T, N):
                
                # Function to solve the SEIRV model using odeint from scipy.integrate.

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
                fig.show()
                return fig
            
        # Define the input parameters and then run
            y_df = solve_SEIRV(i0, mu, beta, sigma, gamma, kappa, T, N)
            seirv_fig = make_plot(y_df)
            ''', language="python")

Data_Projects_page()
