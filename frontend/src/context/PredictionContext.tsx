import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState
} from 'react';
import type { PredictionResponse } from '../types';
import { predictBoneAge } from '../api';
import { persistLastInvestigation } from '../lib/lastInvestigation';

type PredictionContextValue = {
  patientId: string;
  setPatientId: (v: string) => void;
  file: File | null;
  previewUrl: string | null;
  result: PredictionResponse | null;
  error: string | null;
  loading: boolean;
  isDragging: boolean;
  setIsDragging: (v: boolean) => void;
  setError: (v: string | null) => void;
  handleFileChange: (f: File | null) => void;
  onFileDrop: (e: React.DragEvent<HTMLLabelElement>) => void;
  runPrediction: () => Promise<boolean>;
  resetSession: () => void;
};

const PredictionContext = createContext<PredictionContextValue | null>(null);

export function PredictionProvider({ children }: { children: React.ReactNode }) {
  const [patientId, setPatientId] = useState('');
  const [file, setFileState] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);

  useEffect(() => {
    if (!file) {
      setPreviewUrl((prev) => {
        if (prev) URL.revokeObjectURL(prev);
        return null;
      });
      return;
    }
    const url = URL.createObjectURL(file);
    setPreviewUrl((prev) => {
      if (prev) URL.revokeObjectURL(prev);
      return url;
    });
    return () => {
      URL.revokeObjectURL(url);
    };
  }, [file]);

  const handleFileChange = useCallback((f: File | null) => {
    if (!f) {
      setFileState(null);
      setResult(null);
      return;
    }
    if (!f.type.startsWith('image/')) {
      setError('Please upload a valid image file (X-ray).');
      return;
    }
    setError(null);
    setFileState(f);
    setResult(null);
  }, []);

  const onFileDrop = useCallback(
    (e: React.DragEvent<HTMLLabelElement>) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(false);
      const files = e.dataTransfer.files;
      if (files?.[0]) handleFileChange(files[0]);
    },
    [handleFileChange]
  );

  const runPrediction = useCallback(async (): Promise<boolean> => {
    if (!patientId.trim() || !file) {
      setError('Patient ID and radiograph are required.');
      return false;
    }
    setError(null);
    setLoading(true);
    try {
      const data = await predictBoneAge(patientId, file);
      setResult(data);
      persistLastInvestigation(patientId.trim(), data);
      return true;
    } catch (err: unknown) {
      const message =
        err instanceof Error ? err.message : 'Unexpected error. Please try again.';
      setError(message);
      return false;
    } finally {
      setLoading(false);
    }
  }, [patientId, file]);

  const resetSession = useCallback(() => {
    setPatientId('');
    setFileState(null);
    setResult(null);
    setError(null);
    setLoading(false);
  }, []);

  const value = useMemo(
    () => ({
      patientId,
      setPatientId,
      file,
      previewUrl,
      result,
      error,
      loading,
      isDragging,
      setIsDragging,
      setError,
      handleFileChange,
      onFileDrop,
      runPrediction,
      resetSession
    }),
    [
      patientId,
      file,
      previewUrl,
      result,
      error,
      loading,
      isDragging,
      handleFileChange,
      onFileDrop,
      runPrediction,
      resetSession
    ]
  );

  return (
    <PredictionContext.Provider value={value}>{children}</PredictionContext.Provider>
  );
}

export function usePrediction() {
  const ctx = useContext(PredictionContext);
  if (!ctx) throw new Error('usePrediction must be used within PredictionProvider');
  return ctx;
}
