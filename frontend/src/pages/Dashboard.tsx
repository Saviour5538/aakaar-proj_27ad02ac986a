import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getDocuments } from '../api/client';
import { toast } from 'react-toastify';

interface Document {
  id: string;
  name: string;
  created_at: string;
}

const Dashboard: React.FC = () => {
  const [documentCount, setDocumentCount] = useState<number>(0);
  const [recentDocuments, setRecentDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDashboardData = async () => {
      setLoading(true);
      setError(null);
      try {
        const documents = await getDocuments();
        setDocumentCount(documents.length);
        setRecentDocuments(documents.slice(0, 5));
      } catch (err: any) {
        setError('Failed to fetch dashboard data.');
        toast.error('Failed to fetch dashboard data.');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const handleQuickAction = (action: string) => {
    if (action === 'upload') {
      navigate('/upload');
    } else if (action === 'query') {
      navigate('/query');
    }
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      {loading && <p className="text-gray-600">Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}
      {!loading && !error && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div className="bg-white shadow rounded-lg p-4">
              <h2 className="text-lg font-semibold">Total Documents</h2>
              <p className="text-2xl font-bold">{documentCount}</p>
            </div>
            <div className="bg-white shadow rounded-lg p-4">
              <h2 className="text-lg font-semibold">Recent Documents</h2>
              <p className="text-2xl font-bold">{recentDocuments.length}</p>
            </div>
            <div className="bg-white shadow rounded-lg p-4">
              <h2 className="text-lg font-semibold">Quick Actions</h2>
              <div className="flex space-x-4 mt-2">
                <button
                  onClick={() => handleQuickAction('upload')}
                  className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                >
                  Upload
                </button>
                <button
                  onClick={() => handleQuickAction('query')}
                  className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
                >
                  Query
                </button>
              </div>
            </div>
          </div>
          <div className="bg-white shadow rounded-lg p-4">
            <h2 className="text-lg font-semibold mb-4">Recent Documents</h2>
            {recentDocuments.length > 0 ? (
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr>
                    <th className="border-b p-2">Name</th>
                    <th className="border-b p-2">Created At</th>
                  </tr>
                </thead>
                <tbody>
                  {recentDocuments.map((doc) => (
                    <tr key={doc.id}>
                      <td className="border-b p-2">{doc.name}</td>
                      <td className="border-b p-2">{new Date(doc.created_at).toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="text-gray-600">No recent documents available.</p>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;