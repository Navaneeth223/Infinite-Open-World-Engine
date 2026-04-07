from typing import Dict


class PersonalityEngine:
    def get_reaction_modifier(self, npc: dict, event_type: str) -> float:
        reactions = {
            "violence_nearby": npc.get("neuroticism", 0.5) * 0.8 + (1 - npc.get("agreeableness", 0.5)) * 0.2,
            "stranger_approaches": (1 - npc.get("extraversion", 0.5)) * 0.7 + npc.get("neuroticism", 0.5) * 0.3,
            "good_news": npc.get("extraversion", 0.5) * 0.6 + (1 - npc.get("neuroticism", 0.5)) * 0.4,
            "moral_dilemma": npc.get("conscientiousness", 0.5) * 0.5 + npc.get("openness", 0.5) * 0.3 + npc.get("agreeableness", 0.5) * 0.2,
            "new_idea": npc.get("openness", 0.5),
            "threat": npc.get("neuroticism", 0.5) * 0.6 + (1 - npc.get("agreeableness", 0.5)) * 0.4,
        }
        return reactions.get(event_type, 0.5)

    def get_speaking_style_instructions(self, npc: dict) -> str:
        styles = []
        if npc.get("extraversion", 0.5) > 0.7:
            styles.append("speaks freely, volunteers information, asks questions back")
        elif npc.get("extraversion", 0.5) < 0.3:
            styles.append("gives short answers, doesn't volunteer information, pauses before speaking")
        if npc.get("agreeableness", 0.5) > 0.7:
            styles.append("warm, finds common ground, softens bad news")
        elif npc.get("agreeableness", 0.5) < 0.3:
            styles.append("blunt, doesn't spare feelings, transactional")
        if npc.get("neuroticism", 0.5) > 0.7:
            styles.append("worried undertone, mentions risks and problems, easily unsettled")
        if npc.get("openness", 0.5) > 0.7:
            styles.append("curious, makes unexpected connections, philosophical")
        elif npc.get("openness", 0.5) < 0.3:
            styles.append("practical, distrusts novelty, refers to tradition")
        if npc.get("conscientiousness", 0.5) > 0.7:
            styles.append("precise, refers to details and facts, follows through on what they say")
        return "; ".join(styles)

    def update_mood(self, npc: dict, event: dict) -> str:
        base_mood = npc.get("mood", "neutral")
        emotional_impact = event.get("emotional_weight", 0.5) * self.get_reaction_modifier(npc, event.get("type", ""))
        valence = event.get("valence", "neutral")
        if valence == "negative" and emotional_impact > 0.5:
            return "distressed"
        if valence == "negative" and emotional_impact > 0.2:
            return "worried"
        if valence == "positive" and emotional_impact > 0.5:
            return "elated"
        if valence == "positive":
            return "content"
        return base_mood


personality_engine = PersonalityEngine()
