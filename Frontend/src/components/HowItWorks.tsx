import React from 'react';
import { Target, Phone, TrendingUp } from 'lucide-react';

const HowItWorks = () => {
  const steps = [
    {
      number: '01',
      icon: Target,
      title: 'Set Your Fitness Goal',
      description: 'Tell us about your fitness level, goals, and preferences. Our AI analyzes your data to create a personalized plan.'
    },
    {
      number: '02',
      icon: Phone,
      title: 'Get Daily AI Calls',
      description: 'Receive motivational calls every morning with your daily workout plan, nutrition tips, and progress check-ins.'
    },
    {
      number: '03',
      icon: TrendingUp,
      title: 'Track Your Progress',
      description: 'Monitor your improvements through our app. Your AI coach adapts your plan based on your progress and feedback.'
    }
  ];

  return (
    <section id="how-it-works" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-6">
            How It <span className="bg-gradient-to-r from-green-500 to-green-600 bg-clip-text text-transparent">Works</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Get started with your AI fitness coach in three simple steps and transform your health journey forever.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 lg:gap-12">
          {steps.map((step, index) => (
            <div key={index} className="relative group">
              <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-8 border border-gray-200/50 hover:border-green-200 transition-all duration-300 hover:shadow-xl hover:-translate-y-2">
                <div className="flex items-center mb-6">
                  <div className="text-4xl font-bold text-green-100 mr-4">{step.number}</div>
                  <div className="w-12 h-12 bg-gradient-to-br from-green-400 to-green-600 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                    <step.icon className="w-6 h-6 text-white" />
                  </div>
                </div>
                
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  {step.title}
                </h3>
                
                <p className="text-gray-600 leading-relaxed">
                  {step.description}
                </p>
              </div>

              {/* Connection line */}
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-1/2 -right-6 lg:-right-12 w-6 lg:w-12 h-0.5 bg-gradient-to-r from-green-300 to-green-400 transform -translate-y-1/2"></div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;