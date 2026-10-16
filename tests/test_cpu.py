#!/usr/bin/env python3
from pathlib import Path
import csv,json,math,subprocess,tempfile
root=Path(__file__).resolve().parents[1]
subprocess.run(['make','cpu'],cwd=root,check=True)
with tempfile.TemporaryDirectory() as td:
    p=str(Path(td)/'run')
    cmd=[str(root/'bin/runecore_cpu'),'32','5','0.001','42',p]
    a=subprocess.check_output(cmd,text=True); b=subprocess.check_output(cmd,text=True)
    m=json.loads(Path(p+'-metrics.json').read_text()); rows=list(csv.DictReader(open(p+'-state.csv')))
    assert len(rows)==32 and m['backend']=='cpu_cpp' and m['status']=='OBSERVATION_NOT_CANON'
    for row in rows:
        for k in ('x','y','z','vx','vy','vz','mass','amplitude','phase'): assert math.isfinite(float(row[k]))
    first=Path(p+'-state.csv').read_bytes(); subprocess.check_output(cmd,text=True); second=Path(p+'-state.csv').read_bytes(); assert first==second
print('CPU_TESTS_PASS')
