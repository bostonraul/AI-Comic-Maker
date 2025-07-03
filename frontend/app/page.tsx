'use client';

import { useState } from 'react';
import { Wand2, Download, FileText, Loader2 } from 'lucide-react';
import axios from 'axios';

const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';

interface ComicRequest {
  genre: string;
  setting: string;
  characters: string;
  characterNames: string;
  dialogues?: string[];
}

interface PanelPrompt {
  description: string;
  dialogue: string;
}

interface ComicResponse {
  success: boolean;
  message: string;
  zip_url?: string;
  pdf_url?: string;
  error?: string;
  prompts?: PanelPrompt[];
}

export default function Home() {
  const [formData, setFormData] = useState<ComicRequest>({
    genre: '',
    setting: '',
    characters: '',
    characterNames: '',
    dialogues: Array(2).fill(''), // For dev, 2 panels
  });
  
  const [prompts, setPrompts] = useState<PanelPrompt[]>([]);
  const [isGeneratingPrompts, setIsGeneratingPrompts] = useState(false);
  const [isGeneratingComic, setIsGeneratingComic] = useState(false);
  const [comicResult, setComicResult] = useState<ComicResponse | null>(null);
  const [error, setError] = useState<string>('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const generatePrompts = async () => {
    if (!formData.genre || !formData.setting || !formData.characters) {
      setError('Please fill in all fields');
      return;
    }

    setIsGeneratingPrompts(true);
    setError('');
    setComicResult(null);

    try {
      const response = await axios.post(`${apiUrl}/generate-prompts`, formData);
      const data: ComicResponse = response.data;
      
      if (data.success && data.prompts) {
        setPrompts(data.prompts);
        setComicResult(data);
      } else {
        setError(data.error || 'Failed to generate prompts');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate prompts');
    } finally {
      setIsGeneratingPrompts(false);
    }
  };

  const generateComic = async () => {
    if (prompts.length === 0) {
      setError('Please generate prompts first');
      return;
    }

    setIsGeneratingComic(true);
    setError('');

    try {
      const response = await axios.post(`${apiUrl}/generate-comic`, { prompts }, { timeout: 600000 });
      const data: ComicResponse = response.data;
      
      if (data.success) {
        setComicResult(data);
      } else {
        setError(data.error || 'Failed to generate comic');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate comic');
    } finally {
      setIsGeneratingComic(false);
    }
  };

  const downloadFile = async (url: string, filename: string) => {
    try {
      const response = await axios.get(`${apiUrl}${url}`, { responseType: 'blob' });
      const blob = new Blob([response.data]);
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(downloadUrl);
    } catch (err) {
      setError('Failed to download file');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            AI Comic Factory
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Create your own AI-generated comic with genre, setting, and characters. 
            Get 10 unique illustration prompts and generate a complete comic!
          </p>
        </div>

        {/* Main Form */}
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
            <h2 className="text-2xl font-semibold mb-6 text-gray-800">
              Comic Creation Form
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Genre
                </label>
                <input
                  type="text"
                  name="genre"
                  value={formData.genre}
                  onChange={handleInputChange}
                  placeholder="e.g., Sci-Fi, Fantasy, Mystery"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Setting
                </label>
                <input
                  type="text"
                  name="setting"
                  value={formData.setting}
                  onChange={handleInputChange}
                  placeholder="e.g., Space Station, Medieval Castle"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Characters
                </label>
                <input
                  type="text"
                  name="characters"
                  value={formData.characters}
                  onChange={handleInputChange}
                  placeholder="e.g., Robot detective, Wizard apprentice"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Character Names
                </label>
                <input
                  type="text"
                  name="characterNames"
                  value={formData.characterNames}
                  onChange={handleInputChange}
                  placeholder="e.g., Roy, Alice, Bob"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            {/* Optional: Dialogue fields for each panel */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Dialogue for each panel (optional)
              </label>
              {formData.dialogues?.map((dialogue, idx) => (
                <input
                  key={idx}
                  type="text"
                  name={`dialogue_${idx}`}
                  value={dialogue}
                  onChange={e => {
                    const newDialogues = [...(formData.dialogues || [])];
                    newDialogues[idx] = e.target.value;
                    setFormData(prev => ({ ...prev, dialogues: newDialogues }));
                  }}
                  placeholder={`Panel ${idx + 1} dialogue`}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md mb-2"
                />
              ))}
            </div>

            <button
              onClick={generatePrompts}
              disabled={isGeneratingPrompts}
              className="w-full bg-blue-600 text-white py-3 px-6 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {isGeneratingPrompts ? (
                <>
                  <Loader2 className="animate-spin" size={20} />
                  Generating Prompts...
                </>
              ) : (
                <>
                  <Wand2 size={20} />
                  Generate 10 Illustration Prompts
                </>
              )}
            </button>
          </div>

          {/* Error Display */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
              <p className="text-red-800">{error}</p>
            </div>
          )}

          {/* Generated Prompts */}
          {prompts.length > 0 && (
            <div className="bg-gray-50 border border-gray-200 rounded-md p-4 mb-6">
              <h3 className="text-lg font-semibold mb-2">Generated Prompts</h3>
              <ol className="list-decimal pl-6">
                {prompts.map((prompt, index) => (
                  <li key={index} className="mb-2">
                    <div className="font-medium text-gray-800">{prompt.description}</div>
                    <div className="text-blue-700 italic">{prompt.dialogue}</div>
                  </li>
                ))}
              </ol>
            </div>
          )}

          <button
            onClick={generateComic}
            disabled={isGeneratingComic}
            className="w-full bg-green-600 text-white py-3 px-6 rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {isGeneratingComic ? (
              <>
                <Loader2 className="animate-spin" size={20} />
                Generating Comic...
              </>
            ) : (
              <>
                <FileText size={20} />
                Generate Comic (ZIP + PDF)
              </>
            )}
          </button>
        </div>

        {/* Results */}
        {comicResult && comicResult.success && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-semibold mb-4 text-gray-800">
              Comic Generated Successfully!
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {comicResult.zip_url && (
                <button
                  onClick={() => downloadFile(comicResult.zip_url!, 'comic.zip')}
                  className="bg-blue-600 text-white py-3 px-6 rounded-md hover:bg-blue-700 flex items-center justify-center gap-2"
                >
                  <Download size={20} />
                  Download ZIP (Images + PDF)
                </button>
              )}
              
              {comicResult.pdf_url && (
                <button
                  onClick={() => downloadFile(comicResult.pdf_url!, 'comic.pdf')}
                  className="bg-green-600 text-white py-3 px-6 rounded-md hover:bg-green-700 flex items-center justify-center gap-2"
                >
                  <FileText size={20} />
                  Download PDF Only
                </button>
              )}
            </div>
            
            <p className="text-gray-600 mt-4 text-center">
              Your comic includes 10 AI-generated images with captions, assembled into a beautiful PDF!
            </p>
          </div>
        )}
      </div>
    </div>
  );
} 