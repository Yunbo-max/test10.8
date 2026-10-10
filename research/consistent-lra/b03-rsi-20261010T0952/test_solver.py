"""Numerical unit checks only; these arrays are not scientific benchmarks."""
import os
for _k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_k]='1'
import importlib.util, pathlib, sys, unittest
import numpy as np
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'continuation-11'))
import matrix_study as ms

class SolverChecks(unittest.TestCase):
    def solver(self):
        self.assertIsNotNone(importlib.util.find_spec('fast_boundary'),'new root solver module must exist')
        import fast_boundary
        return fast_boundary

    def test_rank_one_closed_form_and_feasibility(self):
        s=self.solver();G=np.diag([1.,10.]);E=11.;Q=np.array([[1.],[0.]]);V=np.array([[0.],[1.]])
        W,fb=s.boundary_path(Q,V,G,E,1.5,1e-9)
        expected=np.array([[np.sqrt(.5/9)],[np.sqrt(1-.5/9)]])
        self.assertLess(np.linalg.norm(W@W.T-expected@expected.T),1e-7)
        self.assertLessEqual(E-float(np.sum(W*(G@W))),1.5+1e-9)

    def test_derivative_is_of_direct_matrix_loss(self):
        s=self.solver();rng=np.random.default_rng(100)
        for d,k in ((7,2),(7,5),(5,3)):
            Z=np.linalg.qr(rng.normal(size=(d,d)))[0];G=Z@np.diag(np.arange(1,d+1))@Z.T
            Q=np.linalg.qr(rng.normal(size=(d,k)))[0];V=Z[:,-k:]
            p=s.coefficients(Q,V,G,float(np.trace(G)))
            for a in (.13,.47,.81):
                loss,der=s.value_derivative(p,a)
                W=p['B']*np.cos(a*p['angles'])+p['U']*np.sin(a*p['angles'])
                direct=np.trace(G)-np.trace(W.T@G@W)
                h=1e-5;fd=(s.value_derivative(p,a+h)[0]-s.value_derivative(p,a-h)[0])/(2*h)
                self.assertAlmostEqual(loss,direct,places=10)
                self.assertLess(abs(der-fd),2e-7)

    def test_shared_tied_and_zero_opt_preserve_legacy(self):
        s=self.solver()
        fixtures=[(np.diag([1.,2.,3.,4.]),np.eye(4)[:,[0,2,3]],np.eye(4)[:,[1,2,3]],1.01),
                  (np.diag([1.,1.,3.,3.]),np.eye(4)[:,[0,2]],np.eye(4)[:,[2,3]],2.1),
                  (np.diag([0.,0.,4.]),np.eye(3)[:,[0]],np.eye(3)[:,[2]],0.)]
        for G,Q,V,target in fixtures:
            E=float(np.trace(G));tol=1e-10*max(1.,E)
            W,fb=s.boundary_path(Q,V,G,E,target,tol);R,rf=ms.boundary_path(Q,V,G,E,target,tol)
            self.assertLess(np.linalg.norm(W@W.T-R@R.T),5e-7)
            self.assertLess(np.linalg.norm(W.T@W-np.eye(W.shape[1])),1e-8)
            self.assertLessEqual(E-float(np.sum(W*(G@W))),target+tol)

if __name__=='__main__':unittest.main()
