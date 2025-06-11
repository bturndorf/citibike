export default async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  try {
    // Try to fetch stations from the backend first
    const backendUrls = [
      process.env.NEXT_PUBLIC_API_URL,
      'http://localhost:8000',
      'http://127.0.0.1:8000'
    ].filter(Boolean);

    let stations = null;
    
    for (const backendUrl of backendUrls) {
      try {
        console.log(`Trying to fetch stations from: ${backendUrl}`);
        const response = await fetch(`${backendUrl}/api/stations`);
        
        if (response.ok) {
          stations = await response.json();
          console.log(`Successfully fetched ${stations.length} stations from backend`);
          break;
        } else {
          console.error(`Backend error (${backendUrl}):`, response.status);
        }
      } catch (error) {
        console.error(`Connection error (${backendUrl}):`, error.message);
      }
    }

    // If backend is not available, fall back to JSON file
    if (!stations) {
      console.log('Falling back to JSON file');
      const fs = await import('fs');
      const path = await import('path');
      
      // Read the stations JSON file
      const stationsPath = path.join(process.cwd(), '..', 'data', 'citibike_data', 'stations.json');
      const stationsData = JSON.parse(fs.readFileSync(stationsPath, 'utf8'));
      
      // Transform the data to match the expected format
      stations = stationsData.data.stations.map((station, index) => ({
        id: index + 1,
        station_id: station.station_id,
        name: station.name,
        latitude: station.lat,
        longitude: station.lon,
        total_trips: 0, // We don't have trip data in the JSON
        unique_bikes: 0  // We don't have bike data in the JSON
      }));
    }

    // Sort stations alphabetically by name
    stations.sort((a, b) => a.name.localeCompare(b.name));

    res.status(200).json(stations);
  } catch (error) {
    console.error('Error loading stations:', error);
    res.status(500).json({ 
      message: 'Failed to load stations',
      error: error.message 
    });
  }
} 