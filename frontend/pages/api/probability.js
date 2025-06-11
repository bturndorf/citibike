export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  try {
    // Try multiple backend URLs
    const backendUrls = [
      process.env.NEXT_PUBLIC_API_URL,
      'http://localhost:8000',
      'http://127.0.0.1:8000',
      'http://backend:8000' // For Docker environments
    ].filter(Boolean);

    let lastError = null;
    
    for (const backendUrl of backendUrls) {
      try {
        console.log(`Trying backend URL: ${backendUrl}`);
        
        const response = await fetch(`${backendUrl}/api/probability`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(req.body),
        });

        if (response.ok) {
          const data = await response.json();
          return res.status(200).json(data);
        } else {
          const errorText = await response.text();
          console.error(`Backend error (${backendUrl}):`, response.status, errorText);
          lastError = { status: response.status, detail: errorText };
        }
      } catch (error) {
        console.error(`Connection error (${backendUrl}):`, error.message);
        lastError = { status: 500, detail: error.message };
      }
    }

    // If we get here, all backend URLs failed
    return res.status(lastError?.status || 500).json({
      message: 'Failed to connect to backend',
      detail: lastError?.detail || 'All backend URLs failed'
    });

  } catch (error) {
    console.error('Error in probability API:', error);
    res.status(500).json({ 
      message: 'Failed to calculate probability',
      error: error.message 
    });
  }
} 