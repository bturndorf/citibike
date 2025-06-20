Note from the human:
This project is about exploring Cursor and working with agentic AI tools. The code and documentation in this repo is generated by Cursor, with guidance provided by me through a requirements doc, PRD, project plan, and cursor rules developed iteratively. If you are looking for high-quality code... this is probably not a good place to look.

running at https://frontend-production-c03b.up.railway.app/

# CitiBike Rider Probability Application

A web application that estimates the probability that a NYC CitiBike rider has ridden the same bike twice, based on their riding patterns and station preferences.

## Project Overview

This application analyzes historical CitiBike usage patterns to calculate the likelihood of encountering the same bike multiple times during rides. Users can input their riding parameters (home station, frequency, time patterns) and receive probability estimates.

## Technology Stack

- **Frontend**: Next.js + TypeScript + Tailwind CSS
- **Backend**: Python + FastAPI + SQLAlchemy
- **Database**: PostgreSQL (Railway)
- **Deployment**: Railway (simple git push)
- **Maps**: Mapbox or Google Maps API
- **Charts**: Chart.js or Recharts

## Project Structure

```
citibike-mvp/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── requirements.txt     # Python dependencies
│   ├── models.py           # Database models
│   ├── data_ingestion.py   # One-time data load
│   └── probability.py      # Simple probability model
├── frontend/
│   ├── package.json        # Node dependencies
│   ├── pages/
│   │   ├── index.tsx       # Home page
│   │   └── calculate.tsx   # Calculator page
│   └── components/
│       ├── StationMap.tsx  # Simple map component
│       └── Results.tsx     # Results display
├── data/
│   └── citibike_data/      # Downloaded data files
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- Railway account
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd citibike-mvp
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Railway Deployment

1. **Connect to Railway**
   - Create Railway account at railway.app
   - Connect GitHub repository
   - Set up new project

2. **Deploy**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push origin main
   ```

## API Endpoints

- `GET /api/stations` - List all stations
- `GET /api/probability` - Calculate encounter probability
- `POST /api/calculate` - Submit calculation parameters
- `GET /api/health` - Health check

## Development Phases

1. **Phase 1**: Infrastructure Setup
2. **Phase 2**: Data Ingestion & Processing
3. **Phase 3**: Backend Development & Modeling
4. **Phase 4**: Frontend Development
5. **Phase 5**: Integration, Testing & Deployment

## Contributing

This project follows a phased development approach. Each phase builds upon the previous one with clear deliverables and testing criteria.

## License

MIT License 