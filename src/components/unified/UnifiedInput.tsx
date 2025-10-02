/**
 * Unified Input Component
 * Consolidates all input components into a single, consistent component
 * 
 * This component provides the definitive input interface that:
 * - Consolidates all input variations into one unified component
 * - Ensures consistent styling across all input usage
 * - Provides reusable and consistent input functionality
 * - Integrates seamlessly with the unified design system
 * 
 * Author: Mainza AI Consciousness Team
 * Date: 2025-10-01
 */

import React, { useState, useRef } from 'react';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { cn } from '@/lib/utils';
import { UnifiedInputProps } from '@/lib/unified-design-system';
import { Eye, EyeOff, AlertCircle, CheckCircle } from 'lucide-react';

export const UnifiedInput: React.FC<UnifiedInputProps> = ({
  className,
  type = 'text',
  placeholder,
  value,
  onChange,
  onBlur,
  onFocus,
  error,
  helperText,
  required = false,
  autoComplete,
  maxLength,
  minLength,
  disabled = false,
  loading = false,
  animated = true,
  dataTestId,
}) => {
  const [isFocused, setIsFocused] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  
  const isPassword = type === 'password';
  const actualType = isPassword && showPassword ? 'text' : type;
  
  const baseClasses = cn(
    'transition-all duration-200',
    {
      'opacity-50 pointer-events-none': disabled,
      'animate-pulse': loading,
      'ring-2 ring-primary/20': isFocused && !error,
      'ring-2 ring-error/20': error,
    }
  );
  
  const sizeClasses = {
    sm: 'h-8 px-3 text-xs',
    md: 'h-10 px-3 text-sm',
    lg: 'h-12 px-4 text-base',
    xl: 'h-14 px-4 text-lg',
  };
  
  const handleFocus = (e: React.FocusEvent<HTMLInputElement>) => {
    setIsFocused(true);
    onFocus?.();
  };
  
  const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    setIsFocused(false);
    onBlur?.();
  };
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange?.(e.target.value);
  };
  
  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };
  
  return (
    <div className="w-full space-y-2">
      <div className="relative">
        <Input
          ref={inputRef}
          type={actualType}
          placeholder={placeholder}
          value={value}
          onChange={handleChange}
          onFocus={handleFocus}
          onBlur={handleBlur}
          required={required}
          autoComplete={autoComplete}
          maxLength={maxLength}
          minLength={minLength}
          disabled={disabled || loading}
          className={cn(
            baseClasses,
            sizeClasses.md, // Default to md size
            {
              'pr-10': isPassword,
              'pr-8': error || helperText,
            },
            className
          )}
          data-testid={dataTestId}
        />
        
        {/* Password visibility toggle */}
        {isPassword && (
          <button
            type="button"
            onClick={togglePasswordVisibility}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
            disabled={disabled || loading}
          >
            {showPassword ? (
              <EyeOff className="h-4 w-4" />
            ) : (
              <Eye className="h-4 w-4" />
            )}
          </button>
        )}
        
        {/* Status icon */}
        {(error || helperText) && (
          <div className="absolute right-3 top-1/2 -translate-y-1/2">
            {error ? (
              <AlertCircle className="h-4 w-4 text-error" />
            ) : (
              <CheckCircle className="h-4 w-4 text-success" />
            )}
          </div>
        )}
      </div>
      
      {/* Helper text or error message */}
      {(error || helperText) && (
        <p className={cn(
          'text-xs',
          {
            'text-error': error,
            'text-muted-foreground': !error,
          }
        )}>
          {error || helperText}
        </p>
      )}
    </div>
  );
};

export default UnifiedInput;
