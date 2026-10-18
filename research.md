---
title: "Research"
permalink: /research/
---

## Conserved quantities

Define the loss of our optimization model:
$$\mathcal L: \text{Parameter}\times\text{Data}\to \mathbb R$$
And denote the parameter as $\theta$.

We are trying to find an operator $G:\text{Parameter}\to\text{Parameter}$, and it remains:
$$\mathcal L(\theta)=\mathcal L(G(\theta))$$

Denote a differentiable action $\phi:\theta\to\phi(\theta,g)$, where $g\in G$. So it holds:
$$<\nabla f,\partial_{\alpha}\phi|_{\alpha = I}>=0$$

## Some work done during Independent Study course

### Singular Values and Integer Powersof Accretive Matrices
Consider any accretive matrix $A \in \mathbb R^{n \times n}$, which means for any $x \in \mathbb R^n$ we have $x^T A x>0$. Do we have a universal bound constant $c$ s.t. 
$$\sigma (A)^2 \le 2 \sigma (A^2)?$$
What about for cubic? Fourth power...?
This notes deals with the question.
- [Singular Values and Integer Powersof Accretive Matrices](report.pdf)

I've proved that there exists a universal constant $c =2$ s.t.
$$\sigma (A)^2 \le 2 \sigma (A^2)\quad\text{for all }n\in \mathbb N$$
Also, for every $k \in \mathbb N$, there exists a bound:
$$\sigma(A)^k\leq 2^{k(k-1)/2}\sigma(A^k)$$