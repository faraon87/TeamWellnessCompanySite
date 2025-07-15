import React, { useState } from 'react';
import { motion } from 'framer-motion';
import Button from '../common/Button';
import { 
  CreditCard, 
  Shield, 
  Check, 
  Star, 
  Users, 
  Video, 
  Target,
  Zap,
  Crown,
  Apple,
  CreditCard as StripeIcon
} from 'lucide-react';

const MembershipPlans = ({ onSelectPlan }) => {
  const [selectedPlan, setSelectedPlan] = useState('plus');
  const [paymentMethod, setPaymentMethod] = useState('stripe');

  const plans = [
    {
      id: 'basic',
      name: 'Basic',
      price: '$9.99',
      period: 'per month',
      description: 'Essential wellness content',
      features: [
        'Access to all programs',
        'Progress tracking',
        'Basic challenges',
        'Community support',
        'Mobile app access'
      ],
      color: 'border-gray-300',
      buttonColor: 'bg-gray-600 hover:bg-gray-700',
      popular: false,
      icon: Target
    },
    {
      id: 'plus',
      name: 'Plus',
      price: '$19.99',
      period: 'per month',
      description: 'Everything in Basic plus group coaching',
      features: [
        'Everything in Basic',
        'Group coaching sessions',
        'Advanced challenges',
        'Wellness analytics',
        'Device integrations',
        'Custom programs'
      ],
      color: 'border-green-500',
      buttonColor: 'bg-green-600 hover:bg-green-700',
      popular: true,
      icon: Users
    },
    {
      id: 'premium',
      name: 'Premium',
      price: '$39.99',
      period: 'per month',
      description: 'Complete wellness solution',
      features: [
        'Everything in Plus',
        '1-on-1 coaching sessions',
        'Custom wellness plans',
        'Priority support',
        'Device bundle included',
        'Advanced analytics',
        'Team challenges'
      ],
      color: 'border-purple-500',
      buttonColor: 'bg-purple-600 hover:bg-purple-700',
      popular: false,
      icon: Crown
    }
  ];

  const paymentMethods = [
    { id: 'stripe', name: 'Credit Card', icon: StripeIcon },
    { id: 'apple', name: 'Apple Pay', icon: Apple },
    { id: 'google', name: 'Google Pay', icon: Shield }
  ];

  const handleSelectPlan = (planId) => {
    setSelectedPlan(planId);
  };

  const handlePayment = () => {
    const plan = plans.find(p => p.id === selectedPlan);
    console.log('Processing payment for:', plan.name, 'with', paymentMethod);
    onSelectPlan(plan);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-50 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Choose Your Wellness Plan
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Select the perfect plan for your wellness journey. All plans include our core features with increasing levels of personalization and support.
          </p>
        </div>

        {/* Plans Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          {plans.map((plan) => {
            const Icon = plan.icon;
            return (
              <motion.div
                key={plan.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                whileHover={{ scale: 1.02 }}
                className={`relative bg-white rounded-2xl shadow-lg p-8 cursor-pointer transition-all border-2 ${
                  selectedPlan === plan.id ? plan.color : 'border-gray-200'
                } ${plan.popular ? 'ring-2 ring-green-500 ring-offset-2' : ''}`}
                onClick={() => handleSelectPlan(plan.id)}
              >
                {plan.popular && (
                  <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                    <div className="bg-green-500 text-white px-4 py-1 rounded-full text-sm font-medium flex items-center space-x-1">
                      <Star className="w-4 h-4" />
                      <span>Most Popular</span>
                    </div>
                  </div>
                )}

                <div className="text-center mb-6">
                  <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Icon className="w-8 h-8 text-gray-600" />
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                  <p className="text-gray-600 mb-4">{plan.description}</p>
                  <div className="mb-6">
                    <span className="text-4xl font-bold text-gray-900">{plan.price}</span>
                    <span className="text-gray-500 ml-2">{plan.period}</span>
                  </div>
                </div>

                <div className="space-y-3 mb-8">
                  {plan.features.map((feature, index) => (
                    <div key={index} className="flex items-center space-x-3">
                      <Check className="w-5 h-5 text-green-500 flex-shrink-0" />
                      <span className="text-gray-700">{feature}</span>
                    </div>
                  ))}
                </div>

                <div className="text-center">
                  <div className={`w-6 h-6 rounded-full border-2 mx-auto ${
                    selectedPlan === plan.id 
                      ? 'bg-green-500 border-green-500' 
                      : 'border-gray-300'
                  }`}>
                    {selectedPlan === plan.id && (
                      <Check className="w-4 h-4 text-white ml-0.5 mt-0.5" />
                    )}
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>

        {/* Payment Section */}
        <div className="bg-white rounded-2xl shadow-lg p-8 max-w-md mx-auto">
          <h3 className="text-xl font-semibold text-gray-900 mb-6 text-center">
            Choose Payment Method
          </h3>

          <div className="space-y-3 mb-6">
            {paymentMethods.map((method) => {
              const Icon = method.icon;
              return (
                <button
                  key={method.id}
                  onClick={() => setPaymentMethod(method.id)}
                  className={`w-full flex items-center space-x-3 p-4 rounded-lg border-2 transition-colors ${
                    paymentMethod === method.id
                      ? 'border-green-500 bg-green-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <Icon className="w-6 h-6 text-gray-600" />
                  <span className="font-medium text-gray-900">{method.name}</span>
                  {paymentMethod === method.id && (
                    <div className="ml-auto">
                      <Check className="w-5 h-5 text-green-500" />
                    </div>
                  )}
                </button>
              );
            })}
          </div>

          <div className="mb-6">
            <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
              <span>Subtotal</span>
              <span>{plans.find(p => p.id === selectedPlan)?.price}</span>
            </div>
            <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
              <span>Tax</span>
              <span>$0.00</span>
            </div>
            <div className="border-t pt-2">
              <div className="flex items-center justify-between font-semibold text-gray-900">
                <span>Total</span>
                <span>{plans.find(p => p.id === selectedPlan)?.price}</span>
              </div>
            </div>
          </div>

          <Button
            fullWidth
            onClick={handlePayment}
            icon={CreditCard}
            iconPosition="left"
            className="text-lg py-4"
          >
            Start Your Plan
          </Button>

          <p className="text-xs text-gray-500 text-center mt-4">
            By continuing, you agree to our Terms of Service and Privacy Policy. Cancel anytime.
          </p>
        </div>
      </div>
    </div>
  );
};

export default MembershipPlans;