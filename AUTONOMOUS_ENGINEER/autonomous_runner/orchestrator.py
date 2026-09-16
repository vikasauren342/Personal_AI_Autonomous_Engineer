import json
from pathlib import Path
from .checkpoint import Checkpoint
from .milestone_manager import inspect_project, discover_current_notebook, next_milestone
from .verifier import verify
from .model_agent import local_qwen, extract_json
from .repair_engine import diagnose
from .safety import require_manual
from .audit import audit

class AutonomousRunner:
    def __init__(self, root):
        self.root=Path(root).resolve(); self.project=Path(__import__('os').environ.get('PERSONAL_AI_PROJECT', str(self.root.parent/'Personal_AI_AGI_Core_v3_0'))).resolve()
        self.notebook=(self.root/'latest_kaggle_notebook.ipynb').resolve(); self.cp=Checkpoint(self.root); self.state=self.cp.load()
        self.goal=json.loads((self.root/'goal.json').read_text()) if (self.root/'goal.json').exists() else {}
        self.config=json.loads((self.root/'config.json').read_text()) if (self.root/'config.json').exists() else {}
    def audit(self):
        result=audit(self.project); self.cp.event(self.state,'RECOVERY_AUDIT',result=result); return result
    def model_plan(self,milestone,verification):
        prompt=f'''Goal:\n{json.dumps(self.goal,indent=2)}\nMilestone:\n{milestone}\nProject:\n{json.dumps(inspect_project(self.project),indent=2)}\nVerification:\n{json.dumps(verification,indent=2)}\nReturn JSON with objective, steps, files_to_create, files_to_modify, tests_to_add, acceptance_tests, manual_approval_required. Keep the change small and never touch protected foundation files.'''
        raw=local_qwen([{"role":"system","content":"Conservative autonomous software engineer. JSON only."},{"role":"user","content":prompt}],max_new_tokens=900)
        return extract_json(raw)
    def run_once(self):
        audit_result=self.audit()
        if audit_result['status']!='PASS':
            require_manual('Recovery audit is not clean; resolve/reconcile source state before autonomous implementation.',self.root)
            return {'status':'MANUAL_STOP','audit':audit_result}
        nb=discover_current_notebook(self.notebook); milestone=next_milestone(self.state,nb); self.state['current_milestone']=milestone; self.cp.save(self.state)
        baseline=verify(self.project); self.cp.event(self.state,'BASELINE',milestone=milestone,result=baseline)
        if not baseline['passed']:
            diagnosis=diagnose(self.goal,baseline,inspect_project(self.project)); require_manual('Baseline verification failed.',self.root); return {'status':'MANUAL_STOP','milestone':milestone,'baseline':baseline,'diagnosis':diagnosis}
        try: plan=self.model_plan(milestone,baseline)
        except Exception as e: require_manual(f'Planner unavailable: {type(e).__name__}: {e}',self.root); return {'status':'MANUAL_STOP','reason':'planner_unavailable'}
        self.cp.event(self.state,'PLAN',milestone=milestone,plan=plan)
        report={'status':'PLAN_READY','milestone':milestone,'plan':plan,'message':'Use the bounded patch adapter to implement; protected foundation remains gated.'}
        (self.root/'reports').mkdir(exist_ok=True); (self.root/'reports'/f'{milestone.replace("/","_")}.json').write_text(json.dumps(report,indent=2))
        return report
