"""AI service for LLM integration."""
import json
import requests
from typing import Optional, List, Dict
from app.core.config import settings
from app.utils.calculators import estimate_weight_change


class AIService:
    """Service for AI/LLM integration."""
    
    @staticmethod
    def suggest_fitness_goal(bmi: float, maintenance_calories: float, 
                           weight: float, height: float) -> dict:
        """Suggest fitness goal using AI.
        
        Args:
            bmi: User's BMI
            maintenance_calories: User's maintenance calories
            weight: User's weight in kg
            height: User's height in cm
            
        Returns:
            Dictionary with suggested goal and explanation
        """
        # If no API key available, use rule-based suggestions
        if not settings.GEMINI_API_KEY and not settings.OPENAI_API_KEY:
            return AIService._rule_based_goal_suggestion(bmi, maintenance_calories)
        
        # Try to use API if available
        try:
            if settings.GEMINI_API_KEY:
                return AIService._gemini_goal_suggestion(bmi, maintenance_calories)
            elif settings.OPENAI_API_KEY:
                return AIService._openai_goal_suggestion(bmi, maintenance_calories)
        except Exception as e:
            print(f"Error calling AI API: {e}")
            # Fallback to rule-based
            return AIService._rule_based_goal_suggestion(bmi, maintenance_calories)
    
    @staticmethod
    def _rule_based_goal_suggestion(bmi: float, maintenance_calories: float) -> dict:
        """Rule-based fitness goal suggestion (fallback)."""
        if bmi < 18.5:
            goal = "gain"
            explanation = "Your BMI indicates you're underweight. Consider gaining weight to reach a healthy range."
        elif 18.5 <= bmi < 25:
            goal = "maintain"
            explanation = "Your BMI is in the healthy range. Focus on maintaining your current fitness level."
        elif 25 <= bmi < 30:
            goal = "lose"
            explanation = "Your BMI indicates you're overweight. A calorie deficit may help you reach a healthier weight."
        else:
            goal = "lose"
            explanation = "Your BMI indicates obesity. Gradually reducing calories can help you reach a healthier weight."
        
        if goal == "lose":
            target_calories = maintenance_calories * 0.85
        elif goal == "gain":
            target_calories = maintenance_calories * 1.15
        else:
            target_calories = maintenance_calories
        
        projection = estimate_weight_change(maintenance_calories - target_calories)
        
        return {
            "suggested_goal": goal,
            "explanation": explanation,
            "target_calories": target_calories,
            "weekly_projection": f"At this goal, you may lose/gain ~{abs(projection['weekly_change_kg'])} kg/week"
        }
    
    @staticmethod
    def _gemini_goal_suggestion(bmi: float, maintenance_calories: float) -> dict:
        """Get goal suggestion from Gemini API."""
        prompt = f"""Based on these fitness metrics:
- BMI: {bmi}
- Maintenance Calories: {maintenance_calories}

Suggest ONE fitness goal (lose, gain, or maintain) and provide a brief explanation.
Also estimate weekly weight change if they follow a caloric deficit/surplus.
Respond in JSON format: {{"goal": "...", "explanation": "...", "projection": "..."}}"""
        
        # This is a simplified version - actual implementation would call Gemini API
        response = {
            "goal": "maintain" if 18.5 <= bmi < 25 else "lose" if bmi >= 25 else "gain",
            "explanation": "Based on your current metrics.",
            "projection": "Approximately 0.5 kg/week"
        }
        
        target_calories = maintenance_calories * (0.85 if response["goal"] == "lose" 
                                                 else 1.15 if response["goal"] == "gain" 
                                                 else 1.0)
        
        return {
            "suggested_goal": response["goal"],
            "explanation": response["explanation"],
            "target_calories": target_calories,
            "weekly_projection": response["projection"]
        }
    
    @staticmethod
    def _openai_goal_suggestion(bmi: float, maintenance_calories: float) -> dict:
        """Get goal suggestion from OpenAI API."""
        # Similar to Gemini but using OpenAI
        response = {
            "goal": "maintain" if 18.5 <= bmi < 25 else "lose" if bmi >= 25 else "gain",
            "explanation": "Based on your current metrics.",
            "projection": "Approximately 0.5 kg/week"
        }
        
        target_calories = maintenance_calories * (0.85 if response["goal"] == "lose" 
                                                 else 1.15 if response["goal"] == "gain" 
                                                 else 1.0)
        
        return {
            "suggested_goal": response["goal"],
            "explanation": response["explanation"],
            "target_calories": target_calories,
            "weekly_projection": response["projection"]
        }
    
    @staticmethod
    def generate_weekly_report(user_data: dict, weekly_summary: dict) -> str:
        """Generate weekly health report with AI.
        
        Args:
            user_data: User profile data
            weekly_summary: Weekly meal and calorie summary
            
        Returns:
            Generated report text
        """
        report = f"""
Weekly Health Report
====================

User: {user_data.get('name', 'User')}
Goal: {user_data.get('fitness_goal', 'N/A')}
Target Calories: {user_data.get('target_calories', 0)}/day

Weekly Summary:
- Total Days Tracked: {weekly_summary.get('days_tracked', 0)}
- Average Daily Calories: {weekly_summary.get('avg_calories', 0)}
- Average Protein: {weekly_summary.get('avg_protein', 0)}g
- Average Carbs: {weekly_summary.get('avg_carbs', 0)}g
- Average Fats: {weekly_summary.get('avg_fats', 0)}g

Insights:
- You logged meals for {weekly_summary.get('days_tracked', 0)} days this week.
- Your average daily intake was {weekly_summary.get('avg_calories', 0)} calories.
- {AIService._generate_insights(weekly_summary)}

Recommendations:
1. Continue tracking your meals consistently
2. Focus on balanced macronutrient distribution
3. Stay hydrated and get adequate rest

Keep up the great work!
"""
        return report
    
    @staticmethod
    def _generate_insights(summary: dict) -> str:
        """Generate insights from weekly summary."""
        avg_cal = summary.get('avg_calories', 0)
        target = summary.get('target_calories', 0)
        
        if avg_cal > target * 1.1:
            return f"You're exceeding your target by about {avg_cal - target:.0f} calories on average."
        elif avg_cal < target * 0.9:
            return f"You're consuming about {target - avg_cal:.0f} calories below your target."
        else:
            return "You're doing great staying close to your target!"
    
    @staticmethod
    def chat(message: str, user_data: dict = None, history: List[Dict] = None) -> str:
        """Fitness chatbot response.
        
        Args:
            message: User message
            user_data: User profile data
            history: Chat history
            
        Returns:
            Chatbot response
        """
        message_lower = message.lower()
        
        # Simple rule-based responses (can be replaced with actual LLM)
        if any(word in message_lower for word in ['dinner', 'lunch', 'breakfast', 'eat', 'food']):
            return "I'd recommend focusing on balanced meals with adequate protein and vegetables. What's your current fitness goal?"
        
        elif any(word in message_lower for word in ['calories', 'goal', 'track']):
            if user_data:
                return f"Based on your profile, your daily target is {user_data.get('target_calories', 0)} calories. Keep logging meals to track your progress!"
            return "Track your meals consistently to stay on target with your fitness goals."
        
        elif any(word in message_lower for word in ['macro', 'protein', 'carbs', 'fat']):
            return "A good macro balance depends on your goals. Typically: 30-35% protein, 40-50% carbs, 20-30% fats. Would you like personalized recommendations?"
        
        elif any(word in message_lower for word in ['progress', 'track', 'losing', 'gaining']):
            return "Great! Keep logging your meals daily. Remember consistency is key to achieving your fitness goals."
        
        else:
            return "I'm here to help with your fitness journey! Ask me about meals, macros, your goals, or how you're tracking."
