import React from 'react';
import { Star, Quote } from 'lucide-react';

const Testimonials = () => {
  const testimonials = [
    {
      name: 'Sarah Johnson',
      role: 'Marketing Manager',
      image: 'https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=300&h=300&dpr=2',
      content: "The daily motivation calls are a game-changer! My AI coach keeps me accountable and adjusts my workouts based on my progress. I've lost 25 pounds in 3 months!",
      rating: 5
    },
    {
      name: 'Michael Chen',
      role: 'Software Developer',
      image: 'https://images.pexels.com/photos/91227/pexels-photo-91227.jpeg?auto=compress&cs=tinysrgb&w=300&h=300&dpr=2',
      content: "As someone with a busy schedule, having an AI coach that calls me every morning is perfect. The workouts are efficient and the nutrition advice is spot-on.",
      rating: 5
    },
    {
      name: 'Emma Rodriguez',
      role: 'Nurse',
      image: 'https://images.pexels.com/photos/712513/pexels-photo-712513.jpeg?auto=compress&cs=tinysrgb&w=300&h=300&dpr=2',
      content: "I was skeptical about AI coaching, but this exceeded my expectations. The personalized approach and consistent motivation helped me stick to my fitness goals.",
      rating: 5
    },
    {
      name: 'David Thompson',
      role: 'Business Owner',
      image: 'https://images.pexels.com/photos/1681010/pexels-photo-1681010.jpeg?auto=compress&cs=tinysrgb&w=300&h=300&dpr=2',
      content: "The 24/7 chat support is incredible. Whenever I have questions about exercises or nutrition, I get instant, helpful responses. It's like having a personal trainer in my pocket.",
      rating: 5
    }
  ];

  return (
    <section className="py-20 bg-gradient-to-br from-green-50 to-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-6">
            What Our <span className="bg-gradient-to-r from-green-500 to-green-600 bg-clip-text text-transparent">Users Say</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Join thousands of people who have transformed their fitness journey with our AI coach.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
          {testimonials.map((testimonial, index) => (
            <div key={index} className="group">
              <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 border border-white/50 hover:bg-white/90 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 relative">
                <Quote className="absolute top-4 right-4 w-8 h-8 text-green-200" />
                
                <div className="flex items-center mb-6">
                  <img
                    src={testimonial.image}
                    alt={testimonial.name}
                    className="w-16 h-16 rounded-full object-cover mr-4"
                  />
                  <div>
                    <h4 className="font-semibold text-gray-900">{testimonial.name}</h4>
                    <p className="text-sm text-gray-600">{testimonial.role}</p>
                  </div>
                </div>

                <div className="flex mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                  ))}
                </div>

                <p className="text-gray-700 leading-relaxed italic">
                  "{testimonial.content}"
                </p>
              </div>
            </div>
          ))}
        </div>

        <div className="text-center mt-12">
          <div className="flex items-center justify-center space-x-8 text-sm text-gray-500">
            <div className="flex items-center">
              <Star className="w-5 h-5 text-yellow-400 fill-current mr-1" />
              <span className="font-semibold">4.9/5</span> average rating
            </div>
            <div>
              <span className="font-semibold">50,000+</span> active users
            </div>
            <div>
              <span className="font-semibold">1M+</span> workouts completed
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Testimonials;