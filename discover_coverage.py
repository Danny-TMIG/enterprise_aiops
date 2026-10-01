import os
import sys
import coverage

def run_discovery():
    print("\n🔍 Evaluating Sovereign Infrastructure Core Telemetry Matrix...")
    
    cov = coverage.Coverage(config_file=".coveragerc")
    cov.load()
    
    data = cov.get_data()
    measured_files = data.measured_files()
    
    if not measured_files:
        print("❌ Error: No execution telemetry captured. Confirm your workspace configuration paths.")
        sys.exit(1)
        
    has_gaps = False
    print("📋 Component Coverage Summary Matrix:")
    
    # Filter the list down specifically to files that pass our include constraints
    target_includes = [
        "dcs/verify.py",
        "dcs/verify_intoto.py",
        "dcs/mesh/behavior.py",
        "dcs/self.py",
        "dcs/crosscut/semver.py",
        "dcs/__main__.py",
        "dcs/conform.py"
    ]
    
    for file_path in measured_files:
        rel_path = os.path.relpath(file_path)
        
        # Only verify the explicit enterprise logic interfaces
        if not any(target in rel_path for target in target_includes):
            continue
            
        analysis = cov._analyze(file_path)
        missing_lines = sorted(list(analysis.missing))
        missing_branches = getattr(analysis, "missing_branches", lambda: {})()
        
        if missing_lines or missing_branches:
            has_gaps = True
            print(f"\n🟥 {rel_path} -> REFACTORING REQUIRED")
            if missing_lines:
                print(f"   • Missing Statements: {missing_lines}")
            if missing_branches:
                print(f"   • Missing Branch Routes: {missing_branches}")
        else:
            print(f"🟩 {rel_path} -> 100% TEST COMPLIANT")
            
    print("\n🏁 Final Structural Analysis Completed.")
    if has_gaps:
        sys.exit(1)
    else:
        print("🎉 Success: 100% Threshold achieved across all core system interfaces!")
        sys.exit(0)

if __name__ == "__main__":
    run_discovery()
