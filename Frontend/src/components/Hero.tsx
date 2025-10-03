import React from 'react';
import { Phone, Play, ArrowRight } from 'lucide-react';

const Hero = () => {
  return (
    <section className="min-h-screen bg-gradient-to-br from-green-50 via-white to-green-50 pt-20 relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-20 left-10 w-72 h-72 bg-green-400 rounded-full blur-3xl"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-green-300 rounded-full blur-3xl"></div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
        <div className="flex flex-col lg:flex-row items-center min-h-screen">
          <div className="flex-1 text-center lg:text-left mb-12 lg:mb-0">
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-gray-900 leading-tight mb-6">
              Meet Your AI Fitness Coach That{' '}
              <span className="bg-gradient-to-r from-green-500 to-green-600 bg-clip-text text-transparent">
                Calls You
              </span>{' '}
              Every Morning
            </h1>
            
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto lg:mx-0">
              Get personalized workout plans, nutrition guidance, and daily motivation calls from your AI fitness coach. 
              Transform your health with the power of artificial intelligence.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <button className="group bg-gradient-to-r from-green-500 to-green-600 text-white px-8 py-4 rounded-full text-lg font-semibold hover:from-green-600 hover:to-green-700 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl">
                Get Started Free
                <ArrowRight className="inline-block ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </button>
              
              <button className="group bg-white/80 backdrop-blur-sm text-gray-900 px-8 py-4 rounded-full text-lg font-semibold border border-gray-200 hover:bg-white hover:shadow-lg transition-all duration-300 transform hover:scale-105">
                <Play className="inline-block mr-2 w-5 h-5 group-hover:scale-110 transition-transform" />
                Try a Demo
              </button>
            </div>

            <div className="mt-12 flex items-center justify-center lg:justify-start space-x-8 text-sm text-gray-500">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                No credit card required
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                Free 14-day trial
              </div>
            </div>
          </div>

          <div className="flex-1 relative">
            <div className="relative max-w-md mx-auto">
              {/* Phone mockup */}
              <div className="relative z-10 bg-gradient-to-br from-gray-900 to-black rounded-[3rem] p-2 shadow-2xl">
                <div className="bg-white rounded-[2.5rem] p-6 h-[600px] relative overflow-hidden">
                  <div className="absolute top-6 left-1/2 transform -translate-x-1/2 w-32 h-6 bg-black rounded-full"></div>
                  
                  <div className="mt-12 space-y-6">
                    <div className="text-center">
                      <div className="w-16 h-16 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                        <Phone className="w-8 h-8 text-white" />
                      </div>
                      <h3 className="text-lg font-semibold text-gray-900">Morning Call</h3>
                      <p className="text-sm text-gray-600">AI Coach Sarah</p>
                    </div>

                    <div className="bg-gradient-to-r from-green-50 to-green-100 rounded-2xl p-4">
                      <p className="text-sm text-gray-800">"Good morning! Ready for today's 20-minute HIIT workout? I've customized it based on your progress."</p>
                    </div>

                    <div className="space-y-3">
                      <div className="bg-gray-50 rounded-xl p-3">
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-medium">Today's Workout</span>
                          <span className="text-xs text-green-600">20 min</span>
                        </div>
                      </div>
                      
                      <div className="bg-gray-50 rounded-xl p-3">
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-medium">Calories Goal</span>
                          <span className="text-xs text-green-600">300 kcal</span>
                        </div>
                      </div>
                    </div>

                    <button className="w-full bg-gradient-to-r from-green-500 to-green-600 text-white py-3 rounded-xl font-medium">
                      Start Workout
                    </button>
                  </div>
                </div>
              </div>

              {/* Floating elements */}
              <div className="absolute -top-4 -left-4 w-20 h-20 bg-gradient-to-br from-green-400/20 to-green-600/20 rounded-full backdrop-blur-sm flex items-center justify-center animate-pulse">
                <Phone className="w-8 h-8 text-green-600" />
              </div>
              
              <div className="absolute -bottom-4 -right-4 w-16 h-16 bg-gradient-to-br from-green-300/20 to-green-500/20 rounded-full backdrop-blur-sm animate-bounce"></div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;