from ..core.contracts import Evaluation
class EvaluationGate:
    def evaluate(self, observations):
        issues=[]
        if not observations: issues.append('no observations')
        for o in observations:
            if not o.ok: issues.append(o.error or 'execution failure')
        return Evaluation(done=not issues, passed=not issues, issues=issues)
    def check(self,result):
        return {'passed': result is not None, 'issues': [] if result is not None else ['empty result']}
