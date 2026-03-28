import React from 'react';

export function IconUpload(props: { className?: string }) {
  return (
    <svg className={props.className} viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M12 16V8m0 0-3 3m3-3 3 3M4 16.8V19a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2.2"
        stroke="currentColor"
        strokeWidth="1.75"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function IconImage(props: { className?: string }) {
  return (
    <svg className={props.className} viewBox="0 0 24 24" fill="none" aria-hidden>
      <rect x="3" y="5" width="18" height="14" rx="2" stroke="currentColor" strokeWidth="1.75" />
      <circle cx="8.5" cy="10" r="1.5" fill="currentColor" />
      <path
        d="m21 15-5.5-5.5L8 17"
        stroke="currentColor"
        strokeWidth="1.75"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function IconChart(props: { className?: string }) {
  return (
    <svg className={props.className} viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M4 19V5M4 19h16M8 15v-4m4 4V9m4 6v-2"
        stroke="currentColor"
        strokeWidth="1.75"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function Spinner({ className }: { className?: string }) {
  return (
    <span
      className={`inline-block h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white ${className ?? ''}`}
      aria-hidden
    />
  );
}

export function TileHeader({
  step,
  title,
  desc,
  icon: Icon,
  className = ''
}: {
  step: number;
  title: string;
  desc: string;
  icon: React.FC<{ className?: string }>;
  className?: string;
}) {
  return (
    <div className={`mb-4 flex gap-3 ${className}`}>
      <span className="step-pill mt-0.5">{step}</span>
      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2">
          <Icon className="h-4 w-4 shrink-0 text-primary-600" />
          <h2 className="tile-title">{title}</h2>
        </div>
        <p className="tile-desc mt-1">{desc}</p>
      </div>
    </div>
  );
}
