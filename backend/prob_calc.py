import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import logging
from sqlalchemy.orm import Session
from sqlalchemy import text
import json
import os

logger = logging.getLogger(__name__)

class CitiBikeProbabilityCalculator:
    """
    Calculates the probability of encountering the same CitiBike twice
    based on historical trip data and user riding patterns.
    """
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.station_stats = {}
        self.bike_movement_patterns = {}
        
    def load_station_statistics(self) -> Dict:
        """Load and cache station statistics from database"""
        logger.info("Starting load_station_statistics")
        if self.station_stats:
            logger.info(f"Using cached station stats for {len(self.station_stats)} stations")
            return self.station_stats
            
        try:
            # Get station statistics - PostgreSQL compatible version
            query = text("""
                SELECT 
                    s.station_id,
                    s.name,
                    s.latitude,
                    s.longitude,
                    COUNT(t.id) as total_trips,
                    COUNT(DISTINCT t.bike_id) as unique_bikes,
                    AVG(EXTRACT(EPOCH FROM (t.ended_at - t.started_at)) / 60) as avg_trip_duration
                FROM stations s
                LEFT JOIN trips t ON s.station_id = t.start_station_id
                GROUP BY s.station_id, s.name, s.latitude, s.longitude
                ORDER BY total_trips DESC
            """)
            
            logger.info("Executing station statistics query")
            result = self.db_session.execute(query)
            stations = []
            
            for row in result:
                stations.append({
                    'station_id': row.station_id,
                    'name': row.name,
                    'latitude': float(row.latitude),
                    'longitude': float(row.longitude),
                    'total_trips': row.total_trips or 0,
                    'unique_bikes': row.unique_bikes or 0,
                    'avg_trip_duration': row.avg_trip_duration or 0
                })
            
            self.station_stats = {s['station_id']: s for s in stations}
            logger.info(f"Loaded statistics for {len(stations)} stations")
            logger.info(f"Sample station IDs: {list(self.station_stats.keys())[:5]}")
            return self.station_stats
            
        except Exception as e:
            logger.error(f"Error loading station statistics: {e}")
            return {}
    
    def calculate_bike_movement_probability(self, home_station_id: str, 
                                          riding_frequency: int,
                                          time_pattern: str) -> Dict:
        """
        Calculate the probability of encountering the same bike twice
        
        Args:
            home_station_id: User's primary station
            riding_frequency: Number of rides per week
            time_pattern: "weekday", "weekend", or "both"
            
        Returns:
            Dictionary with probability calculation results
        """
        logger.info(f"Starting probability calculation for station {home_station_id}, frequency {riding_frequency}, pattern {time_pattern}")
        try:
            # Load station statistics
            station_stats = self.load_station_statistics()
            logger.info(f"Available station IDs: {list(station_stats.keys())[:10]}")
            logger.info(f"Looking for station ID: {home_station_id}")
            
            if home_station_id not in station_stats:
                logger.error(f"Station {home_station_id} not found in database")
                logger.error(f"Available stations: {list(station_stats.keys())[:20]}")
                raise ValueError(f"Station {home_station_id} not found in database")
            
            home_station = station_stats[home_station_id]
            logger.info(f"Found home station: {home_station}")
            
            # Get bike movement patterns for the home station
            logger.info("Getting bike movement patterns")
            bike_patterns = self._get_bike_movement_patterns(home_station_id, time_pattern)
            logger.info(f"Bike patterns: {bike_patterns}")
            
            # Calculate probability using multiple factors
            logger.info("Calculating encounter probability")
            probability = self._calculate_encounter_probability(
                home_station, bike_patterns, riding_frequency, time_pattern
            )
            logger.info(f"Calculated probability: {probability}")
            
            # Calculate confidence interval
            logger.info("Calculating confidence interval")
            confidence_interval = self._calculate_confidence_interval(probability, home_station)
            
            # Generate explanation
            logger.info("Generating explanation")
            explanation = self._generate_explanation(
                probability, home_station, bike_patterns, riding_frequency, time_pattern
            )
            
            result = {
                'probability': probability,
                'confidence_interval': confidence_interval,
                'explanation': explanation,
                'station_info': home_station,
                'bike_patterns': bike_patterns
            }
            logger.info(f"Final result: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error calculating probability: {e}")
            logger.error(f"Exception type: {type(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    
    def _get_bike_movement_patterns(self, station_id: str, time_pattern: str) -> Dict:
        """Get bike movement patterns for a specific station and time pattern"""
        logger.info(f"Getting bike movement patterns for station {station_id}, pattern {time_pattern}")
        try:
            # Build time filter based on pattern - PostgreSQL compatible
            time_filter = ""
            if time_pattern == "weekday":
                time_filter = "AND EXTRACT(DOW FROM t.started_at) BETWEEN 1 AND 5"
            elif time_pattern == "weekend":
                time_filter = "AND EXTRACT(DOW FROM t.started_at) IN (0, 6)"
            
            query_text = f"""
                SELECT 
                    t.bike_id,
                    COUNT(*) as trip_count,
                    AVG(EXTRACT(EPOCH FROM (t.ended_at - t.started_at)) / 60) as avg_duration,
                    COUNT(DISTINCT t.end_station_id) as unique_destinations
                FROM trips t
                WHERE t.start_station_id = :station_id {time_filter}
                GROUP BY t.bike_id
                ORDER BY trip_count DESC
                LIMIT 100
            """
            logger.info(f"Executing bike patterns query: {query_text}")
            logger.info(f"Query parameters: station_id={station_id}")
            
            query = text(query_text)
            result = self.db_session.execute(query, {'station_id': station_id})
            patterns = []
            
            for row in result:
                patterns.append({
                    'bike_id': row.bike_id,
                    'trip_count': row.trip_count,
                    'avg_duration': row.avg_duration or 0,
                    'unique_destinations': row.unique_destinations
                })
            
            logger.info(f"Found {len(patterns)} bike patterns")
            
            # Calculate summary statistics
            if patterns:
                total_bikes = len(patterns)
                avg_trips_per_bike = np.mean([p['trip_count'] for p in patterns])
                bike_return_rate = self._calculate_bike_return_rate(station_id, time_pattern)
                
                return {
                    'total_bikes_analyzed': total_bikes,
                    'avg_trips_per_bike': avg_trips_per_bike,
                    'bike_return_rate': bike_return_rate,
                    'patterns': patterns[:10]  # Top 10 bikes
                }
            else:
                logger.warning(f"No bike patterns found for station {station_id}")
                return {
                    'total_bikes_analyzed': 0,
                    'avg_trips_per_bike': 0,
                    'bike_return_rate': 0,
                    'patterns': []
                }
                
        except Exception as e:
            logger.error(f"Error getting bike movement patterns: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return {}
    
    def _calculate_bike_return_rate(self, station_id: str, time_pattern: str) -> float:
        """Calculate the rate at which bikes return to the same station"""
        logger.info(f"Calculating bike return rate for station {station_id}, pattern {time_pattern}")
        try:
            time_filter = ""
            if time_pattern == "weekday":
                time_filter = "AND EXTRACT(DOW FROM t1.started_at) BETWEEN 1 AND 5"
            elif time_pattern == "weekend":
                time_filter = "AND EXTRACT(DOW FROM t1.started_at) IN (0, 6)"
            
            query_text = f"""
                SELECT 
                    COUNT(DISTINCT t1.bike_id) as bikes_returning,
                    COUNT(DISTINCT t1.bike_id) as total_bikes
                FROM trips t1
                WHERE t1.start_station_id = :station_id {time_filter}
                AND EXISTS (
                    SELECT 1 FROM trips t2 
                    WHERE t2.bike_id = t1.bike_id 
                    AND t2.end_station_id = :station_id
                    AND t2.started_at > t1.ended_at
                    AND t2.started_at <= t1.ended_at + INTERVAL '7 days'
                )
            """
            logger.info(f"Executing bike return rate query: {query_text}")
            
            query = text(query_text)
            result = self.db_session.execute(query, {'station_id': station_id})
            row = result.fetchone()
            
            if row and row.total_bikes > 0:
                return_rate = row.bikes_returning / row.total_bikes
                logger.info(f"Bike return rate: {return_rate} ({row.bikes_returning}/{row.total_bikes})")
                return return_rate
            else:
                logger.warning(f"No bike return data found for station {station_id}")
                return 0.0
                
        except Exception as e:
            logger.error(f"Error calculating bike return rate: {e}")
            return 0.0
    
    def _calculate_encounter_probability(self, home_station: Dict, 
                                       bike_patterns: Dict,
                                       riding_frequency: int,
                                       time_pattern: str) -> float:
        """
        Calculate the probability of encountering the same bike twice
        using a combination of factors:
        1. Station popularity (more trips = higher chance)
        2. Bike return rate (bikes returning to station)
        3. Riding frequency (more rides = higher chance)
        4. Time pattern (weekday vs weekend patterns)
        """
        try:
            # Base probability from station popularity
            total_trips = home_station.get('total_trips', 0)
            unique_bikes = home_station.get('unique_bikes', 1)
            
            if total_trips == 0 or unique_bikes == 0:
                return 0.0
            
            # Calculate bike turnover rate
            bike_turnover_rate = total_trips / unique_bikes
            
            # Base probability (simplified model)
            base_probability = min(0.3, bike_turnover_rate / 1000)  # Cap at 30%
            
            # Adjust for riding frequency
            frequency_multiplier = min(2.0, riding_frequency / 5)  # Normalize to 5 rides/week
            
            # Adjust for bike return rate
            return_rate = bike_patterns.get('bike_return_rate', 0.0)
            return_rate_multiplier = 1 + (return_rate * 2)  # Boost if bikes return
            
            # Time pattern adjustment
            time_multiplier = 1.0
            if time_pattern == "weekday":
                time_multiplier = 1.2  # Weekdays have more consistent patterns
            elif time_pattern == "weekend":
                time_multiplier = 0.8  # Weekends have more random patterns
            
            # Calculate final probability
            probability = base_probability * frequency_multiplier * return_rate_multiplier * time_multiplier
            
            # Ensure probability is between 0 and 1
            return max(0.0, min(1.0, probability))
            
        except Exception as e:
            logger.error(f"Error in probability calculation: {e}")
            return 0.0
    
    def _calculate_confidence_interval(self, probability: float, home_station: Dict) -> List[float]:
        """Calculate confidence interval based on data quality and sample size"""
        try:
            total_trips = home_station.get('total_trips', 0)
            
            # Confidence interval based on sample size
            if total_trips > 10000:
                margin = 0.02  # High confidence
            elif total_trips > 1000:
                margin = 0.05  # Medium confidence
            else:
                margin = 0.10  # Low confidence
            
            lower = max(0.0, probability - margin)
            upper = min(1.0, probability + margin)
            
            return [round(lower, 3), round(upper, 3)]
            
        except Exception as e:
            logger.error(f"Error calculating confidence interval: {e}")
            return [0.0, 1.0]
    
    def _generate_explanation(self, probability: float, home_station: Dict,
                            bike_patterns: Dict, riding_frequency: int,
                            time_pattern: str) -> str:
        """Generate a human-readable explanation of the probability calculation"""
        try:
            station_name = home_station.get('name', 'your station')
            total_trips = home_station.get('total_trips', 0)
            unique_bikes = home_station.get('unique_bikes', 0)
            return_rate = bike_patterns.get('bike_return_rate', 0.0)
            
            explanation = f"Based on analysis of {total_trips:,} trips from {station_name} "
            explanation += f"involving {unique_bikes:,} unique bikes, "
            
            if probability < 0.05:
                explanation += "the probability is quite low. This station has high bike turnover, "
                explanation += "meaning bikes rarely return to the same location."
            elif probability < 0.15:
                explanation += "the probability is moderate. While some bikes do return, "
                explanation += "the station's popularity means many different bikes pass through."
            elif probability < 0.30:
                explanation += "the probability is relatively high. This station has good bike return patterns, "
                explanation += "increasing your chances of encountering the same bike."
            else:
                explanation += "the probability is quite high. This station has excellent bike return patterns "
                explanation += "and consistent bike availability."
            
            explanation += f" With your {riding_frequency} rides per week on {time_pattern}s, "
            explanation += f"and a bike return rate of {return_rate:.1%}, "
            explanation += f"you have approximately a {probability:.1%} chance of riding the same bike twice."
            
            return explanation
            
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return "Unable to generate explanation due to calculation error."

def calculate_probability(db_session: Session, home_station_id: str,
                         riding_frequency: int, time_pattern: str) -> Dict:
    """
    Main function to calculate bike encounter probability
    
    Args:
        db_session: Database session
        home_station_id: User's primary station ID
        riding_frequency: Number of rides per week
        time_pattern: "weekday", "weekend", or "both"
        
    Returns:
        Dictionary with probability results
    """
    calculator = CitiBikeProbabilityCalculator(db_session)
    return calculator.calculate_bike_movement_probability(
        home_station_id, riding_frequency, time_pattern
    ) 