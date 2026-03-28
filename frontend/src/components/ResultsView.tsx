import React, { useState } from 'react';
import type { PredictionResponse } from '../types';
import { gradcamSrc } from '../api';

function PredictionResultCard(props: {
  label: string;
  side: PredictionResponse['male_prediction'];
  variant: 'male' | 'female';
  cacheKey: string;
}) {
  const { label, side, variant, cacheKey } = props;
  const accent = variant === 'male' ? 'prediction-card-male' : 'prediction-card-female';
  const tint =
    variant === 'male'
      ? 'bg-primary-50 text-primary-800 border-primary-100'
      : 'bg-sky-50 text-sky-900 border-sky-100';
  const [camFailed, setCamFailed] = useState(false);

  if (!side) return null;
  const camUrl = side.gradcam_url ? gradcamSrc(side.gradcam_url, cacheKey) : '';

  return (
    <div className={`model-card ${accent} animate-fade-in-up flex h-full flex-col space-y-3`}>
      <div className="flex flex-wrap items-start justify-between gap-2">
        <div className="flex items-center gap-2">
          <div
            className={`flex h-8 w-8 items-center justify-center rounded-lg border text-xs font-bold ${tint}`}
          >
            {label.charAt(0)}
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-800">{label} model</p>
            <p className="text-xs text-slate-500">Hand–wrist radiograph analysis</p>
          </div>
        </div>
        <span className="badge tabular-nums text-slate-700">σ = {side.uncertainty_sigma.toFixed(3)}</span>
      </div>

      <div className="grid flex-1 grid-cols-1 gap-4 sm:grid-cols-[minmax(0,0.95fr),minmax(0,1.2fr)]">
        <div className="space-y-1">
          <p className="stat-label">Bone age</p>
          <p className="stat-value">{side.age.toFixed(2)}</p>
          <p className="text-xs text-slate-500">years</p>
          <p className="stat-subtext pt-1">Lower σ reflects higher model confidence.</p>
        </div>

        <div className="space-y-1.5">
          <p className="stat-label">Grad-CAM</p>
          <div className="relative flex aspect-video items-center justify-center overflow-hidden rounded-lg border border-slate-200 bg-slate-100">
            {camUrl && !camFailed ? (
              <img
                src={camUrl}
                alt={`${label} model attention map`}
                className="h-full w-full object-contain"
                loading="lazy"
                onError={() => setCamFailed(true)}
              />
            ) : (
              <span className="px-3 text-center text-xs text-slate-500">
                {camFailed
                  ? 'Could not load heatmap. Is the API running on port 8000 with /storage mounted?'
                  : 'Not available'}
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

type ResultsViewProps = {
  result: PredictionResponse;
  /** Shown above the summary cards (e.g. last saved banner) */
  banner?: React.ReactNode;
};

export function ResultsView({ result, banner }: ResultsViewProps) {
  const cacheKey = `${result.timestamp}-${result.prediction_id}`;

  return (
    <div className="space-y-5">
      {banner}
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 sm:gap-4">
        <div className="kv-card animate-fade-in-up">
          <p className="stat-label">Status</p>
          <p className="mt-1 text-sm font-semibold text-emerald-700">
            {result.status === 'success' ? 'Completed' : result.status}
          </p>
          <p className="stat-subtext mt-1.5">{result.message}</p>
        </div>
        <div className="kv-card animate-fade-in-up">
          <p className="stat-label">Record</p>
          <p className="mt-1 font-mono text-sm font-semibold tabular-nums text-slate-800">
            #{result.prediction_id}
          </p>
          <p className="mt-0.5 truncate text-sm text-slate-700" title={result.patient_id}>
            Patient: {result.patient_id}
          </p>
          <p className="stat-subtext mt-1.5">{new Date(result.timestamp).toLocaleString()}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 md:items-stretch">
        <PredictionResultCard
          label="Male"
          side={result.male_prediction}
          variant="male"
          cacheKey={cacheKey}
        />
        <PredictionResultCard
          label="Female"
          side={result.female_prediction}
          variant="female"
          cacheKey={cacheKey}
        />
      </div>
    </div>
  );
}
