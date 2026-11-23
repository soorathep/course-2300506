"""2300506 Industrial Science: check that your laptop is ready for the workshops.

Run it from a terminal (Windows: Command Prompt or Anaconda Prompt; macOS: Terminal):

    python check_setup.py

It prints one line per item. [OK] means ready. [FIX] tells you what to do. At the end it says READY or NOT READY.
"""
import sys
import platform
import importlib

MIRROR = "https://pypi.tuna.tsinghua.edu.cn/simple"
problems = []


def ok(msg):
    print("[OK]  " + msg)


def fix(msg, how):
    print("[FIX] " + msg)
    print("      -> " + how)
    problems.append(msg)


print("2300506 setup check  |  Python " + platform.python_version() + "  |  " + platform.system() + " " + platform.machine())
print("-" * 72)

v = sys.version_info
if v >= (3, 12):
    ok("Python " + platform.python_version())
elif v >= (3, 10):
    fix("Python " + platform.python_version() + " works for most tasks, but recent PuLP needs Python 3.12 or newer",
        "install Python 3.12 or newer from python.org, then install the packages again")
else:
    fix("Python " + platform.python_version() + " is too old", "install Python 3.12 or newer from python.org")

PIP = 'python -m pip install -i ' + MIRROR + ' '
for name, pipname in [("numpy", "numpy"), ("scipy", "scipy"), ("pandas", "pandas"), ("matplotlib", "matplotlib")]:
    try:
        m = importlib.import_module(name)
        ok(name + " " + getattr(m, "__version__", ""))
    except Exception:
        fix(name + " is missing", PIP + pipname)

try:
    import notebook  # noqa: F401
    ok("Jupyter Notebook")
except Exception:
    try:
        import jupyterlab  # noqa: F401
        ok("JupyterLab")
    except Exception:
        fix("Jupyter is missing", PIP + "jupyterlab")

# A small linear program with SciPy (used in Block 2)
try:
    from scipy.optimize import linprog
    r = linprog([-30, -48], A_ub=[[2, 3], [1.5, 1], [0, 1]], b_ub=[240, 150, 60], method="highs")
    if r.success and abs(-r.fun - 3780) < 1e-6:
        ok("SciPy solves the CellCo product-mix LP (3,780)")
    else:
        fix("SciPy linprog gave an unexpected result", "update SciPy: " + PIP + "--upgrade scipy")
except Exception as e:
    fix("SciPy linprog failed (" + str(e)[:60] + ")", "update SciPy: " + PIP + "--upgrade scipy")

# PuLP 3.x with a working MILP solver (used in Block 2, workshop W6).
# The course uses the classic PuLP 3 interface; PuLP 4 changed it.
def pulp_test(pulp, solver):
    prob = pulp.LpProblem("check", pulp.LpMinimize)
    x = pulp.LpVariable("x", lowBound=0)
    y = pulp.LpVariable("y", cat="Binary")
    prob += 3 * x + 250 * y
    prob += x >= 90 - 40 * y
    prob += x <= 80
    prob.solve(solver)
    return pulp.LpStatus[prob.status] == "Optimal" and abs(pulp.value(prob.objective) - 400) < 1e-6


try:
    import pulp
    major = int(pulp.__version__.split(".")[0])
    if major != 3:
        fix("PuLP " + pulp.__version__ + " is installed; the course uses PuLP 3",
            PIP + '"pulp>=3,<4" highspy')
    else:
        works = []
        for label, make in [("CBC", lambda: pulp.PULP_CBC_CMD(msg=0)), ("HiGHS", lambda: pulp.HiGHS(msg=False))]:
            try:
                if pulp_test(pulp, make()):
                    works.append(label)
            except Exception:
                pass
        if works:
            ok("PuLP " + pulp.__version__ + " solves a small integer program with " + " and ".join(works))
        else:
            how = PIP + "highspy"
            if platform.system() == "Darwin" and platform.machine() == "arm64":
                how += "   (or install Rosetta 2: softwareupdate --install-rosetta)"
            fix("PuLP " + pulp.__version__ + " is installed but no solver works", how)
except ImportError:
    fix("PuLP is missing", PIP + '"pulp>=3,<4" highspy')

print("-" * 72)
if problems:
    print("NOT READY: fix the " + str(len(problems)) + " item(s) marked [FIX], then run this check again.")
    print("If an item still fails, bring this output to the first class.")
else:
    print("READY. Bring your laptop and charger to class.")
