"""Utility functions for calculations."""
import math


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """Calculate BMI from weight and height.
    
    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
        
    Returns:
        BMI value
    """
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)


def calculate_maintenance_calories(weight_kg: float, height_cm: float, 
                                   age: int = 30, gender: str = "M") -> float:
    """Calculate maintenance calories using Mifflin-St Jeor formula.
    
    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
        age: Age in years (default: 30)
        gender: Gender "M" or "F" (default: "M")
        
    Returns:
        Maintenance calories per day
    """
    if gender.upper() == "M":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    
    # Assume moderate activity level (1.55)
    maintenance_calories = bmr * 1.55
    return round(maintenance_calories, 0)


def calculate_macro_percentages(protein_g: float, carbs_g: float, fats_g: float) -> dict:
    """Calculate macro percentages from grams.
    
    Args:
        protein_g: Protein in grams
        carbs_g: Carbs in grams
        fats_g: Fats in grams
        
    Returns:
        Dictionary with calorie and percentage breakdowns
    """
    protein_cal = protein_g * 4
    carbs_cal = carbs_g * 4
    fats_cal = fats_g * 9
    
    total_cal = protein_cal + carbs_cal + fats_cal
    
    if total_cal == 0:
        return {
            "protein_calories": 0,
            "carbs_calories": 0,
            "fats_calories": 0,
            "protein_percent": 0,
            "carbs_percent": 0,
            "fats_percent": 0
        }
    
    return {
        "protein_calories": protein_cal,
        "carbs_calories": carbs_cal,
        "fats_calories": fats_cal,
        "protein_percent": round((protein_cal / total_cal) * 100, 1),
        "carbs_percent": round((carbs_cal / total_cal) * 100, 1),
        "fats_percent": round((fats_cal / total_cal) * 100, 1)
    }


def estimate_weight_change(calorie_deficit: float) -> dict:
    """Estimate weekly weight change from calorie deficit/surplus.
    
    Args:
        calorie_deficit: Daily calorie deficit (negative) or surplus (positive)
        
    Returns:
        Dictionary with weekly estimates
    """
    # 1 kg of body weight ≈ 7700 calories
    weekly_deficit = calorie_deficit * 7
    weekly_weight_change = weekly_deficit / 7700
    
    return {
        "daily_deficit": calorie_deficit,
        "weekly_change_kg": round(weekly_weight_change, 2),
        "weekly_change_lbs": round(weekly_weight_change * 2.2, 2),
        "monthly_change_kg": round(weekly_weight_change * 4, 2),
        "monthly_change_lbs": round(weekly_weight_change * 2.2 * 4, 2)
    }
