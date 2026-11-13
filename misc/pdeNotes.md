# Worked Exercises: Separation of Variables  
## Based on the Standard Eigenvalue Problems and Separation Setups  
*(from the quick-reference tables on eigenvalue problems and separation of variables)*

These exercises walk through the complete process for the main cases:  
1. Separate variables  
2. Apply boundary conditions to obtain the eigenvalue problem  
3. Find eigenvalues and eigenfunctions  
4. Solve the remaining ODE  
5. Superpose to form the infinite series  
6. Apply initial/boundary data to fix coefficients  

All notation uses `$...$` (inline) and `$$...$$` (display) so it pastes cleanly into Markdown.

---

# Expanded Reasoning: Why $\lambda_n = \bigl(\frac{n\pi}{L}\bigr)^2$ and Why $\omega_n = \frac{n\pi c}{L}$

This is a fully expanded version of **Exercise 1** (wave equation, Dirichlet ends).  
Every algebraic step and the underlying reason is shown.

---

## The Problem

$$
u_{tt} = c^2 u_{xx}, \qquad 0 < x < L,\quad t > 0,
$$
$$
u(0,t) = 0, \qquad u(L,t) = 0,
$$
$$
u(x,0) = \phi(x), \qquad \frac{\partial}{\partial t}\left[u(x,0)\right]asdf = u_t(x,0) = \psi(x).
$$

---

## Step 1 – Separation of Variables

We look for solutions of the special form
$$
u(x,t) = X(x)\,T(t).
$$
(This is not the most general solution; it is a convenient family of solutions we can later superpose.)

Substitute into the PDE:
$$
X(x)\,T''(t) = c^2 X''(x)\,T(t).
$$
Assuming $X T \neq 0$, divide both sides by $c^2 X T$:
$$
\frac{T''(t)}{c^2 T(t)} = \frac{X''(x)}{X(x)}.
$$
The left side depends only on $t$; the right side depends only on $x$.  
The only way two functions of different independent variables can be equal for all $x$ and $t$ is if both are equal to the same constant. Call that constant $-\lambda$:
$$
\frac{X''(x)}{X(x)} = -\lambda, \qquad \frac{T''(t)}{c^2 T(t)} = -\lambda.
$$
(The minus sign is chosen for later convenience; $\lambda$ itself may turn out positive, zero, or negative.)

This immediately gives the pair of ordinary differential equations
$$
X'' + \lambda X = 0, \qquad T'' + c^2\lambda\, T = 0.
$$

---

## Step 2 – The Spatial Eigenvalue Problem

The boundary conditions $u(0,t)=0$ and $u(L,t)=0$ for all $t$ force
$$
X(0) = 0, \qquad X(L) = 0
$$
(assuming $T\not\equiv 0$).

We therefore solve
$$
X'' + \lambda X = 0, \qquad X(0)=X(L)=0.
$$

### Case $\lambda < 0$
Write $\lambda = -\mu^2$ with $\mu>0$. The general solution is
$$
X(x) = A\cosh(\mu x) + B\sinh(\mu x).
$$
$X(0)=0$ forces $A=0$.  
Then $X(L)=B\sinh(\mu L)=0$. Since $\sinh(\mu L)\neq 0$, we must have $B=0$.  
Only the trivial solution. Discard $\lambda<0$.

### Case $\lambda = 0$
$X''=0$ so $X(x)=Ax+B$.  
$X(0)=0$ $\Rightarrow$ $B=0$.  
$X(L)=AL=0$ $\Rightarrow$ $A=0$.  
Trivial solution. Discard $\lambda=0$.

### Case $\lambda > 0$
Write $\lambda = \mu^2$ with $\mu>0$. The general solution is
$$
X(x) = A\cos(\mu x) + B\sin(\mu x).
$$
$X(0)=0$ forces $A=0$, so
$$
X(x) = B\sin(\mu x).
$$
Now impose $X(L)=0$:
$$
B\sin(\mu L) = 0.
$$
For a non-trivial solution ($B\neq 0$) we need
$$
\sin(\mu L) = 0 \quad\Rightarrow\quad \mu L = n\pi, \quad n=1,2,3,\dots
$$
(The integer $n=0$ gives the zero function; negative $n$ simply duplicates the positive ones.)

Thus
$$
\mu_n = \frac{n\pi}{L}, \qquad \lambda_n = \mu_n^2 = \left(\frac{n\pi}{L}\right)^2.
$$
The corresponding eigenfunctions are
$$
X_n(x) = \sin\left(\frac{n\pi x}{L}\right)
$$
(up to a non-zero multiplicative constant, which we conventionally take to be 1).

**Intuition.**  
These are exactly the spatial shapes that can “fit” between two fixed ends: an integer number of half-waves. Any other wavelength would not vanish at both $x=0$ and $x=L$ simultaneously.

---

## Step 3 – The Time Factors and the Frequency $\omega_n$

For each eigenvalue $\lambda_n$ the time equation becomes
$$
T'' + c^2\lambda_n\, T = 0,
$$
i.e.
$$
T'' + \left(c\cdot\frac{n\pi}{L}\right)^2 T = 0.
$$
This is the equation of simple harmonic motion. Its general solution is
$$
T_n(t) = A_n\cos(\omega_n t) + B_n\sin(\omega_n t),
$$
where the angular frequency is precisely
$$
\omega_n = c\sqrt{\lambda_n} = c\cdot\frac{n\pi}{L} = \frac{n\pi c}{L}.
$$

**Why this value?**  
From the separated equation we already had
$$
\frac{T''}{T} = -c^2\lambda.
$$
Once $\lambda$ is fixed by the spatial problem, the constant on the right is known, and the oscillation rate of $T$ is forced to be $\sqrt{c^2\lambda}$.  
Physically, shorter spatial waves (larger $n$) have higher temporal frequencies—the classic dispersion relation for the wave equation.

---

## Step 4 – Product Solutions and Superposition

Each pair $(X_n,T_n)$ produces a solution
$$
u_n(x,t) = \sin\left(\frac{n\pi x}{L}\right)\bigl(A_n\cos(\omega_n t)+B_n\sin(\omega_n t)\bigr).
$$
Because the PDE is linear and homogeneous, any finite linear combination of these $u_n$ is again a solution. Under mild convergence assumptions the infinite sum
$$
u(x,t) = \sum_{n=1}^\infty \sin\left(\frac{n\pi x}{L}\right)\bigl(A_n\cos(\omega_n t)+B_n\sin(\omega_n t)\bigr)
$$
is also a solution.

---

## Step 5 – Initial Conditions Fix the Coefficients

- At $t=0$:
  $$
  u(x,0) = \sum_{n=1}^\infty A_n\sin\left(\frac{n\pi x}{L}\right) = \phi(x).
  $$
  This is the Fourier sine series of $\phi$ on $(0,L)$, so
  $$
  A_n = \frac{2}{L}\int_0^L\phi(x)\sin\left(\frac{n\pi x}{L}\right)\,dx.
  $$

- Differentiating the series and setting $t=0$ likewise determines the $B_n$ from $\psi$.

---

## Summary of the Logical Chain

1. Product assumption $\Rightarrow$ separation constant $-\lambda$.  
2. Boundary conditions $X(0)=X(L)=0$ force $\lambda$ to be one of the discrete values $(n\pi/L)^2$.  
3. Those same numbers, when inserted into the time equation, produce the frequencies $\omega_n = n\pi c/L$.  
4. Linearity lets us add every such mode.  
5. Initial data pick the amplitudes via Fourier coefficients.

The formula $\lambda_n=(n\pi/L)^2$ is therefore not an arbitrary choice; it is the unique set of numbers that let a non-trivial sinusoidal function vanish at both ends of the interval.

---

## Exercise 2 – Heat Equation, Neumann Boundary Conditions  
*(Case: $X'(0)=X'(L)=0$)*

**Problem**  
Solve
$$
u_t = k u_{xx}, \qquad 0 < x < L,\quad t > 0,
$$
$$
u_x(0,t) = u_x(L,t) = 0,
$$
$$
u(x,0) = \phi(x).
$$

**Solution**

**Separation.** $u = X(x)T(t)$ yields
$$
\frac{T'}{kT} = \frac{X''}{X} = -\lambda.
$$

**Eigenvalue problem.** $X'(0) = X'(L) = 0$ gives
$$
\lambda_n = \left(\frac{n\pi}{L}\right)^2, \qquad X_n(x) = \cos\left(\frac{n\pi x}{L}\right), \quad n = 0,1,2,\dots
$$
(Note the $n=0$ constant eigenfunction is included.)

**Time factors.**
$$
T_n(t) = A_n e^{-k\lambda_n t}.
$$

**Superposition.**
$$
u(x,t) = A_0 + \sum_{n=1}^\infty A_n \cos\left(\frac{n\pi x}{L}\right) e^{-k(n\pi/L)^2 t}.
$$

**Coefficients.**
$$
A_0 = \frac{1}{L} \int_0^L \phi(x)\,dx,
$$
$$
A_n = \frac{2}{L} \int_0^L \phi(x)\cos\left(\frac{n\pi x}{L}\right)\,dx \quad (n\ge 1).
$$

---

## Exercise 3 – Wave Equation, Mixed Boundary Conditions  
*(Case: $X(0)=X'(L)=0$)*

**Problem**  
Solve
$$
u_{tt} = c^2 u_{xx}, \qquad 0 < x < L,\quad t > 0,
$$
$$
u(0,t) = 0, \qquad u_x(L,t) = 0,
$$
$$
u(x,0) = \phi(x), \qquad u_t(x,0) = 0.
$$

**Solution**

**Separation.** Same as Exercise 1:
$$
X'' + \lambda X = 0, \qquad T'' + c^2\lambda T = 0.
$$

**Eigenvalue problem.** Conditions $X(0)=0$, $X'(L)=0$ produce
$$
\lambda_n = \left( \frac{(n-\tfrac12)\pi}{L} \right)^2, \qquad X_n(x) = \sin\left( \frac{(n-\tfrac12)\pi x}{L} \right), \quad n=1,2,3,\dots
$$

**Time factors.** Because $u_t(x,0)=0$,
$$
T_n(t) = A_n \cos(\omega_n t), \qquad \omega_n = c\sqrt{\lambda_n}.
$$

**Superposition.**
$$
u(x,t) = \sum_{n=1}^\infty A_n \sin\left( \frac{(n-\tfrac12)\pi x}{L} \right) \cos(\omega_n t).
$$

**Coefficients.** The eigenfunctions are orthogonal on $[0,L]$ with norm $L/2$:
$$
A_n = \frac{2}{L} \int_0^L \phi(x) \sin\left( \frac{(n-\tfrac12)\pi x}{L} \right)\,dx.
$$

---

## Exercise 4 – Laplace Equation on a Rectangle (Dirichlet)  
*(Separation setup from the quick guide)*

**Problem**  
Solve
$$
u_{xx} + u_{yy} = 0, \qquad 0 < x < a,\quad 0 < y < b,
$$
$$
u(0,y) = u(a,y) = 0, \qquad u(x,0) = 0, \qquad u(x,b) = f(x).
$$

**Solution**

**Separation.** $u = X(x)Y(y)$ yields
$$
\frac{X''}{X} = -\frac{Y''}{Y} = -\lambda.
$$

**Eigenvalue problem in $x$.** $X(0)=X(a)=0$ gives
$$
\lambda_n = \left(\frac{n\pi}{a}\right)^2, \qquad X_n(x) = \sin\left(\frac{n\pi x}{a}\right), \quad n=1,2,\dots
$$

**$Y$ equation.** 
$$
Y'' - \lambda_n Y = 0 \quad\Rightarrow\quad Y_n(y) = A_n \cosh(\mu_n y) + B_n \sinh(\mu_n y), \quad \mu_n = \frac{n\pi}{a}.
$$
The condition $u(x,0)=0$ forces $A_n=0$.

**Superposition.**
$$
u(x,y) = \sum_{n=1}^\infty B_n \sin\left(\frac{n\pi x}{a}\right) \sinh\left(\frac{n\pi y}{a}\right).
$$

**Coefficients.** At $y=b$,
$$
B_n \sinh\left(\frac{n\pi b}{a}\right) = \frac{2}{a}\int_0^a f(x)\sin\left(\frac{n\pi x}{a}\right)\,dx,
$$
so
$$
B_n = \frac{2}{a\sinh(n\pi b/a)} \int_0^a f(x)\sin\left(\frac{n\pi x}{a}\right)\,dx.
$$

---

## Exercise 5 – Heat Equation, Mixed Boundary Conditions  
*(Case: $X'(0)=X(L)=0$)*

**Problem**  
Solve
$$
u_t = k u_{xx}, \qquad 0 < x < L,\quad t > 0,
$$
$$
u_x(0,t) = 0, \qquad u(L,t) = 0,
$$
$$
u(x,0) = \phi(x).
$$

**Solution**

**Separation.** Same heat-equation separation as before.

**Eigenvalue problem.** $X'(0)=0$, $X(L)=0$ yields
$$
\lambda_n = \left(\frac{(n-\tfrac12)\pi}{L}\right)^2, \qquad X_n(x) = \cos\left(\frac{(n-\tfrac12)\pi x}{L}\right), \quad n=1,2,\dots
$$

**Time factors.**
$$
T_n(t) = A_n e^{-k\lambda_n t}.
$$

**Superposition.**
$$
u(x,t) = \sum_{n=1}^\infty A_n \cos\left(\frac{(n-\tfrac12)\pi x}{L}\right) e^{-k\lambda_n t}.
$$

**Coefficients.**
$$
A_n = \frac{2}{L} \int_0^L \phi(x) \cos\left(\frac{(n-\tfrac12)\pi x}{L}\right)\,dx.
$$

---

## Exercise 6 – Fourth-Order Beam / Wave-Type Equation  
*(From the fourth-order eigenvalue table)*

**Problem**  
Solve the vibrating beam equation
$$
u_{tt} = -k u_{xxxx}, \qquad 0 < x < L,\quad t > 0,
$$
with simply-supported ends
$$
u(0,t)=u(L,t)=0, \qquad u_{xx}(0,t)=u_{xx}(L,t)=0,
$$
and initial data $u(x,0)=\phi(x)$, $u_t(x,0)=0$.

**Solution**

**Separation.** $u=X(x)T(t)$ leads to
$$
\frac{T''}{kT} = -\frac{X''''}{X} = -\lambda.
$$
Thus
$$
X'''' - \lambda X = 0, \qquad T'' + k\lambda T = 0.
$$

**Eigenvalue problem.** The boundary conditions give
$$
\lambda_n = \left(\frac{n\pi}{L}\right)^4, \qquad X_n(x) = \sin\left(\frac{n\pi x}{L}\right), \quad n=1,2,\dots
$$

**Time factors.** With zero initial velocity,
$$
T_n(t) = A_n \cos(\omega_n t), \qquad \omega_n = \sqrt{k}\,\left(\frac{n\pi}{L}\right)^2.
$$

**Superposition.**
$$
u(x,t) = \sum_{n=1}^\infty A_n \sin\left(\frac{n\pi x}{L}\right) \cos(\omega_n t),
$$
where
$$
A_n = \frac{2}{L}\int_0^L \phi(x)\sin\left(\frac{n\pi x}{L}\right)\,dx.
$$

---

## Summary of Eigenfunction Families Used

| Boundary conditions              | Eigenvalues                          | Eigenfunctions                          |
|----------------------------------|--------------------------------------|-----------------------------------------|
| $X(0)=X(L)=0$                    | $(n\pi/L)^2$                         | $\sin(n\pi x/L)$                        |
| $X'(0)=X'(L)=0$                  | $(n\pi/L)^2$ ($n=0,1,\dots$)         | $\cos(n\pi x/L)$                        |
| $X(0)=X'(L)=0$                   | $\bigl((n-1/2)\pi/L\bigr)^2$         | $\sin((n-1/2)\pi x/L)$                  |
| $X'(0)=X(L)=0$                   | $\bigl((n-1/2)\pi/L\bigr)^2$         | $\cos((n-1/2)\pi x/L)$                  |
| Simply supported beam            | $(n\pi/L)^4$                         | $\sin(n\pi x/L)$                        |

These exercises cover every major case appearing in the standard eigenvalue tables and the separation-of-variables quick guide.  
Each one shows the complete chain from product assumption through the infinite series.