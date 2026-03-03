import { useState, useRef, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { CheckCircle, XCircle, Loader2, ShieldCheck, RefreshCw } from 'lucide-react';
import apiClient from '../../services/apiClient';
import { ENDPOINTS } from '../../config/constants';

type VerifyState = 'input' | 'verifying' | 'success' | 'error';

export function VerifyEmailPage() {
  const [searchParams] = useSearchParams();
  const emailFromUrl = searchParams.get('email') || '';

  const [email, setEmail] = useState(emailFromUrl);
  const [digits, setDigits] = useState<string[]>(['', '', '', '', '', '']);
  const [state, setState] = useState<VerifyState>('input');
  const [errorMessage, setErrorMessage] = useState('');
  const [resending, setResending] = useState(false);
  const [resendCooldown, setResendCooldown] = useState(0);

  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

  // Auto-focus first input on mount
  useEffect(() => {
    if (state === 'input') {
      inputRefs.current[0]?.focus();
    }
  }, [state]);

  // Resend cooldown countdown
  useEffect(() => {
    if (resendCooldown <= 0) return;
    const timer = setTimeout(() => setResendCooldown((c) => c - 1), 1000);
    return () => clearTimeout(timer);
  }, [resendCooldown]);

  const handleDigitChange = (index: number, value: string) => {
    // Only allow digits
    const digit = value.replace(/\D/g, '').slice(-1);
    const newDigits = [...digits];
    newDigits[index] = digit;
    setDigits(newDigits);

    // Auto-advance to next input
    if (digit && index < 5) {
      inputRefs.current[index + 1]?.focus();
    }

    // Auto-submit when all 6 digits are filled
    if (digit && index === 5 && newDigits.every((d) => d !== '')) {
      handleVerify(newDigits.join(''));
    }
  };

  const handleKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Backspace' && !digits[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
    if (e.key === 'Enter') {
      const code = digits.join('');
      if (code.length === 6) handleVerify(code);
    }
  };

  const handlePaste = (e: React.ClipboardEvent) => {
    e.preventDefault();
    const pasted = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, 6);
    if (!pasted) return;
    const newDigits = [...digits];
    for (let i = 0; i < 6; i++) {
      newDigits[i] = pasted[i] || '';
    }
    setDigits(newDigits);
    // Focus last filled input or the next empty one
    const focusIndex = Math.min(pasted.length, 5);
    inputRefs.current[focusIndex]?.focus();

    if (pasted.length === 6) {
      handleVerify(pasted);
    }
  };

  const handleVerify = async (code: string) => {
    if (!email) {
      setErrorMessage('Please enter your email address.');
      setState('error');
      return;
    }

    setState('verifying');
    setErrorMessage('');

    try {
      await apiClient.post(ENDPOINTS.AUTH.VERIFY_EMAIL, { email, code });
      setState('success');
    } catch (err: any) {
      setState('error');
      const detail =
        err?.response?.data?.detail ||
        err?.response?.data?.error ||
        'Verification failed. The code may be invalid or expired.';
      setErrorMessage(typeof detail === 'string' ? detail : 'Verification failed');
    }
  };

  const handleResend = async () => {
    if (!email || resending || resendCooldown > 0) return;
    setResending(true);
    setErrorMessage('');
    try {
      await apiClient.post(ENDPOINTS.AUTH.RESEND_VERIFICATION, { email });
      setResendCooldown(60);
      setDigits(['', '', '', '', '', '']);
      setState('input');
      inputRefs.current[0]?.focus();
    } catch (err: any) {
      const detail =
        err?.response?.data?.detail || 'Failed to resend code.';
      setErrorMessage(typeof detail === 'string' ? detail : 'Failed to resend');
    } finally {
      setResending(false);
    }
  };

  const resetToInput = () => {
    setDigits(['', '', '', '', '', '']);
    setErrorMessage('');
    setState('input');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 px-4">
      <div className="max-w-md w-full bg-white rounded-lg shadow-xl p-8">
        {/* ─── Success ─── */}
        {state === 'success' && (
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-6">
              <CheckCircle className="w-8 h-8 text-green-600" />
            </div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">Email Verified!</h1>
            <p className="text-gray-600 mb-6">
              Your email has been successfully verified. You can now log in.
            </p>
            <Link
              to="/login"
              className="inline-block w-full bg-indigo-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-indigo-700 transition-colors text-center"
            >
              Go to Login
            </Link>
          </div>
        )}

        {/* ─── Verifying Spinner ─── */}
        {state === 'verifying' && (
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-indigo-100 rounded-full mb-6">
              <Loader2 className="w-8 h-8 text-indigo-600 animate-spin" />
            </div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">Verifying...</h1>
            <p className="text-gray-600">Checking your verification code.</p>
          </div>
        )}

        {/* ─── Input / Error ─── */}
        {(state === 'input' || state === 'error') && (
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-indigo-100 rounded-full mb-6">
              <ShieldCheck className="w-8 h-8 text-indigo-600" />
            </div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">Verify Your Email</h1>
            <p className="text-gray-600 mb-6">
              Enter the 6-digit code sent to{' '}
              <span className="font-semibold text-indigo-600">{email || 'your email'}</span>
            </p>

            {/* Email input if not provided via URL */}
            {!emailFromUrl && (
              <div className="mb-4">
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-center"
                />
              </div>
            )}

            {/* 6-digit code inputs */}
            <div className="flex justify-center gap-3 mb-6" onPaste={handlePaste}>
              {digits.map((digit, i) => (
                <input
                  key={i}
                  ref={(el) => { inputRefs.current[i] = el; }}
                  type="text"
                  inputMode="numeric"
                  maxLength={1}
                  value={digit}
                  onChange={(e) => handleDigitChange(i, e.target.value)}
                  onKeyDown={(e) => handleKeyDown(i, e)}
                  className={`w-12 h-14 text-center text-2xl font-bold border-2 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors ${
                    state === 'error' ? 'border-red-300 bg-red-50' : 'border-gray-300'
                  }`}
                />
              ))}
            </div>

            {/* Error message */}
            {state === 'error' && errorMessage && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                <div className="flex items-center gap-2 justify-center">
                  <XCircle className="w-4 h-4 text-red-600" />
                  <p className="text-sm text-red-600">{errorMessage}</p>
                </div>
                <button
                  onClick={resetToInput}
                  className="mt-2 text-sm text-indigo-600 hover:text-indigo-800 underline"
                >
                  Try again
                </button>
              </div>
            )}

            {/* Verify button */}
            <button
              onClick={() => handleVerify(digits.join(''))}
              disabled={digits.join('').length !== 6}
              className="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed mb-4"
            >
              Verify Email
            </button>

            {/* Resend */}
            <div className="flex items-center justify-center gap-2 text-sm text-gray-600">
              <span>Didn't receive the code?</span>
              <button
                onClick={handleResend}
                disabled={resending || resendCooldown > 0}
                className="inline-flex items-center gap-1 text-indigo-600 hover:text-indigo-800 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${resending ? 'animate-spin' : ''}`} />
                {resendCooldown > 0 ? `Resend in ${resendCooldown}s` : 'Resend Code'}
              </button>
            </div>

            <p className="mt-4 text-xs text-gray-400">Code expires in 5 minutes</p>

            <div className="mt-6 pt-4 border-t text-sm text-gray-500">
              <Link to="/login" className="text-indigo-600 hover:text-indigo-800 font-medium">
                Back to Login
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
