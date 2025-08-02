import React, { useState } from 'react';
import { Menu, X, Phone, MessageCircle } from 'lucide-react';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="fixed top-0 w-full bg-white/80 backdrop-blur-md border-b border-gray-200/20 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-green-400 to-green-600 rounded-lg flex items-center justify-center">
              <Phone className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">FitCoach AI</span>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <a href="#how-it-works" className="text-gray-700 hover:text-green-600 transition-colors">How It Works</a>
            <a href="#features" className="text-gray-700 hover:text-green-600 transition-colors">Features</a>
            <a href="#demo" className="text-gray-700 hover:text-green-600 transition-colors">Demo</a>
            <a href="#pricing" className="text-gray-700 hover:text-green-600 transition-colors">Pricing</a>
            <button className="bg-gradient-to-r from-green-500 to-green-600 text-white px-6 py-2 rounded-full hover:from-green-600 hover:to-green-700 transition-all duration-300 transform hover:scale-105">
              Get Started
            </button>
          </nav>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden border-t border-gray-200/20 py-4">
            <nav className="flex flex-col space-y-4">
              <a href="#how-it-works" className="text-gray-700 hover:text-green-600 transition-colors">How It Works</a>
              <a href="#features" className="text-gray-700 hover:text-green-600 transition-colors">Features</a>
              <a href="#demo" className="text-gray-700 hover:text-green-600 transition-colors">Demo</a>
              <a href="#pricing" className="text-gray-700 hover:text-green-600 transition-colors">Pricing</a>
              <button className="bg-gradient-to-r from-green-500 to-green-600 text-white px-6 py-2 rounded-full hover:from-green-600 hover:to-green-700 transition-all duration-300 w-fit">
                Get Started
              </button>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;