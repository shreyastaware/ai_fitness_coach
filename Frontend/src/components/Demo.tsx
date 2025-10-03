import React, { useState } from 'react';
import { MessageCircle, Send, Phone, Volume2 } from 'lucide-react';

const Demo = () => {
  const [messages, setMessages] = useState([
    { type: 'bot', text: "Hi! I'm your AI fitness coach. What's your fitness goal?" },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isVoiceActive, setIsVoiceActive] = useState(false);

  const botResponses = [
    "That's a great goal! Based on your preference, I'd recommend starting with 3 workouts per week.",
    "Perfect! I can create a personalized plan for you. Would you prefer morning or evening workouts?",
    "Excellent choice! I'll schedule your daily motivation calls for 7 AM. Ready to get started?",
    "I'll help you track your progress and adjust your plan as needed. Let's begin your fitness journey!"
  ];

  const handleSendMessage = () => {
    if (!inputValue.trim()) return;

    const newMessages = [...messages, { type: 'user', text: inputValue }];
    setMessages(newMessages);
    setInputValue('');

    // Simulate bot response
    setTimeout(() => {
      const randomResponse = botResponses[Math.floor(Math.random() * botResponses.length)];
      setMessages([...newMessages, { type: 'bot', text: randomResponse }]);
    }, 1000);
  };

  const handleVoiceDemo = () => {
    setIsVoiceActive(!isVoiceActive);
    if (!isVoiceActive) {
      setTimeout(() => setIsVoiceActive(false), 3000);
    }
  };

  return (
    <section id="demo" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-6">
            Try Our <span className="bg-gradient-to-r from-green-500 to-green-600 bg-clip-text text-transparent">AI Coach</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Experience the power of AI-driven fitness coaching. Chat with our bot or try our voice assistant.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-12 max-w-6xl mx-auto">
          {/* Chat Demo */}
          <div className="bg-gradient-to-br from-white to-gray-50 rounded-2xl border border-gray-200 overflow-hidden shadow-xl">
            <div className="bg-gradient-to-r from-green-500 to-green-600 p-4 text-white">
              <div className="flex items-center">
                <MessageCircle className="w-6 h-6 mr-3" />
                <div>
                  <h3 className="font-semibold">AI Fitness Chat</h3>
                  <p className="text-sm opacity-90">Get instant fitness advice</p>
                </div>
              </div>
            </div>

            <div className="h-80 overflow-y-auto p-4 space-y-4">
              {messages.map((message, index) => (
                <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-xs px-4 py-2 rounded-2xl ${
                    message.type === 'user' 
                      ? 'bg-green-500 text-white rounded-br-md' 
                      : 'bg-gray-100 text-gray-800 rounded-bl-md'
                  }`}>
                    {message.text}
                  </div>
                </div>
              ))}
            </div>

            <div className="p-4 border-t border-gray-200">
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Ask about workouts, nutrition, or goals..."
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
                <button
                  onClick={handleSendMessage}
                  className="bg-green-500 text-white p-2 rounded-full hover:bg-green-600 transition-colors"
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>

          {/* Voice Demo */}
          <div className="bg-gradient-to-br from-white to-gray-50 rounded-2xl border border-gray-200 overflow-hidden shadow-xl">
            <div className="bg-gradient-to-r from-blue-500 to-blue-600 p-4 text-white">
              <div className="flex items-center">
                <Phone className="w-6 h-6 mr-3" />
                <div>
                  <h3 className="font-semibold">Voice Assistant</h3>
                  <p className="text-sm opacity-90">Experience voice coaching</p>
                </div>
              </div>
            </div>

            <div className="h-80 p-8 flex flex-col items-center justify-center">
              <div className={`w-32 h-32 rounded-full border-4 ${
                isVoiceActive ? 'border-green-500 animate-pulse' : 'border-gray-300'
              } flex items-center justify-center mb-8 transition-all duration-300`}>
                <Volume2 className={`w-12 h-12 ${isVoiceActive ? 'text-green-500' : 'text-gray-400'}`} />
              </div>

              <button
                onClick={handleVoiceDemo}
                disabled={isVoiceActive}
                className={`px-8 py-3 rounded-full font-semibold transition-all duration-300 ${
                  isVoiceActive 
                    ? 'bg-green-500 text-white' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {isVoiceActive ? 'Listening...' : 'Try Voice Demo'}
              </button>

              <p className="text-sm text-gray-500 mt-4 text-center">
                {isVoiceActive 
                  ? '"Good morning! Ready for today\'s workout? I\'ve prepared a 20-minute session for you."'
                  : 'Click to hear a sample coaching call'
                }
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Demo;