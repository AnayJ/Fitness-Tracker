"""AI service for LLM integration."""
import json
import re
from typing import Optional, List, Dict

import requests
from app.core.config import settings
from app.utils.calculators import (
    calculate_maintenance_calories,
    calculate_macro_percentages,
    estimate_weight_change,
)


class AIService:
    """Service for AI/LLM integration."""

    @staticmethod
    def _ollama_generate(prompt: str) -> Optional[str]:
        """Generate a response using a local Ollama model."""
        api_url = settings.OLLAMA_API_URL or "http://127.0.0.1:11434/v1/generate"
        model = settings.OLLAMA_MODEL or "llama2"
        payload = {
            "model": model,
            "prompt": prompt,
            "max_tokens": 400,
            "temperature": 0.2,
        }
        response = requests.post(api_url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict):
            if "choices" in data and isinstance(data["choices"], list):
                texts = []
                for choice in data["choices"]:
                    if isinstance(choice, dict):
                        texts.append(choice.get("content") or choice.get("text", ""))
                return "".join(texts).strip()
            return data.get("text") or data.get("response")

        return None

    @staticmethod
    def _build_ollama_prompt(message: str, user_data: dict, history: List[Dict]) -> str:
        """Compose an Ollama prompt for the fitness assistant."""
        profile = []
        if user_data:
            profile.append("User fitness profile:")
            profile.append(f"- Name: {user_data.get('name', 'N/A')}")
            profile.append(f"- Goal: {user_data.get('fitness_goal', 'N/A')}")
            profile.append(f"- Weight: {user_data.get('weight', 'N/A')} kg")
            profile.append(f"- Height: {user_data.get('height', 'N/A')} cm")
            profile.append(f"- BMI: {user_data.get('bmi', 'N/A')}")
            profile.append(f"- Maintenance calories: {user_data.get('maintenance_calories', 'N/A')} kcal/day")
            profile.append(f"- Target calories: {user_data.get('target_calories', 'N/A')} kcal/day")
            profile.append("")

        if history:
            profile.append("Conversation history:")
            for message_item in history:
                role = message_item.get("role", "user")
                content = message_item.get("content", "")
                profile.append(f"- {role}: {content}")
            profile.append("")

        profile_text = "\n".join(profile)
        prompt = f"""You are a friendly fitness assistant.
Use the Mifflin-St Jeor formula for maintenance calories and a moderate activity multiplier of 1.55.
Use macros: protein 4 kcal/g, carbs 4 kcal/g, fats 9 kcal/g.
When asked about deficits or surpluses, calculate 15% adjustment from maintenance calories.
Answer clearly with numbers and short recommendations.

{profile_text}
User question: {message}

Respond as a helpful fitness assistant."""
        return prompt

    @staticmethod
    def suggest_fitness_goal(bmi: float, maintenance_calories: float, 
                           weight: float, height: float) -> dict:
        """Suggest fitness goal using AI."""
        if settings.OLLAMA_API_URL:
            try:
                return AIService._ollama_goal_suggestion(bmi, maintenance_calories)
            except Exception as exc:
                print(f"Ollama goal suggestion failed: {exc}")

        if not settings.GEMINI_API_KEY and not settings.OPENAI_API_KEY:
            return AIService._rule_based_goal_suggestion(bmi, maintenance_calories)

        try:
            if settings.GEMINI_API_KEY:
                return AIService._gemini_goal_suggestion(bmi, maintenance_calories)
            elif settings.OPENAI_API_KEY:
                return AIService._openai_goal_suggestion(bmi, maintenance_calories)
        except Exception as exc:
            print(f"AI goal suggestion failed: {exc}")

        return AIService._rule_based_goal_suggestion(bmi, maintenance_calories)

    @staticmethod
    def _ollama_goal_suggestion(bmi: float, maintenance_calories: float) -> dict:
        """Query Ollama to suggest a fitness goal."""
        prompt = (
            f"Based on these metrics:\n- BMI: {bmi}\n- Maintenance Calories: {maintenance_calories:.0f}\n"
            "Suggest one fitness goal (lose, gain, maintain), a brief explanation, "
            "and a weekly projection for weight change. Respond in JSON like: "
            "{\"goal\": \"...\", \"explanation\": \"...\", \"projection\": \"...\"}."
        )
        llm_response = AIService._ollama_generate(prompt)
        if not llm_response:
            return AIService._rule_based_goal_suggestion(bmi, maintenance_calories)

        try:
            parsed = json.loads(re.search(r"\{.*\}", llm_response, re.DOTALL).group(0))
            goal = parsed.get("goal", "maintain")
            explanation = parsed.get("explanation", "Based on your current metrics.")
            projection = parsed.get("projection", "Approximately 0.5 kg/week")
        except Exception:
            goal = "maintain" if 18.5 <= bmi < 25 else "lose" if bmi >= 25 else "gain"
            explanation = "Based on your current metrics."
            projection = "Approximately 0.5 kg/week"

        target_calories = maintenance_calories * (0.85 if goal == "lose" else 1.15 if goal == "gain" else 1.0)
        return {
            "suggested_goal": goal,
            "explanation": explanation,
            "target_calories": target_calories,
            "weekly_projection": projection,
        }

    @staticmethod
    def _rule_based_calorie_goal(user_data: dict, message_lower: str) -> Dict[str, Optional[str]]:
        maintenance = user_data.get("maintenance_calories") if user_data else None
        if not maintenance and user_data and user_data.get("weight") and user_data.get("height"):
            maintenance = calculate_maintenance_calories(user_data["weight"], user_data["height"])

        goal = user_data.get("fitness_goal") if user_data else None
        if goal not in {"lose", "gain", "maintain"}:
            goal = "maintain"

        response = None
        suggested_action = None

        if "maintain" in message_lower or "maintenance" in message_lower or "bmr" in message_lower:
            if maintenance:
                deficit = maintenance * 0.85
                surplus = maintenance * 1.15
                response = (
                    f"Your estimated maintenance calories are {maintenance:.0f} kcal/day. "
                    f"For a moderate 15% deficit, aim for about {deficit:.0f} kcal/day. "
                    f"For a moderate 15% surplus, aim for about {surplus:.0f} kcal/day."
                )
                suggested_action = f"Use {deficit:.0f} kcal/day for deficit or {surplus:.0f} kcal/day for surplus."
            else:
                response = "I can help calculate your maintenance calories once you provide weight and height."

        elif any(word in message_lower for word in ["deficit", "surplus", "lose weight", "gain weight", "goal"]):
            if maintenance:
                if "lose" in message_lower or "deficit" in message_lower:
                    target = maintenance * 0.85
                    response = (
                        f"A gentle 15% deficit from maintenance is {target:.0f} kcal/day. "
                        f"That means if your maintenance is {maintenance:.0f}, you can target {target:.0f} calories to support fat loss."
                    )
                    suggested_action = f"Try {target:.0f} kcal/day for a 15% deficit."
                elif "gain" in message_lower or "surplus" in message_lower:
                    target = maintenance * 1.15
                    response = (
                        f"A moderate 15% surplus from maintenance is {target:.0f} kcal/day. "
                        f"That means if your maintenance is {maintenance:.0f}, you can target {target:.0f} calories to support muscle gain."
                    )
                    suggested_action = f"Try {target:.0f} kcal/day for a 15% surplus."
                else:
                    response = (
                        f"Your maintenance calories are {maintenance:.0f} kcal/day. "
                        f"For fat loss choose a deficit, for muscle gain choose a surplus, and for keeping weight aim for maintenance."
                    )
            else:
                response = "I can help suggest deficit or surplus targets once your maintenance calories are known."

        if response:
            return {"response": response, "suggested_action": suggested_action}

        return {"response": None, "suggested_action": None}

    @staticmethod
    def _rule_based_macro_advice(user_data: dict, message_lower: str) -> Dict[str, Optional[str]]:
        target_calories = user_data.get("target_calories") if user_data else None
        if not target_calories and user_data and user_data.get("maintenance_calories"):
            target_calories = user_data["maintenance_calories"]

        if not target_calories:
            return {
                "response": "I can recommend a macro split once your daily calorie target is available.",
                "suggested_action": None,
            }

        goal = user_data.get("fitness_goal") if user_data else "maintain"
        if goal == "lose":
            ratios = (0.35, 0.40, 0.25)
        elif goal == "gain":
            ratios = (0.30, 0.45, 0.25)
        else:
            ratios = (0.30, 0.40, 0.30)

        protein_cal = target_calories * ratios[0]
        carbs_cal = target_calories * ratios[1]
        fats_cal = target_calories * ratios[2]
        protein_g = round(protein_cal / 4)
        carbs_g = round(carbs_cal / 4)
        fats_g = round(fats_cal / 9)
        breakdown = calculate_macro_percentages(protein_g, carbs_g, fats_g)

        response = (
            f"For a {goal} goal, a good daily macro target on {target_calories:.0f} kcal is: "
            f"{protein_g}g protein, {carbs_g}g carbs, {fats_g}g fats. "
            f"That is approximately {breakdown['protein_percent']}% protein, {breakdown['carbs_percent']}% carbs, and {breakdown['fats_percent']}% fats."
        )
        suggested_action = (
            f"Aim for {protein_g}g protein, {carbs_g}g carbs, and {fats_g}g fats daily."
        )

        return {"response": response, "suggested_action": suggested_action}

    @staticmethod
    def generate_weekly_report(user_data: dict, summary: dict) -> str:
        """Create a simple weekly report summary."""
        days_tracked = summary.get("days_tracked", 0)
        avg_calories = summary.get("avg_calories", 0)
        avg_protein = summary.get("avg_protein", 0)
        avg_carbs = summary.get("avg_carbs", 0)
        avg_fats = summary.get("avg_fats", 0)
        target_calories = summary.get("target_calories", 2000)

        if days_tracked == 0:
            return (
                "No meals were logged in the past week yet. "
                "Start logging meals daily to get better weekly insights and nutrition guidance."
            )

        name = user_data.get("name", "there")
        goal = user_data.get("fitness_goal", "maintain")

        return (
            f"Hi {name}! Over the last {days_tracked} tracked days, you averaged "
            f"{avg_calories:.0f} calories, {avg_protein:.0f}g protein, {avg_carbs:.0f}g carbs, and {avg_fats:.0f}g fats per day. "
            f"Your daily target is {target_calories:.0f} calories and your goal is set to {goal}. "
            "Keep logging your meals consistently and aim for balanced macros to support your progress."
        )

    @staticmethod
    def _simple_rule_based_chat(message: str, user_data: dict = None, history: List[Dict] = None) -> Dict[str, Optional[str]]:
        message_lower = message.lower()

        calorie_response = AIService._rule_based_calorie_goal(user_data or {}, message_lower)
        if calorie_response["response"]:
            return calorie_response

        if any(word in message_lower for word in ["macro", "protein", "carb", "fat"]):
            return AIService._rule_based_macro_advice(user_data or {}, message_lower)

        if any(word in message_lower for word in ["dinner", "lunch", "breakfast", "eat", "food"]):
            return {
                "response": "Focus on balanced meals with lean protein, vegetables, and whole grains. Keep your portions aligned with your daily calorie target.",
                "suggested_action": None,
            }

        if any(word in message_lower for word in ["progress", "track", "losing", "gaining"]):
            return {
                "response": "Consistency is key. Track your calories and macros daily, and adjust your plan based on how your body responds.",
                "suggested_action": None,
            }

        if user_data and user_data.get("target_calories"):
            return {
                "response": f"Your current daily target is {user_data['target_calories']:.0f} kcal. Ask me how to adjust that for deficit, surplus, or macros.",
                "suggested_action": None,
            }

        return {
            "response": "I'm here to help with maintenance calories, calorie targets, and macro recommendations. Ask me anything fitness-related.",
            "suggested_action": None,
        }

    @staticmethod
    def chat(message: str, user_data: dict = None, history: List[Dict] = None) -> Dict[str, Optional[str]]:
        """Fitness chatbot response."""
        if history is None:
            history = []

        if settings.OLLAMA_API_URL:
            try:
                prompt = AIService._build_ollama_prompt(message, user_data or {}, history)
                llm_response = AIService._ollama_generate(prompt)
                if llm_response:
                    return {"response": llm_response.strip(), "suggested_action": None}
            except Exception as exc:
                print(f"Ollama request failed: {exc}")

        return AIService._simple_rule_based_chat(message, user_data, history)
