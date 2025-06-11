import React, { useEffect, useState } from 'react';
import Head from 'next/head';
import { Combobox } from '@headlessui/react';

interface Station {
  id: number;
  station_id: string;
  name: string;
  latitude: number;
  longitude: number;
  total_trips?: number;
  unique_bikes?: number;
}

interface ProbabilityResult {
  probability: number;
  confidence_interval: [number, number];
  explanation: string;
  station_info?: Station;
}

export default function Home() {
  const [stations, setStations] = useState<Station[]>([]);
  const [loadingStations, setLoadingStations] = useState(true);
  const [query, setQuery] = useState('');
  const [form, setForm] = useState({
    home_station_id: '',
    riding_frequency: 5,
    time_pattern: 'weekday',
  });
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<ProbabilityResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchStations() {
      setLoadingStations(true);
      try {
        const res = await fetch('/api/stations');
        let data: Station[] = await res.json();
        // Sort stations alphabetically by name
        data = data.sort((a, b) => a.name.localeCompare(b.name));
        setStations(data);
        setForm(f => ({ ...f, home_station_id: data[0]?.station_id || '' }));
      } catch (e) {
        setError('Failed to load stations');
      } finally {
        setLoadingStations(false);
      }
    }
    fetchStations();
  }, []);

  const filteredStations =
    query === ''
      ? stations
      : stations.filter((station: Station) =>
          station.name.toLowerCase().includes(query.toLowerCase())
        );

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch('/api/probability', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      
      if (!res.ok) {
        // Try to parse error response as JSON, but handle non-JSON responses
        let errorMessage = 'API error';
        try {
          const errorData = await res.json();
          errorMessage = errorData.detail || errorData.message || 'API error';
        } catch (parseError) {
          // If error response is not JSON, get the text
          const errorText = await res.text();
          errorMessage = errorText || `HTTP ${res.status}: ${res.statusText}`;
        }
        throw new Error(errorMessage);
      }
      
      // Try to parse the successful response
      let data;
      try {
        data = await res.json();
      } catch (parseError) {
        console.error('JSON parse error:', parseError);
        const responseText = await res.text();
        console.error('Response text:', responseText);
        throw new Error('Invalid JSON response from server');
      }
      
      setResult(data);
    } catch (e: any) {
      console.error('Error in handleSubmit:', e);
      setError(e.message || 'Failed to calculate probability');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <>
      <Head>
        <title>CitiBike Probability Calculator</title>
        <meta name="description" content="Calculate the probability of encountering the same CitiBike twice" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
        <div className="max-w-xl mx-auto bg-white rounded-lg shadow p-8">
          <h1 className="text-2xl font-bold mb-2 text-citibike-blue">CitiBike Probability Calculator</h1>
          <p className="text-gray-600 mb-6 text-sm">
            Figure out your chance of getting the same CitiBike twice, based on your ride frequency and home station.
          </p>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block font-medium mb-1">Home Station</label>
              {loadingStations ? (
                <div>Loading stations...</div>
              ) : (
                <Combobox
                  value={form.home_station_id}
                  onChange={(value: string) => setForm(f => ({ ...f, home_station_id: value }))}
                >
                  <div className="relative">
                    <Combobox.Input
                      className="w-full border rounded px-3 py-2"
                      displayValue={(stationId: string) => {
                        const station = stations.find(s => s.station_id === stationId);
                        return station ? station.name : '';
                      }}
                      onChange={e => setQuery(e.target.value)}
                      placeholder="Search for a station..."
                    />
                    <Combobox.Options className="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                      {filteredStations.length === 0 && query !== '' ? (
                        <div className="px-4 py-2 text-gray-500">No stations found.</div>
                      ) : (
                        filteredStations.map((station: Station) => (
                          <Combobox.Option
                            key={station.station_id}
                            value={station.station_id}
                            className={({ active }: { active: boolean }) =>
                              `cursor-pointer select-none relative py-2 pl-3 pr-9 ${active ? 'bg-blue-100 text-blue-900' : 'text-gray-900'}`
                            }
                          >
                            {station.name}
                          </Combobox.Option>
                        ))
                      )}
                    </Combobox.Options>
                  </div>
                </Combobox>
              )}
            </div>
            <div>
              <label className="block font-medium mb-1">Riding Frequency (rides per week)</label>
              <input
                type="number"
                min={1}
                max={21}
                className="w-full border rounded px-3 py-2"
                value={form.riding_frequency}
                onChange={e => setForm(f => ({ ...f, riding_frequency: Number(e.target.value) }))}
                required
              />
            </div>
            <div>
              <label className="block font-medium mb-1">Time Pattern</label>
              <select
                className="w-full border rounded px-3 py-2"
                value={form.time_pattern}
                onChange={e => setForm(f => ({ ...f, time_pattern: e.target.value }))}
                required
              >
                <option value="weekday">Weekday</option>
                <option value="weekend">Weekend</option>
                <option value="both">Both</option>
              </select>
            </div>
            <button
              type="submit"
              className="btn-primary w-full py-3 text-lg"
              disabled={submitting || loadingStations}
            >
              {submitting ? 'Calculating...' : 'Calculate Probability'}
            </button>
          </form>
          {error && <div className="mt-4 text-red-600">{error}</div>}
          {result && (
            <div className="mt-8 bg-blue-50 rounded p-4">
              <h2 className="text-xl font-bold mb-2 text-citibike-blue">Result</h2>
              <div className="mb-2">
                <span className="font-medium">Probability:</span>{' '}
                <span className="text-lg">{(result.probability * 100).toFixed(2)}%</span>
              </div>
              <div className="mb-2">
                <span className="font-medium">Confidence Interval:</span>{' '}
                {result.confidence_interval[0] * 100}% - {result.confidence_interval[1] * 100}%
              </div>
              <div className="mb-2">
                <span className="font-medium">Explanation:</span>
                <div className="text-gray-700 mt-1">{result.explanation}</div>
              </div>
              {result.station_info && (
                <div className="mt-2 text-sm text-gray-500">
                  <div>Station: {result.station_info.name}</div>
                  <div>Total Trips: {result.station_info.total_trips}</div>
                  <div>Unique Bikes: {result.station_info.unique_bikes}</div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </>
  );
} 