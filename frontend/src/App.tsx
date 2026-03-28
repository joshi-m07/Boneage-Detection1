import React from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import { PredictionProvider } from './context/PredictionContext';
import { AppShell } from './components/AppShell';
import { HomePage } from './pages/HomePage';
import { UploadPage } from './pages/UploadPage';
import { PreviewPage } from './pages/PreviewPage';
import { ResultsPage } from './pages/ResultsPage';
import { LastInvestigationPage } from './pages/LastInvestigationPage';

export default function App() {
  return (
    <PredictionProvider>
      <Routes>
        <Route element={<AppShell />}>
          <Route index element={<HomePage />} />
          <Route path="upload" element={<UploadPage />} />
          <Route path="preview" element={<PreviewPage />} />
          <Route path="results" element={<ResultsPage />} />
          <Route path="last" element={<LastInvestigationPage />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </PredictionProvider>
  );
}
