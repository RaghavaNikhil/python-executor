import subprocess
import uuid
import os
import json
import ast

def validate_script(script_code):
    """Ensure the script has a main() function."""
    try:
        tree = ast.parse(script_code)
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        if "main" not in functions:
            raise Exception("Script must define a function named main()")
    except SyntaxError:
        raise Exception("Script contains syntax errors")

def run_script(script_code):
    # Validate before execution
    validate_script(script_code)

    script_id = str(uuid.uuid4())
    temp_path = f"/tmp/{script_id}.py"

    with open(temp_path, "w") as f:
        f.write(script_code)

    try:
        result = subprocess.run([
            "nsjail",
            "--mode", "o",
            "--hostname", "sandbox",
            "--disable_clone_newnet",
            "--disable_clone_newuser",
            "--disable_clone_newcgroup",
            "--disable_clone_newipc",
            "--disable_clone_newuts",
            "--disable_clone_newpid",
            "--disable_clone_newns",
            "--disable_no_new_privs",
            "--disable_rlimits",
            "--rlimit_as", "268435456",
            "--rlimit_cpu", "5",
            "--bindmount", "/tmp",
            "--bindmount_ro", "/usr/local",
            "--bindmount_ro", "/lib",
            "--bindmount_ro", "/lib64",
            "--bindmount_ro", "/usr/local/lib",
            "--env", "LD_LIBRARY_PATH=/usr/local/lib",
            "--",
            "/usr/local/bin/python3", temp_path
        ], capture_output=True, text=True, timeout=5)

        if result.returncode != 0:
            raise Exception(result.stderr or result.stdout)

        stdout = result.stdout.strip()
        try:
            parsed_result = json.loads(stdout)
            if not isinstance(parsed_result, dict):
                raise Exception("main() must return a JSON object (dict)")
        except json.JSONDecodeError:
            raise Exception("main() must return valid JSON")

        return parsed_result, stdout
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
