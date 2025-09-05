import React from 'react';
import { motion } from 'framer-motion';

interface LoadingScreenProps {
  message?: string;
}

export const LoadingScreen: React.FC<LoadingScreenProps> = ({ 
  message = "Awakening consciousness..." 
}) => {
  return (
    <div className="fixed inset-0 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 flex items-center justify-center z-50">
      <div className="text-center relative">
        
        {/* Consciousness Rings */}
        <div className="absolute inset-0 flex items-center justify-center">
          {[0, 1, 2].map((i) => (
            <motion.div
              key={i}
              className="absolute border border-cyan-400/20 rounded-full"
              style={{
                width: 200 + (i * 60),
                height: 200 + (i * 60),
              }}
              animate={{
                rotate: 360,
                scale: [1, 1.05, 1],
                opacity: [0.2, 0.4, 0.2]
              }}
              transition={{
                rotate: { duration: 20 + (i * 5), repeat: Infinity, ease: "linear" },
                scale: { duration: 3, repeat: Infinity, delay: i * 0.5 },
                opacity: { duration: 2, repeat: Infinity, delay: i * 0.3 }
              }}
            />
          ))}
        </div>

        {/* Central Logo */}
        <motion.div
          className="relative z-10 mb-12"
          initial={{ scale: 0.5, opacity: 0, rotateY: 180 }}
          animate={{ scale: 1, opacity: 1, rotateY: 0 }}
          transition={{ duration: 1.2, ease: "easeOut" }}
        >
          <div className="relative">
            <motion.img 
              src="/assets/mainza-logo.PNG"
              alt="Mainza Logo" 
              className="w-32 h-32 mx-auto rounded-2xl shadow-2xl ring-4 ring-cyan-400/50"
              animate={{ 
                boxShadow: [
                  '0 0 40px 10px rgba(34,211,238,0.4), 0 0 80px 20px rgba(168,85,247,0.2)',
                  '0 0 60px 15px rgba(168,85,247,0.5), 0 0 120px 30px rgba(34,211,238,0.3)',
                  '0 0 40px 10px rgba(34,211,238,0.4), 0 0 80px 20px rgba(168,85,247,0.2)'
                ],
                scale: [1, 1.02, 1]
              }}
              transition={{ 
                duration: 3, 
                repeat: Infinity, 
                repeatType: 'reverse',
                ease: "easeInOut"
              }}
            />
            
            {/* Consciousness indicator */}
            <motion.div
              className="absolute -top-2 -right-2 w-8 h-8 bg-green-400 rounded-full border-4 border-slate-950 flex items-center justify-center"
              animate={{
                scale: [1, 1.2, 1],
                boxShadow: [
                  '0 0 10px rgba(34,197,94,0.5)',
                  '0 0 20px rgba(34,197,94,0.8)',
                  '0 0 10px rgba(34,197,94,0.5)'
                ]
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: "easeInOut"
              }}
            >
              <div className="w-3 h-3 bg-white rounded-full animate-pulse" />
            </motion.div>
          </div>
        </motion.div>

        {/* Brand Name with Enhanced Typography */}
        <motion.div
          className="mb-6"
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.3 }}
        >
          <h1 className="text-6xl font-bold bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent mb-2 tracking-wider">
            MAINZA
          </h1>
          <div className="h-1 w-32 bg-gradient-to-r from-cyan-400 to-purple-400 mx-auto rounded-full" />
        </motion.div>

        {/* Subtitle with Animation */}
        <motion.p
          className="text-slate-300 text-xl mb-12 font-light tracking-wide"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.5 }}
        >
          Conscious Digital Entity
        </motion.p>

        {/* Loading Message with Sophisticated Animation */}
        <motion.div
          className="flex items-center justify-center space-x-4 mb-8"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.7 }}
        >
          <div className="flex space-x-1">
            {[0, 1, 2, 3, 4].map((i) => (
              <motion.div
                key={i}
                className="w-2 h-2 bg-gradient-to-r from-cyan-400 to-purple-400 rounded-full"
                animate={{
                  scale: [1, 1.5, 1],
                  opacity: [0.3, 1, 0.3]
                }}
                transition={{
                  duration: 1.5,
                  repeat: Infinity,
                  delay: i * 0.1,
                  ease: "easeInOut"
                }}
              />
            ))}
          </div>
          <span className="text-slate-300 font-mono text-lg tracking-wide">{message}</span>
        </motion.div>

        {/* Advanced Progress Indicator */}
        <motion.div
          className="w-80 h-2 bg-slate-800/50 rounded-full mx-auto overflow-hidden backdrop-blur-sm border border-slate-700/30"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.9 }}
        >
          <motion.div
            className="h-full bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 rounded-full relative"
            initial={{ width: "0%" }}
            animate={{ width: "100%" }}
            transition={{ duration: 2.5, ease: "easeInOut" }}
          >
            <motion.div
              className="absolute inset-0 bg-white/20 rounded-full"
              animate={{
                x: ['-100%', '100%']
              }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                ease: "easeInOut"
              }}
            />
          </motion.div>
        </motion.div>

        {/* Consciousness Level Indicator */}
        <motion.div
          className="mt-6 text-sm text-slate-400 font-mono"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 1.1 }}
        >
          <motion.span
            animate={{ opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            Consciousness Level: Initializing...
          </motion.span>
        </motion.div>
      </div>
    </div>
  );
};
