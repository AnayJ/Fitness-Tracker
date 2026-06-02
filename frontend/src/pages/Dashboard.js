import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { dashboardService, mealService, aiService } from '../services/api';
import { Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { LogOut, Plus, TrendingDown, MessageCircle, BarChart3, Moon, Sun, Trash2 } from 'lucide-react';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

export default function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [chatMessage, setChatMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [chatSuggestedAction, setChatSuggestedAction] = useState(null);
  const { darkMode, toggleDarkMode } = useTheme();
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    setLoading(true);
    try {
      const response = await dashboardService.getSummary();
      setDashboard(response.data);
      if (response.data.prediction) {
        setPrediction(response.data.prediction);
      }
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSendChat = async (e) => {
    e.preventDefault();
    if (!chatMessage.trim()) return;

    const newHistory = [...chatHistory, { role: 'user', content: chatMessage }];
    setChatHistory(newHistory);
    setChatMessage('');

    try {
      const response = await aiService.chat(chatMessage, newHistory);
      setChatHistory((prev) => [
        ...prev,
        { role: 'assistant', content: response.data.response },
      ]);
      setChatSuggestedAction(response.data.suggested_action || null);
    } catch (error) {
      console.error('Error sending chat:', error);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleDeleteMeal = async (mealId) => {
    if (!window.confirm('Are you sure you want to delete this meal?')) {
      return;
    }

    try {
      await mealService.deleteMeal(mealId);
      await loadDashboard();
    } catch (error) {
      console.error('Error deleting meal:', error);
      alert('Failed to delete meal');
    }
  };
  if (loading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  if (!dashboard) {
    return <div className="flex justify-center items-center h-screen">No data available</div>;
  }

  const macroData = {
    labels: ['Protein', 'Carbs', 'Fats'],
    datasets: [
      {
        data: [dashboard.protein, dashboard.carbs, dashboard.fats],
        backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
        borderColor: ['#059669', '#d97706', '#dc2626'],
        borderWidth: 2,
      },
    ],
  };

  const caloriePercentage = (dashboard.consumed_calories / dashboard.target_calories) * 100;

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'}`}>
      {/* Header */}
      <header className={`${darkMode ? 'bg-gray-800' : 'bg-white'} shadow`}>
        <div className="max-w-7xl mx-auto px-4 py-6 flex justify-between items-center">
          <div>
            <h1 className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-800'}`}>Welcome, {user?.name}!</h1>
            <p className={darkMode ? 'text-gray-400' : 'text-gray-600'}>Track your daily nutrition</p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={toggleDarkMode}
              className={`p-2 rounded-lg transition ${
                darkMode
                  ? 'bg-gray-700 text-yellow-400 hover:bg-gray-600'
                  : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
              }`}
              title={darkMode ? 'Light mode' : 'Dark mode'}
            >
              {darkMode ? <Sun size={20} /> : <Moon size={20} />}
            </button>
            <button
              onClick={() => navigate('/weekly-report')}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              <BarChart3 size={20} />
              Weekly Report
            </button>
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
            >
              <LogOut size={20} />
              Logout
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Calorie and Macros */}
          <div className="lg:col-span-2 space-y-6">
            {/* Calorie Progress */}
            <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-6`}>
              <h2 className={`text-xl font-bold ${darkMode ? 'text-white' : 'text-gray-800'} mb-4`}>Daily Progress</h2>
              
              <div className="mb-6">
                <div className="flex justify-between items-center mb-2">
                  <span className={`${darkMode ? 'text-gray-300' : 'text-gray-700'} font-semibold`}>
                    {Math.round(dashboard.consumed_calories)} / {Math.round(dashboard.target_calories)} calories
                  </span>
                  <span className={darkMode ? 'text-gray-400' : 'text-gray-600'}>{caloriePercentage.toFixed(0)}%</span>
                </div>
                <div className={`w-full h-4 ${darkMode ? 'bg-gray-700' : 'bg-gray-200'} rounded-full overflow-hidden`}>
                  <div
                    className={`h-full transition-all ${
                      caloriePercentage > 100 ? 'bg-red-500' : 'bg-green-500'
                    }`}
                    style={{ width: `${Math.min(caloriePercentage, 100)}%` }}
                  />
                </div>
                {dashboard.remaining_calories > 0 && (
                  <p className="text-green-600 mt-2 font-semibold">
                    {Math.round(dashboard.remaining_calories)} calories remaining
                  </p>
                )}
                {dashboard.exceeded && (
                  <p className="text-red-600 mt-2 font-semibold flex items-center gap-2">
                    <TrendingDown size={18} />
                    Exceeded by {Math.round(dashboard.consumed_calories - dashboard.target_calories)} calories
                  </p>
                )}
              </div>

              {/* Prediction */}
              {prediction && (
                <div className={`p-4 rounded-lg ${
                  prediction.will_exceed
                    ? darkMode
                      ? 'bg-red-900 border border-red-700 text-red-100'
                      : 'bg-red-50 border border-red-200 text-red-900'
                    : darkMode
                      ? 'bg-gray-800 border border-gray-700 text-green-200'
                      : 'bg-green-50 border border-green-200 text-green-900'
                }`}>
                  <p className={`text-sm font-semibold mb-2 ${
                    prediction.will_exceed
                      ? darkMode ? 'text-red-100' : 'text-red-700'
                      : darkMode ? 'text-green-200' : 'text-green-700'
                  }`}>
                    {prediction.will_exceed ? 'Projected to exceed!' : 'On track!'}
                  </p>
                  <p className={`text-sm ${
                    prediction.will_exceed
                      ? darkMode ? 'text-red-200' : 'text-red-600'
                      : darkMode ? 'text-gray-300' : 'text-gray-600'
                  }`}>
                    Projected total: {Math.round(prediction.projected_total)} calories
                    ({prediction.confidence.toFixed(0)}% confidence)
                  </p>
                </div>
              )}
            </div>

            {/* Macro Breakdown */}
            <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-6`}>
              <h2 className={`text-xl font-bold ${darkMode ? 'text-white' : 'text-gray-800'} mb-4`}>Macro Breakdown</h2>
              <div className="flex justify-center mb-4">
                <div className="w-40 h-40 md:w-60 md:h-60">
                  <Doughnut data={macroData} options={{ maintainAspectRatio: true }} />
                </div>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">
                <div className={`rounded-3xl p-4 min-h-[130px] flex flex-col justify-center items-center ${darkMode ? 'bg-gray-900 border border-gray-700' : 'bg-gray-100 border border-gray-200'}`}>
                  <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Protein</p>
                  <p className="text-3xl font-bold text-green-600 mt-3">{Math.round(dashboard.protein)}g</p>
                </div>
                <div className={`rounded-3xl p-4 min-h-[130px] flex flex-col justify-center items-center ${darkMode ? 'bg-gray-900 border border-gray-700' : 'bg-gray-100 border border-gray-200'}`}>
                  <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Carbs</p>
                  <p className="text-3xl font-bold text-amber-600 mt-3">{Math.round(dashboard.carbs)}g</p>
                </div>
                <div className={`rounded-3xl p-4 min-h-[130px] flex flex-col justify-center items-center ${darkMode ? 'bg-gray-900 border border-gray-700' : 'bg-gray-100 border border-gray-200'}`}>
                  <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Fats</p>
                  <p className="text-3xl font-bold text-red-600 mt-3">{Math.round(dashboard.fats)}g</p>
                </div>
              </div>
            </div>

            {/* Meals List */}
            <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-6`}>
              <div className="flex justify-between items-center mb-4">
                <h2 className={`text-xl font-bold ${darkMode ? 'text-white' : 'text-gray-800'}`}>Today's Meals ({dashboard.meal_count})</h2>
                <button
                  onClick={() => navigate('/meal-entry')}
                  className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
                >
                  <Plus size={20} />
                  Add Meal
                </button>
              </div>

              {dashboard.meals.length === 0 ? (
                <p className={`${darkMode ? 'text-gray-400' : 'text-gray-600'} text-center py-4`}>No meals logged yet</p>
              ) : (
                <div className="space-y-3">
                  {dashboard.meals.map((meal) => (
                    <div
                      key={meal.id}
                      className={`p-4 rounded-lg ${
                        darkMode
                          ? 'border border-gray-700 hover:bg-gray-700'
                          : 'border border-gray-200 hover:bg-gray-50'
                      }`}
                    >
                      <div className="flex justify-between items-start mb-2">
                        <h3 className={`font-semibold ${darkMode ? 'text-white' : 'text-gray-800'}`}>{meal.name}</h3>
                        <div className="flex items-center gap-2">
                          <span className="bg-indigo-100 text-indigo-800 px-2 py-1 rounded text-sm font-semibold">
                            {Math.round(meal.calories)} cal
                          </span>
                          <button
                            onClick={() => handleDeleteMeal(meal.id)}
                            className="text-red-600 hover:text-red-700 transition p-1"
                            title="Delete meal"
                          >
                            <Trash2 size={18} />
                          </button>
                        </div>
                      </div>
                      {meal.description && (
                        <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'} mb-2`}>{meal.description}</p>
                      )}
                      <div className={`flex gap-4 text-xs ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                        <span>🥛 {meal.protein}g protein</span>
                        <span>🌾 {meal.carbs}g carbs</span>
                        <span>🧈 {meal.fats}g fats</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Right Column - AI Chat (hidden on small screens for clarity) */}
          <div className="lg:col-span-1 hidden lg:block">
            <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-4 flex flex-col sticky top-4 max-h-[calc(100vh-120px)]`}>
              <h2 className={`text-lg font-bold ${darkMode ? 'text-white' : 'text-gray-800'} mb-2 flex items-center gap-2 flex-shrink-0`}>
                <MessageCircle size={20} />
                Fitness AI
              </h2>

              <div className={`flex-1 overflow-y-auto space-y-2 p-3 rounded-lg min-h-0 ${
                darkMode ? 'bg-gray-900' : 'bg-gray-50'
              }`}>
                <div className={`rounded-lg p-2 text-xs ${darkMode ? 'bg-gray-800 text-gray-300' : 'bg-gray-100 text-gray-700'}`}>
                  Try asking: "What are my maintenance calories?", "How many calories should I eat for a deficit?", or "Help me calculate daily macros."
                </div>
                {chatSuggestedAction && (
                  <div className={`rounded-lg p-2 text-sm font-medium ${darkMode ? 'bg-indigo-700 text-indigo-100' : 'bg-indigo-100 text-indigo-900'}`}>
                    {chatSuggestedAction}
                  </div>
                )}
                {chatHistory.length === 0 && (
                  <p className={`${darkMode ? 'text-gray-500' : 'text-gray-500'} text-sm text-center py-4`}>
                    Ask me anything about your fitness journey!
                  </p>
                )}
                {chatHistory.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`p-2 rounded-lg text-sm ${
                      msg.role === 'user'
                        ? 'bg-indigo-100 text-indigo-900 ml-4'
                        : darkMode ? 'bg-gray-700 text-gray-100 mr-4' : 'bg-gray-200 text-gray-900 mr-4'
                    }`}
                  >
                    {msg.content}
                  </div>
                ))}
              </div>

              <form onSubmit={handleSendChat} className="flex gap-2 flex-shrink-0 mt-2">
                <input
                  type="text"
                  value={chatMessage}
                  onChange={(e) => setChatMessage(e.target.value)}
                  placeholder="Ask me..."
                  className={`flex-1 px-3 py-2 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 ${
                    darkMode
                      ? 'bg-gray-700 border border-gray-600 text-white placeholder-gray-400'
                      : 'border border-gray-300 text-gray-900'
                  }`}
                />
                <button
                  type="submit"
                  className="px-3 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
                >
                  Send
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
