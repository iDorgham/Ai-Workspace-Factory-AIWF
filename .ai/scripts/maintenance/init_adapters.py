import os

adapters = [
    ("copilot", 0.0, 0.0), # Copilot pricing logic here
    ("codex", 0.0015, 0.0020),
    ("gemini", 0.000125, 0.000375),
    ("qwen", 0.0004, 0.0012),
    ("opencode", 0.0, 0.0),
    ("kilo", 0.005, 0.015)
]

template = """from .base_adapter import BaseAdapter

class {name}Adapter(BaseAdapter):
    ADAPTER_NAME = "{name}"
    COST_PER_1K_IN = {cost_in}
    COST_PER_1K_OUT = {cost_out}

    def _execute_query(self, prompt, **kwargs):
        # Implementation for {name}
        # Returns simulated values for now
        return ("Stub response from {name}", len(prompt)//4, 10)
"""

for name, cost_in, cost_out in adapters:
    class_name = name.capitalize()
    content = template.format(name=class_name, cost_in=cost_in, cost_out=cost_out)
    with open(f".ai/scripts/tool_adapters/{name}_adapter.py", "w") as f:
        f.write(content)

with open(".ai/scripts/tool_adapters/__init__.py", "w") as f:
    f.write("from .base_adapter import BaseAdapter\n")
    for name, _, _ in adapters:
        f.write(f"from .{name}_adapter import {name.capitalize()}Adapter\n")
