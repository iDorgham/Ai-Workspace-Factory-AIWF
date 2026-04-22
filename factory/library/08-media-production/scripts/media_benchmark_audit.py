import os
import json
import sys
import importlib.util
from pathlib import Path

# Add project root to sys.path
root = Path("/Users/Dorgham/Documents/Work/Devleopment/Sovereign/Sovereign Workspace Factory")
sys.path.append(str(root))

def import_path(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Dynamic imports for dashed paths
video_core_path = root / "factory/library/08-media-production/video-production/skills/video-production-mastery/core.py"
threed_core_path = root / "factory/library/08-media-production/3d-production/skills/3d-production-mastery/core.py"

video_mod = import_path(str(video_core_path), "video_production_mastery_core")
threed_mod = import_path(str(threed_core_path), "threed_production_mastery_core")

VideoProductionMastery = video_mod.VideoProductionMastery
ThreeDProductionMastery = threed_mod.ThreeDProductionMastery

# Mock Oasis Asset Manifest
OASIS_MEDIA_MANIFEST = [
    {
        "name": "Oasis_New_Cairo_Main_Hero_V1.mp4",
        "type": "video",
        "specs": {"resolution": "4K", "bitrate_mbps": 45.0, "color_space": "Rec.709", "cut_timestamps": [0, 1.8, 4.5, 9.0]}
    },
    {
        "name": "Penthouse_3D_Interactive_Unit.glb",
        "type": "3d",
        "specs": {"poly_count": 48000, "draw_calls": 3, "is_atlased": True, "has_normal_map": True, "has_roughness_map": True, "has_metallic_map": True}
    },
    {
        "name": "Oasis_Lifestyle_Shorts_IG.mp4",
        "type": "video",
        "specs": {"resolution": "1080p", "bitrate_mbps": 12.0, "color_space": "Rec.709", "cut_timestamps": [0, 1.2, 2.5, 4.0]}
    }
]

REPORT_PATH = root / "content/sovereign/outputs/simulations/egypt-real-estate-mega/MEDIA_CERTIFICATION.json"

def run_legacy_benchmark():
    video_engine = VideoProductionMastery()
    threed_engine = ThreeDProductionMastery()

    results = []
    total_score = 0

    print("🎬 Starting Cross-Project Media Benchmark for Oasis New Cairo...")

    for asset in OASIS_MEDIA_MANIFEST:
        audit = {}
        if asset["type"] == "video":
            b_audit = video_engine.audit_cinematic_bitrate(asset["specs"])
            c_audit = video_engine.verify_color_space_guard(asset["specs"])
            s_audit = video_engine.calculate_storytelling_density(asset["specs"])
            
            is_pass = b_audit["is_bitrate_compliant"] and c_audit["is_brand_standard"] and s_audit["is_scroll_stop_ready"]
            audit = {
                "name": asset["name"],
                "passed": is_pass,
                "bitrate_status": b_audit["status"],
                "color_status": c_audit["is_brand_standard"],
                "hook_density": s_audit["density_tier"]
            }
        elif asset["type"] == "3d":
            m_audit = threed_engine.audit_mesh_density(asset["specs"])
            t_audit = threed_engine.verify_texture_atlas(asset["specs"])
            p_audit = threed_engine.check_pbr_integrity(asset["specs"])
            
            is_pass = m_audit["is_compliant"] and t_audit["is_optimized"] and p_audit["is_high_fidelity"]
            audit = {
                "name": asset["name"],
                "passed": is_pass,
                "mesh_status": m_audit["status"],
                "texture_status": t_audit["status"],
                "fidelity_tier": p_audit["fidelity_tier"]
            }
        
        results.append(audit)
        if audit["passed"]: total_score += 1

    final_score = (total_score / len(OASIS_MEDIA_MANIFEST)) * 100

    final_report = {
        "project": "Oasis New Cairo",
        "audit_timestamp": "2026-04-20",
        "overall_certification": "💎 OMEGA-CINEMATIC" if final_score >= 90 else "INDUSTRIAL_BETA",
        "fidelity_score": int(final_score),
        "asset_audits": results
    }

    # Ensure output directory exists
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, "w") as f:
        json.dump(final_report, f, indent=4)

    print(f"\n✅ Benchmark Complete. Overall Fidelity Score: {final_score}%")
    print(f"Certification: {final_report['overall_certification']}")

if __name__ == "__main__":
    run_legacy_benchmark()
