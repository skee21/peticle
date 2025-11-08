'use client';
import { useDropzone } from 'react-dropzone';
import { useState } from 'react';
import { Upload, Video, Loader } from 'lucide-react';
import { videoAPI } from '@/lib/api';

export default function VideoUploader({ petId, onUploadComplete }) {
  const [preview, setPreview] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const { getRootProps, getInputProps } = useDropzone({
    accept: { 'video/*': ['.mp4', '.mov', '.avi'] },
    maxFiles: 1,
    onDrop: async (files) => {
      const file = files[0];
      setPreview(URL.createObjectURL(file));
      setUploading(true);
      setError(null);
      
      try {
        const result = await videoAPI.upload(petId, file);
        onUploadComplete?.(result);
      } catch (err) {
        setError(err.message);
      } finally {
        setUploading(false);
      }
    }
  });

  return (
    <div className="space-y-4">
      <div {...getRootProps()} 
           className="border-2 border-dashed rounded-lg p-8 text-center cursor-pointer hover:border-blue-500 transition">
        <input {...getInputProps()} />
        <Video className="mx-auto h-12 w-12 text-gray-400" />
        <p className="mt-2">Drop video or click to upload</p>
        <p className="text-sm text-gray-500">MP4, MOV, AVI up to 100MB</p>
      </div>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}
      
      {preview && (
        <video controls className="w-full rounded-lg max-h-96" src={preview} />
      )}
      
      {uploading && (
        <div className="flex items-center justify-center gap-2 text-blue-600">
          <Loader className="w-5 h-5 animate-spin" />
          <p>Uploading and analyzing video...</p>
        </div>
      )}
    </div>
  );
}
