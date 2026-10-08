import os
import sys
import shutil
import zipfile
from pathlib import Path

# UTF-8 stdout configuration
sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent

def make_submission_zip(team_name="CareerPath_AI"):
    # Sanitize team name for filesystem
    safe_team_name = team_name.strip().replace(" ", "_")
    output_dir = ROOT_DIR / "submission_staging" / safe_team_name
    zip_path = ROOT_DIR / f"{safe_team_name}.zip"
    
    if output_dir.exists():
        shutil.rmtree(output_dir, ignore_errors=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"==================================================")
    print(f"Creating Hackathon Submission Package: {safe_team_name}")
    print(f"==================================================")

    # 1. Approach Note
    appr_dir = output_dir / "1_Approach_Note"
    appr_dir.mkdir(parents=True, exist_ok=True)
    
    report_file = ROOT_DIR / "CareerPath_AI_Hackathon_Report.docx"
    alt_report = Path(r"C:\Users\Prem\Downloads\CareerPath_AI_Hackathon_Report (1).docx")
    appr_file = ROOT_DIR / "Approach_Note_CareerPath_AI.docx"
    
    if report_file.exists():
        try:
            shutil.copy2(report_file, appr_dir / "CareerPath_AI_Hackathon_Report.docx")
            print("✓ Copied: CareerPath_AI_Hackathon_Report.docx (29 Pages)")
        except Exception:
            if alt_report.exists():
                shutil.copy2(alt_report, appr_dir / "CareerPath_AI_Hackathon_Report.docx")
                print("✓ Copied: CareerPath_AI_Hackathon_Report.docx (from Downloads backup)")
    elif alt_report.exists():
        shutil.copy2(alt_report, appr_dir / "CareerPath_AI_Hackathon_Report.docx")
        print("✓ Copied: CareerPath_AI_Hackathon_Report.docx")
        
    if appr_file.exists():
        try:
            shutil.copy2(appr_file, appr_dir / "Approach_Note_CareerPath_AI.docx")
            print("✓ Copied: Approach_Note_CareerPath_AI.docx")
        except Exception as e:
            print(f"Notice: {e}")

    # 2. Source Code
    src_dir = output_dir / "2_Source_Code"
    src_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy backend (excluding .venv, __pycache__)
    backend_dest = src_dir / "backend"
    shutil.copytree(
        ROOT_DIR / "backend",
        backend_dest,
        ignore=shutil.ignore_patterns(".venv", "__pycache__", "*.pyc", "data", "figures"),
        dirs_exist_ok=True
    )
    print("✓ Packaged: Backend Source Code (FastAPI, routers, services, models)")
    
    # Copy frontend (excluding node_modules, dist)
    frontend_dest = src_dir / "frontend"
    if (ROOT_DIR / "frontend").exists():
        shutil.copytree(
            ROOT_DIR / "frontend",
            frontend_dest,
            ignore=shutil.ignore_patterns("node_modules", "dist", ".git", ".env*"),
            dirs_exist_ok=True
        )
        print("✓ Packaged: Frontend Source Code (React, Vite, TailwindCSS, Pages)")
        
    # Copy root scripts
    for f in ["README.md", "create_presentation.py"]:
        p = ROOT_DIR / f
        if p.exists():
            shutil.copy2(p, src_dir / f)

    # 3. Data Files
    data_dest = output_dir / "3_Data_Files"
    data_dest.mkdir(parents=True, exist_ok=True)
    
    backend_data = ROOT_DIR / "backend" / "data"
    if backend_data.exists():
        for item in backend_data.iterdir():
            if item.is_file():
                shutil.copy2(item, data_dest / item.name)
            elif item.is_dir() and item.name == "figures":
                shutil.copytree(item, data_dest / "figures", dirs_exist_ok=True)
        print("✓ Packaged: All 7 Datasets, Trained Model JSONs, and Figures")

    # 4. Create ZIP
    print(f"\nCompressing to {zip_path.name}...")
    if zip_path.exists():
        zip_path.unlink()
        
    with zipfile.ZipFile(str(zip_path), "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                abs_file = Path(root) / file
                rel_path = abs_file.relative_to(output_dir.parent)
                zipf.write(abs_file, rel_path)
                
    # Clean up staging safely
    try:
        shutil.rmtree(ROOT_DIR / "submission_staging", ignore_errors=True)
    except Exception:
        pass
    
    zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"==================================================")
    print(f"SUCCESS: {zip_path.name} created successfully!")
    print(f"Path: {zip_path.resolve()}")
    print(f"Size: {zip_size_mb:.2f} MB")
    print(f"==================================================")
    return zip_path

if __name__ == "__main__":
    t_name = sys.argv[1] if len(sys.argv) > 1 else "CareerPath_AI"
    make_submission_zip(t_name)
