'use client';
import { useState } from 'react';
import VideoUploader from '@/components/VideoUploader';
import { AlertCircle, CheckCircle, Loader, Video } from 'lucide-react';

export default function AnalysisPage() {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);

  const handleVideoUpload = async (file) => {
    setAnalyzing(true);
    
    // Simulate AI analysis
    setTimeout(() => {
      setAnalysisResult({
        status: 'completed',
        insights: [
          { type: 'positive', text: 'Normal activity levels detected' },
          { type: 'warning', text: 'Slight limping on left paw - monitor closely' },
          { type: 'positive', text: 'Good appetite and energy' },
        ],
        confidence: 87,
        recommendations: [
          'Schedule a vet checkup for the limping issue',
          'Continue current diet and exercise routine',
          'Monitor behavior over the next 3-5 days'
        ]
      });
      setAnalyzing(false);
    }, 3000);
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4">AI Video Analysis</h1>
        <p className="text-lg text-gray-600">
          Upload a video of your pet to detect behavior patterns and potential health issues
        </p>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-8">
        <VideoUploader onUpload={handleVideoUpload} />

        {analyzing && (
          <div className="mt-8 text-center py-12">
            <Loader className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-2">Analyzing Video...</h3>
            <p className="text-gray-600">
              Our AI is examining your pet's behavior and movements
            </p>
          </div>
        )}

        {analysisResult && !analyzing && (
          <div className="mt-8 space-y-6">
            <div className="border-t pt-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold">Analysis Complete</h2>
                <div className="bg-green-100 text-green-800 px-4 py-2 rounded-full font-semibold">
                  {analysisResult.confidence}% Confidence
                </div>
              </div>

              {/* Insights */}
              <div className="mb-6">
                <h3 className="text-lg font-semibold mb-4">Key Insights</h3>
                <div className="space-y-3">
                  {analysisResult.insights.map((insight, idx) => (
                    <div 
                      key={idx}
                      className={`flex items-start gap-3 p-4 rounded-lg ${
                        insight.type === 'positive' 
                          ? 'bg-green-50 border border-green-200' 
                          : 'bg-yellow-50 border border-yellow-200'
                      }`}
                    >
                      {insight.type === 'positive' ? (
                        <CheckCircle className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                      ) : (
                        <AlertCircle className="w-5 h-5 text-yellow-600 mt-0.5 flex-shrink-0" />
                      )}
                      <span className={
                        insight.type === 'positive' ? 'text-green-800' : 'text-yellow-800'
                      }>
                        {insight.text}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommendations */}
              <div>
                <h3 className="text-lg font-semibold mb-4">Recommendations</h3>
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                  <ul className="space-y-3">
                    {analysisResult.recommendations.map((rec, idx) => (
                      <li key={idx} className="flex items-start gap-3">
                        <span className="bg-blue-600 text-white w-6 h-6 rounded-full flex items-center justify-center text-sm font-semibold flex-shrink-0">
                          {idx + 1}
                        </span>
                        <span className="text-blue-900">{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <button className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition mt-6">
                Save to Pet Profile
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
