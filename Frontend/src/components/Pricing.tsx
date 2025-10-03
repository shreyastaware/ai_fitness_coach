import React from 'react';
import { Check, Phone, MessageCircle, Crown } from 'lucide-react';

const Pricing = () => {
  const plans = [
    {
      name: 'Free',
      price: '$0',
      period: 'forever',
      description: 'Perfect for getting started with AI fitness coaching',
      features: [
        'Basic workout plans',
        'Weekly progress tracking',
        'Limited chat support',
        'Community access',
        'Basic nutrition tips'
      ],
      cta: 'Start Free',
      popular: false,
      gradient: 'from-gray-400 to-gray-600'
    },
    {
      name: 'Premium',
      price: '$29',
      period: 'per month',
      description: 'Complete AI fitness coaching with daily calls and personalized plans',
      features: [
        'Daily AI coaching calls',
        'Personalized workout plans',
        '24/7 AI chat support',
        'Advanced progress analytics',
        'Custom nutrition plans',
        'Priority customer support',
        'Integration with fitness apps',
        'Unlimited plan adjustments'
      ],
      cta: 'Start Premium',
      popular: true,
      gradient: 'from-green-500 to-green-600'
    }
  ];

  return (
    <section id="pricing" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-6">
            Simple <span className="bg-gradient-to-r from-green-500 to-green-600 bg-clip-text text-transparent">Pricing</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Choose the plan that fits your fitness journey. Start free and upgrade when you're ready for more.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {plans.map((plan, index) => (
            <div key={index} className={`relative group ${plan.popular ? 'transform scale-105' : ''}`}>
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 bg-gradient-to-r from-green-500 to-green-600 text-white px-6 py-2 rounded-full text-sm font-semibold flex items-center">
                  <Crown className="w-4 h-4 mr-1" />
                  Most Popular
                </div>
              )}
              
              <div className={`bg-white rounded-2xl border-2 ${
                plan.popular ? 'border-green-500 shadow-xl' : 'border-gray-200'
              } p-8 relative overflow-hidden transition-all duration-300 hover:shadow-xl`}>
                
                <div className="text-center mb-8">
                  <h3 className="text-2xl font-bold text-gray-900 mb-4">{plan.name}</h3>
                  <div className="mb-4">
                    <span className="text-5xl font-bold text-gray-900">{plan.price}</span>
                    <span className="text-lg text-gray-600">/{plan.period}</span>
                  </div>
                  <p className="text-gray-600">{plan.description}</p>
                </div>

                <ul className="space-y-4 mb-8">
                  {plan.features.map((feature, featureIndex) => (
                    <li key={featureIndex} className="flex items-center">
                      <Check className="w-5 h-5 text-green-500 mr-3 flex-shrink-0" />
                      <span className="text-gray-700">{feature}</span>
                    </li>
                  ))}
                </ul>

                <button className={`w-full py-4 px-6 rounded-xl font-semibold text-lg transition-all duration-300 ${
                  plan.popular 
                    ? 'bg-gradient-to-r from-green-500 to-green-600 text-white hover:from-green-600 hover:to-green-700 transform hover:scale-105' 
                    : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
                }`}>
                  {plan.cta}
                </button>

                {plan.popular && (
                  <div className="flex items-center justify-center mt-4 space-x-4 text-sm text-gray-500">
                    <div className="flex items-center">
                      <Phone className="w-4 h-4 mr-1" />
                      Daily calls
                    </div>
                    <div className="flex items-center">
                      <MessageCircle className="w-4 h-4 mr-1" />
                      24/7 support
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="text-center mt-12">
          <p className="text-gray-600">
            All plans include a <span className="font-semibold text-green-600">14-day free trial</span>. 
            No credit card required for the free plan.
          </p>
        </div>
      </div>
    </section>
  );
};

export default Pricing;