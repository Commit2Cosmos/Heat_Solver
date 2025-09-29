# 2D Heat Transfer Solver


## Theory

$
\dfrac{\partial u}{\partial t} = \alpha 
\left( 
\dfrac{\partial^2 u}{\partial x^2} +
\dfrac{\partial^2 u}{\partial y^2}
\right)
$

where:
- $u(x,y,t)$ is the temperature field,
- $t$ is the temporal variable
- $x, y$ are the spatial variables
- $\alpha$ is the thermal diffusivity.
<br><br><br>



$
f^{'} \approx 
\dfrac{f(a+h) - f(a)}{\Delta h}
$<br><br>

In finite-difference method, we are going to “discretize” the spatial domain and the time interval. Hence the solution we want to find is $u(x,y,t)=u_{i,j}^{k}$ everywhere in $x$ and $y$ and over $t$.


Substituting 


$
\dfrac{u^{k+1}_{i,j} - u^{k}_{i,j}}{\Delta t} = \alpha \left(\dfrac{u^{k}_{i+1,j} - 2u^{k}_{i,j} + u^{k}_{i-1,j}}{\Delta x^2} + \dfrac{u^{k}_{i,j+1} - 2u^{k}_{i,j} + u^{k}_{i,j-1}}{\Delta y^2} \right)
$

If we take $\Delta x = \Delta y$, the equation becomes:

$
u^{k+1}_{i,j} = \gamma \left(
u^{k}_{i+1,j} + u^{k}_{i-1,j} + u^{k}_{i,j+1} + u^{k}_{i,j-1} - 4u^{k}_{i,j}
\right) + u^{k}_{i,j}
$


where

$\gamma = \alpha \dfrac{\Delta t}{\Delta x^2}$


Hence, the value at a particular point in space depends on what it and all the neighbouring values were in the previous timestep.


### Stability Analysis


I will use von Neumann stability analysis to derive the acceptable range of values for $\Delta t$. It is a way to test whether small errors/perturbations decay or grow as values are updated over time. The intuition behind this method is that sines and cosines form a complete basis on a uniform grid, so we want to check how the scheme updates a pure wave $e^{i(k_x x + k_y y)}$.


1. Assume a single Fourier mode solution (anzats)
$u^{k}_{i,j} = G^{\,k}\,\hat{u}\,e^{\mathrm{i}(i\theta + j\phi)}$,
with $\theta=k_x\Delta x$, $\phi=k_y\Delta x$, $\mathrm{i}=\sqrt{-1}$, and $G$ is the amplification factor per time step. $|G| < 1$ signals that the mode is stable; $|G| > 1$ that the mode grows exponentially. Hence, we need to check that all Fourier modes have $|G| < 1$. 

1. Evaluate neighbour values:
$u^{k}_{i\pm1,j}=u^{k}_{i,j}e^{\pm\mathrm{i}\theta},
u^{k}_{i,j\pm1}=u^{k}_{i,j}e^{\pm\mathrm{i}\phi}.$

1. Substitute into the update and divide by $u^{k}_{i,j}$ to obtain
$G = 1 + \gamma\bigl(e^{\mathrm{i}\theta}+e^{-\mathrm{i}\theta}+e^{\mathrm{i}\phi}+e^{-\mathrm{i}\phi}-4\bigr).$

1. Use $e^{\mathrm{i}\theta}+e^{-\mathrm{i}\theta}=2\cos\theta$ to simplify:
$G = 1 - 4\gamma + 2\gamma\bigl(\cos\theta + \cos\phi\bigr).$

The scheme is stable if $|G|\le 1$ or $-1\le G\le 1$ for all wavenumbers $\theta,\phi$. The quantity $\cos\theta+\cos\phi$ ranges between $-2$ and $+2$. The worst case occurs at maximum wave oscillation i.e. at maximum and minimum cosine values. Hence,
$G_{\max}=1-4\gamma+2\gamma(2)=1$ and $G_{\min}=1-4\gamma+2\gamma(-2)=1-8\gamma$.

Enforce $G_{\min}\ge -1$:

$1-8\gamma \ge -1 \quad\Rightarrow\quad \gamma \le \tfrac{1}{4}.$

Therefore the stability condition is
$\displaystyle \gamma=\alpha\frac{\Delta t}{\Delta x^2}\le \frac{1}{4},$
or
$\displaystyle \Delta t \le \frac{\Delta x^2}{4\alpha}.$



## Project Structure

TODO


## Bugs

- Doesn't work for central heating point
- Neumann doesn't produce smooth heat transfer cz grid is updated bottom to top, left to right
- Dirichlet doesn't update sides i.e. walls that should get heated remain cold affecting further heat distribution