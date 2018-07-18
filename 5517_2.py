import numpy as np
import matplotlib.pyplot as plt
import cvxopt as opt
from cvxopt import blas, solvers
import pandas as pd
import os
from pandas import DataFrame as df
np.random.seed(123)

# Turn off progress printing
solvers.options['show_progress'] = False
os.chdir(r'C:\Users\qeaw\Desktop\5517')

price = pd.read_csv('proj_FINS5517.csv', parse_dates=True, index_col=0)


r0 = price.pct_change()

r1 = r0 + 1

r1 = r1.ix[:2517]

r_stock = r1.drop('SP500', axis = 1)
sp500 = r1['SP500']

n_obs = r_stock.shape[0]
n_assets = r_stock.shape[1]



# return_vec = np.random.randn(n_assets, n_obs)
return_vec = np.asmatrix(r_stock.T)


# plt.plot(return_vec.T, alpha=.4);
# plt.xlabel('time')
# plt.ylabel('returns')
#





def rand_weights(n):
    ''' Produces n random weights that sum to 1 '''
    k = np.random.rand(n)
    return k / sum(k)

def annualize(r):
    rcum = r.cumprod().ix[-1]
    rann = rcum ** (250.0/float(r.shape[0])) - 1
    rcov = (r-1).cov()
    covann = rcov * 250.0
    # covann.fillna(0.0)
    return rann, covann

def annua2(r):
    rcum = r.cumprod().ix[-1]
    rann = rcum ** (250.0 / float(r.shape[0])) - 1
    rdif = r - r.mean()
    cov = (np.asmatrix(rdif).T * np.asmatrix(rdif)) / float(r.shape[0])
    covann = cov * 250.0
    return rann, covann

rann, covann = annualize(r_stock)
rann2,covann2 = annua2(r_stock)
print rann
def random_portfolio(rann, covann):
    '''
    Returns the mean and standard deviation of returns for a random portfolio
    '''

    p = np.asmatrix(rann)
    w = np.asmatrix(rand_weights(covann.shape[0]))
    C = np.asmatrix(covann)
    # print 'p shape',p.shape
    # print 'wshape',w.shape
    mu = w * p.T
    # print 'mu', mu
    sigma = np.sqrt(w * C * w.T)

    # This recursion reduces outliers to keep plots pretty
    # if sigma > 2:
    #     return random_portfolio(returns)
    return mu, sigma

print random_portfolio(rann, covann)

n_portfolios = 500
means, stds = np.column_stack([
    random_portfolio(rann, covann)
    for _ in xrange(n_portfolios)
])
f1 = plt.figure('Mean and standard deviation of returns of generated portfolios')
ax = f1.add_subplot(1,1,1)
plt.plot(stds, means, 'o', markersize=5)
plt.xlabel('std')
plt.ylabel('mean')
plt.title('Mean and standard deviation of returns of generated portfolios')
print means
# print stds
#
# #
def optimal_portfolio(r1,rann, covann):
    r0 = r1- 1
    returns_vec = np.asmatrix(r0.T)

    n = len(returns_vec)

    print n
    N = 100
    mus = [(10 ** (5.0 * t / N - 1.0)) / 10 for t in range(N)]

    # Convert to cvxopt matrices

    # S = opt.matrix(np.asmatrix(r1.cov() * 250.0)) # fixed annualized cov matrix
    S = opt.matrix(np.asmatrix(covann))
    print covann.shape
    # pbar = opt.matrix(np.asmatrix((r1.cumprod().ix[-1] ** (250.0 / 2517.0) - 1.0)))   #  fixed retrun vec11 x 1
    pbar = opt.matrix(np.asmatrix(rann)).T

    print rann.T.shape
    print np.asmatrix(rann.T)
    print pbar
    # Create constraint matrices
    G = -opt.matrix(np.eye(n))  # negative n x n identity matrix
    h = opt.matrix(0.0, (n, 1))
    A = opt.matrix(1.0, (1, n))
    b = opt.matrix(1.0)

    # Calculate efficient frontier weights using quadratic programming
    portfolios = [solvers.qp(mu * S, -1 * pbar, G, h, A, b)['x']
                  for mu in mus]
    ## CALCULATE RISKS AND RETURNS FOR FRONTIER
    returns = [blas.dot(pbar, x) for x in portfolios]
    risks = [np.sqrt(blas.dot(x, S * x)) for x in portfolios]
    ## CALCULATE THE 2ND DEGREE POLYNOMIAL OF THE FRONTIER CURVE
    m1 = np.polyfit(returns, risks, 2)
    x1 = np.sqrt(m1[2] / m1[0])
    # CALCULATE THE OPTIMAL PORTFOLIO
    wt = solvers.qp(opt.matrix(x1 * S), -pbar, G, h, A, b)['x']
    return np.asarray(wt), returns, risks

weights, returns, risks = optimal_portfolio(r_stock,rann, covann)

plt.plot(stds, means, 'o')
plt.ylabel('mean')
plt.xlabel('std')



R = rann - 0.05
S = np.asmatrix(covann)
z = np.dot(S.I, R)
z1 = df(z)
w = [0 for _ in range(10)]
for i in range(10):
    w[i] = z1[i] / sum(z1)

w1 = np.asmatrix(w)

rrr = np.dot(rann.T , w1)

sigma = np.sqrt(np.dot(np.dot(w1.T , covann), w1))

slope = rrr / sigma

x = [i / 100.0 for i in range(30)]
y = [float(slope * i) + 0.05 for i in x]


ax.plot(risks, returns, 'y-o')
plt.xlim([0.15,0.3])
plt.ylim([0,0.2])
ax.plot(x, y,  'y')
print x
print y


print 'asdf'
plt.show()