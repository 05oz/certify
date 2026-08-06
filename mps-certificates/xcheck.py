# Fully independent cross-check: numpy dense Pauli build, no shared code with reverify.py
import numpy as np
X = np.array([[0,1],[1,0]], dtype=object)
Z = np.array([[1,0],[0,-1]], dtype=object)
I = np.array([[1,0],[0,1]], dtype=object)
A = {0: np.array([[1,0],[0,-1]], dtype=object),
     1: np.array([[-2,-1],[1,0]], dtype=object)}

def opat(op, site, L):
    m = np.array([[1]], dtype=object)
    for k in range(L):
        m = np.kron(m, op if k==site else I)
    return m

def buildH(L):
    dim = 1<<L
    H = np.zeros((dim,dim), dtype=object)
    for i in range(L):
        j = (i+1)%L
        Xi = opat(X, i, L)
        Xj = opat(X, j, L); Zj = opat(Z, j, L)
        term = (opat(I,i,L) + Xi) @ (Xj + Zj)
        H = H - term
    return H

def psivec(L):
    v = np.zeros(1<<L, dtype=object)
    for idx in range(1<<L):
        bits = [(idx>>(L-1-k))&1 for k in range(L)]
        M = np.array([[1,0],[0,1]], dtype=object)
        for s in bits:
            M = M @ A[s]
        v[idx] = M[0,0] + M[1,1]
    return v

print("Independent numpy cross-check (dense Pauli H, exact integer object dtype):")
for L in range(3,10):
    H = buildH(L)
    v = psivec(L)
    Hv = H @ v
    nz = any(x!=0 for x in v)
    zero = all(x==0 for x in Hv)
    # also confirm H is symmetric (Hermitian, real)
    sym = all(H[a,b]==H[b,a] for a in range(1<<L) for b in range(1<<L))
    print(f"  L={L}: psi nonzero={nz}, H@psi==0 exactly={zero}, H symmetric={sym}, ||psi||^2={int(sum(x*x for x in v))}")
