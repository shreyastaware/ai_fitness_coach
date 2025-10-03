import React from 'react';
import { Phone, MessageCircle, Brain, Activity, Calendar, Shield } from 'lucide-react';

const Features = () => {
  const features = [
    {
      icon: Phone,
      title: 'Voice-Based Coaching',
      description: 'Get personalized workout instructions and motivation through daily phone calls from your AI coach.',
      gradient: 'from-green-400 to-green-600'
    },
    {
      icon: MessageCircle,
      title: 'AI Chatbot Support',
      description: '24/7 instant answers to your health and fitness questions through our intelligent chat assistant.',
      gradient: 'from-blue-400 to-blue-600'
    },
    {
      icon: Brain,
      title: 'Personalized Plans',
      description: 'Custom workout and nutrition plans tailored to your goals, fitness level, and dietary preferences.',
      gradient: 'from-purple-400 to-purple-600'
    },
    {
      icon: Activity,
      title: 'Real-Time Tracking',
      description: 'Monitor your progress with detailed analytics and receive adaptive coaching based on your performance.',
      gradient: 'from-red-400 to-red-600'
    },
    {
      icon: Calendar,
      title: 'Smart Scheduling',
      description: 'Flexible workout scheduling that adapts to your calendar and lifestyle for maximum consistency.',
      gradient: 'from-yellow-400 to-yellow-600'
    },
    {
      icon: Shield,
      title: 'Privacy First',
      description: 'Your health data is encrypted and secure. We never share your personal information with third parties.',
      gradient: 'from-indigo-400 to-indigo-600'
    }
  ];

  return (
    <section id="features" className="py-20 bg-gradient-to-br from-gray-50 to-green-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-6">
            Powerful <span className="bg-gradient-to-r from-green-500 to-green-600 bg-clip-text text-transparent">Features</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Everything you need to achieve your fitness goals with the power of artificial intelligence.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="group">
              <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 border border-white/50 hover:bg-white/90 transition-all duration-300 hover:shadow-xl hover:-translate-y-2 h-full">
                <div className={`w-14 h-14 bg-gradient-to-br ${feature.gradient} rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <feature.icon className="w-7 h-7 text-white" />
                </div>
                
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  {feature.title}
                </h3>
                
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;