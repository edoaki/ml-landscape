"""Check the mathematical claims behind the Flow Matching illustrations."""
import math
from pathlib import Path
import sys
import unittest

SOURCE=Path(__file__).resolve().parents[1]/'source'
sys.path.insert(0,str(SOURCE))
import fm_figures as fm


def density(x,t):
    variance=(1-t)**2+(fm.SIGMA*t)**2
    return sum(math.exp(-sum((x[j]-t*m[j])**2 for j in range(2))/(2*variance))/(2*math.pi*variance) for m in fm.MEANS)/2


class FlowExample(unittest.TestCase):
    def test_velocity_satisfies_continuity_equation(self):
        eps=1e-5
        for t in [.1,.5,.9]:
            for x in [[0,0],[.4,.2],[-1.5,.6],[2,1]]:
                dt=(density(x,t+eps)-density(x,t-eps))/(2*eps)
                divergence=0
                for j in range(2):
                    a=x[:];b=x[:];a[j]+=eps;b[j]-=eps
                    divergence+=(density(a,t)*fm.velocity(a,t)[0][j]-density(b,t)*fm.velocity(b,t)[0][j])/(2*eps)
                self.assertAlmostEqual(dt+divergence,0,places=7)

    def test_integrated_endpoints_preserve_mixture_quantiles(self):
        normal=lambda z:(1+math.erf(z/math.sqrt(2)))/2
        for start in [[.6,-.4],[-1,.4],[1,2],[-2,-1],[.01,.02]]:
            x=start[:]
            for i in range(400):x=fm.rk4(x,i/400,1/400)
            # Along the means' axis, the exact flow preserves the scalar CDF.
            projection=lambda p:(2*p[0]+p[1])/math.sqrt(5)
            end_cdf=sum(normal((projection(x)-m)/fm.SIGMA) for m in [-math.sqrt(5),math.sqrt(5)])/2
            self.assertAlmostEqual(normal(projection(start)),end_cdf,places=6)
            self.assertAlmostEqual((-x[0]+2*x[1]),fm.SIGMA*(-start[0]+2*start[1]),places=6)

if __name__=='__main__':unittest.main()
