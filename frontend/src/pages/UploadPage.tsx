import React from 'react';
import { useNavigate } from 'react-router-dom';
import { usePrediction } from '../context/PredictionContext';
import { IconChart, IconUpload, TileHeader } from '../icons';

export function UploadPage() {
  const navigate = useNavigate();
  const {
    patientId,
    setPatientId,
    file,
    error,
    isDragging,
    setIsDragging,
    setError,
    handleFileChange,
    onFileDrop
  } = usePrediction();

  const onContinue = (e: React.FormEvent) => {
    e.preventDefault();
    if (!patientId.trim()) {
      setError('Patient ID is required.');
      return;
    }
    if (!file) {
      setError('Please upload a radiograph first.');
      return;
    }
    setError(null);
    navigate('/preview');
  };

  return (
    <section aria-labelledby="upload-heading" className="mx-auto max-w-xl">
      <h1 id="upload-heading" className="sr-only">
        Upload radiograph — BoneAgeX
      </h1>
      <div className="glass-card p-5 sm:p-6">
        <div className="glass-card-inner">
          <TileHeader
            step={1}
            title="Upload"
            desc="Patient ID and PA hand–wrist radiograph (PNG or JPEG)."
            icon={IconUpload}
          />

          <form onSubmit={onContinue} className="space-y-4">
            <div className="space-y-1.5">
              <label htmlFor="patientId" className="stat-label">
                Patient ID
              </label>
              <input
                id="patientId"
                className="input-base"
                placeholder="e.g. P-2026-001"
                value={patientId}
                onChange={(e) => setPatientId(e.target.value)}
                autoComplete="off"
              />
            </div>

            <div className="space-y-1.5">
              <p className="stat-label">Radiograph</p>
              <label
                htmlFor="fileInput"
                className={`dropzone ${isDragging ? '!border-primary-400 !bg-primary-50' : ''}`}
                onDragOver={(e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  setIsDragging(true);
                }}
                onDragLeave={(e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  setIsDragging(false);
                }}
                onDrop={onFileDrop}
              >
                <input
                  id="fileInput"
                  type="file"
                  accept="image/*"
                  className="hidden"
                  onChange={(e) => handleFileChange(e.target.files?.[0] ?? null)}
                />
                <IconUpload className="mb-2 h-8 w-8 text-primary-500/70" />
                <p className="font-medium text-slate-700">Drop file or click to browse</p>
                <p className="mt-1 text-xs text-slate-500">High-contrast PA view recommended</p>
                {file && (
                  <div className="mt-4 flex w-full items-center justify-between gap-2 border-t border-slate-200 pt-3 text-xs text-slate-600">
                    <span className="truncate font-medium text-slate-800">{file.name}</span>
                    <span className="shrink-0 tabular-nums text-slate-500">
                      {(file.size / 1024 / 1024).toFixed(2)} MB
                    </span>
                  </div>
                )}
              </label>
            </div>

            <button type="submit" className="btn-primary w-full">
              <IconChart className="h-4 w-4 opacity-95" />
              Continue to preview
            </button>
          </form>

          {error && (
            <div
              className="mt-4 rounded-xl border border-red-200 bg-red-50 px-3 py-2.5 text-xs text-red-900"
              role="alert"
            >
              <span className="font-semibold text-red-800">Error — </span>
              {error}
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
