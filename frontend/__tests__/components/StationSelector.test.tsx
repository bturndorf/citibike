import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import StationSelector from '../../components/StationSelector'

// Mock the API call
const mockStations = [
  { station_id: 'test-uuid-1', name: 'Test Station 1', latitude: 40.7589, longitude: -73.9851 },
  { station_id: 'test-uuid-2', name: 'Test Station 2', latitude: 40.7505, longitude: -73.9934 },
  { station_id: 'test-uuid-3', name: 'Test Station 3', latitude: 40.7484, longitude: -73.9857 },
]

// Mock fetch
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve(mockStations),
  })
) as jest.Mock

describe('StationSelector', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders station selector component', async () => {
    render(<StationSelector onStationSelect={() => {}} />)
    
    // Check if the component renders
    expect(screen.getByText(/select your home station/i)).toBeInTheDocument()
    
    // Wait for stations to load
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/stations')
    })
  })

  it('loads and displays stations', async () => {
    render(<StationSelector onStationSelect={() => {}} />)
    
    // Wait for stations to load
    await waitFor(() => {
      expect(screen.getByText('Test Station 1')).toBeInTheDocument()
      expect(screen.getByText('Test Station 2')).toBeInTheDocument()
      expect(screen.getByText('Test Station 3')).toBeInTheDocument()
    })
  })

  it('allows searching for stations', async () => {
    const user = userEvent.setup()
    render(<StationSelector onStationSelect={() => {}} />)
    
    // Wait for stations to load
    await waitFor(() => {
      expect(screen.getByText('Test Station 1')).toBeInTheDocument()
    })
    
    // Find and click the combobox
    const combobox = screen.getByRole('combobox')
    await user.click(combobox)
    
    // Type to search
    await user.type(combobox, 'Test Station 1')
    
    // Should show filtered results
    expect(screen.getByText('Test Station 1')).toBeInTheDocument()
    expect(screen.queryByText('Test Station 2')).not.toBeInTheDocument()
  })

  it('calls onStationSelect when a station is selected', async () => {
    const mockOnStationSelect = jest.fn()
    const user = userEvent.setup()
    
    render(<StationSelector onStationSelect={mockOnStationSelect} />)
    
    // Wait for stations to load
    await waitFor(() => {
      expect(screen.getByText('Test Station 1')).toBeInTheDocument()
    })
    
    // Find and click the combobox
    const combobox = screen.getByRole('combobox')
    await user.click(combobox)
    
    // Select a station
    const stationOption = screen.getByText('Test Station 1')
    await user.click(stationOption)
    
    // Check if callback was called with correct data
    expect(mockOnStationSelect).toHaveBeenCalledWith('test-uuid-1')
  })

  it('handles API errors gracefully', async () => {
    // Mock fetch to return an error
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
      })
    ) as jest.Mock
    
    render(<StationSelector onStationSelect={() => {}} />)
    
    // Should show error message
    await waitFor(() => {
      expect(screen.getByText(/error loading stations/i)).toBeInTheDocument()
    })
  })

  it('handles empty station list', async () => {
    // Mock fetch to return empty array
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve([]),
      })
    ) as jest.Mock
    
    render(<StationSelector onStationSelect={() => {}} />)
    
    // Should show no stations message
    await waitFor(() => {
      expect(screen.getByText(/no stations available/i)).toBeInTheDocument()
    })
  })

  it('filters stations alphabetically', async () => {
    const user = userEvent.setup()
    render(<StationSelector onStationSelect={() => {}} />)
    
    // Wait for stations to load
    await waitFor(() => {
      expect(screen.getByText('Test Station 1')).toBeInTheDocument()
    })
    
    // Find and click the combobox
    const combobox = screen.getByRole('combobox')
    await user.click(combobox)
    
    // Check that stations are in alphabetical order
    const stationElements = screen.getAllByRole('option')
    const stationNames = stationElements.map(el => el.textContent)
    
    expect(stationNames).toEqual([
      'Test Station 1',
      'Test Station 2', 
      'Test Station 3'
    ])
  })
}) 