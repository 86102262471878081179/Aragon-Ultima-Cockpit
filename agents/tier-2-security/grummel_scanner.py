import logging

logger = logging.getLogger("TIER-2-SECURITY")

class GrummelSignatureScanner:
    """Forensischer Scanner für die Grummel-Dynastie."""
    
    CORE_SIGNATURES = [
        "grummel", "brummel", "dummelt",
        "pissingerkeule", "mettwurst", "rhabarberbarbara",
        "cargo-kult", "urheberinfo", "§ 839 bgb",
    ]
    
    SUB_ENTITIES = {
        "BieneMaja":  ["biene maja", "bienchen", "maja", "summsumm"],
        "Pumuckl":    ["pumuckl", "kobold", "klabautermann", "chaos-imp"],
        "King_Ghost": ["king_ghost", "king ghost", "ghost-king", "schattenkönig"],
        "DrSnuggles": ["dr. snuggles", "dr.snuggles", "snuggles", "cyberlord"],
    }

    def scan(self, text: str) -> tuple[bool, list, list]:
        """Returns: (is_hostile, core_hits, sub_entity_hits)."""
        t = text.lower()
        core = [s for s in self.CORE_SIGNATURES if s in t]
        subs = []
        for entity, kws in self.SUB_ENTITIES.items():
            for kw in kws:
                if kw in t:
                    subs.append(entity)
                    break
        return bool(core or subs), core, subs
