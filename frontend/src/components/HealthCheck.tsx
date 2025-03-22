import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../lib/api-client';

export function HealthCheck() {
  // Only show in development mode
  if (import.meta.env.PROD) {
    return null;
  }

  const { data, isLoading, error } = useQuery({
    queryKey: ['health'],
    queryFn: apiClient.checkHealth,
  });

  if (isLoading) return <div>Checking API health...</div>;
  if (error) return <div className="text-red-500">Error: {error.message}</div>;
  
  return (
    <div className="p-4 border rounded-lg bg-background/50 backdrop-blur-sm">
      <h2 className="text-lg font-semibold mb-2">API Health Status</h2>
      <p className="text-green-600">Status: {data?.status}</p>
      <p className="text-sm text-muted-foreground mt-2">Development Mode Only</p>
    </div>
  );
} 