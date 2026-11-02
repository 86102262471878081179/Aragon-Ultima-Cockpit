#!/usr/bin/env python3
import json
import re
import os
from typing import List, Dict, Any

def parse_arsenal_file(filepath: str) -> List[Dict[str, Any]]:
    if not os.path.exists(filepath):
        print(f"Quelldatei '{filepath}' nicht gefunden.")
        return []

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    mappings = []
    
    for line in lines:
        line = line.strip()
        if not line or not re.match(r'^\d+\.', line):
            continue
            
        parts = line.split('.', 1)
        slot_num = parts[0].strip()
        raw_title = parts[1].strip() if len(parts) > 1 else ""
        
        calm_id = re.sub(r'[^\x00-\x7F]+', ' ', raw_title)
        calm_id = re.sub(r'[^a-zA-Z0-9_]+', '_', calm_id)
        calm_id = re.sub(r'_+', '_', calm_id).strip('_').upper()
        
        if not calm_id.startswith("B6_"):
            calm_id = f"B6_{slot_num}_{calm_id}"
            
        mapping_item = {
            "slot_number": int(slot_num),
            "id": f"DRIVE_FOLDER_ID_{int(slot_num):04d}",
            "old_title": raw_title,
            "calm_title": calm_id,
            "status": "READY_FOR_SYNC"
        }
        mappings.append(mapping_item)

    return mappings

if __name__ == "__main__":
    arsenal_path = "b6_sys.Notebook_Arsenal[124].txt" # Platzhalter
    output_json = "b6_drive_mapping.json"
    
    print(f"Lese Arsenal-Slots aus '{arsenal_path}'...")
    mappings = parse_arsenal_file(arsenal_path)
    
    if mappings:
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(mappings, f, indent=2, ensure_ascii=False)
        print(f"Mapping erfolgreich generiert: {len(mappings)} Slots -> '{output_json}'")
    else:
        print("Keine Einträge verarbeitet (Datei fehlt evtl.).")
