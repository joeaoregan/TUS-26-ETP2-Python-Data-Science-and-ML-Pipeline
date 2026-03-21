#!/usr/bin/env python3
"""
API Test Client
Simple client to test the AI Traffic Control API
"""

import sys
import json
import requests
import time
from typing import List, Dict, Any
import random


class TrafficAPIClient:
    """Client for the Traffic Control API."""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def check_health(self) -> bool:
        """Check if the API is healthy."""
        try:
            response = self.session.get(f"{self.base_url}/api/traffic/health")
            response.raise_for_status()
            data = response.json()
            return data.get("status") == "healthy"
        except Exception as e:
            print(f"Health check failed: {e}")
            return False
    
    def get_action(self) -> Dict[str, Any]:
        """Get traffic action with auto-generated observations."""
        response = self.session.get(f"{self.base_url}/api/traffic/action")
        response.raise_for_status()
        return response.json()
    
    def predict_action(self, observations: List[float]) -> Dict[str, Any]:
        """Predict action with custom observations."""
        payload = {"observations": observations}
        response = self.session.post(
            f"{self.base_url}/api/traffic/action",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        try:
            response = self.session.get("http://localhost:8000/model_info")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Could not fetch model info: {e}")
            return None


def print_response(response: Dict[str, Any], title: str = "Response") -> None:
    """Pretty print API response."""
    print(f"\n{title}:")
    print(json.dumps(response, indent=2))


def test_basic_functionality(client: TrafficAPIClient) -> None:
    """Test basic API functionality."""
    print("=" * 60)
    print("TEST 1: Basic Functionality")
    print("=" * 60)
    
    # Test health
    print("\n1. Health Check...")
    if client.check_health():
        print("✓ API is healthy")
    else:
        print("✗ API health check failed")
        return
    
    # Test auto-generated action
    print("\n2. Get Traffic Action (auto-generated observations)...")
    try:
        response = client.get_action()
        print_response(response)
        print(f"✓ Got traffic action: {response.get('signalState')}")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_custom_observations(client: TrafficAPIClient) -> None:
    """Test with custom observations."""
    print("\n\n" + "=" * 60)
    print("TEST 2: Custom Observations")
    print("=" * 60)
    
    # Test 1: Low traffic
    print("\n1. Low Traffic Scenario (mostly zeros)...")
    low_traffic = [0.1 * random.random() for _ in range(10)]
    try:
        response = client.predict_action(low_traffic)
        print_response(response)
        print(f"✓ Action for low traffic: {response.get('signalState')}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 2: High traffic
    print("\n2. High Traffic Scenario (mostly ones)...")
    high_traffic = [0.9 + 0.1 * random.random() for _ in range(10)]
    try:
        response = client.predict_action(high_traffic)
        print_response(response)
        print(f"✓ Action for high traffic: {response.get('signalState')}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 3: Mixed traffic
    print("\n3. Mixed Traffic Scenario...")
    mixed_traffic = [random.random() for _ in range(10)]
    try:
        response = client.predict_action(mixed_traffic)
        print_response(response)
        print(f"✓ Action for mixed traffic: {response.get('signalState')}")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_load_testing(client: TrafficAPIClient, num_requests: int = 10) -> None:
    """Simple load test."""
    print("\n\n" + "=" * 60)
    print(f"TEST 3: Load Testing ({num_requests} requests)")
    print("=" * 60)
    
    successful = 0
    failed = 0
    response_times = []
    
    print(f"\nSending {num_requests} requests...")
    
    for i in range(num_requests):
        try:
            start_time = time.time()
            response = client.get_action()
            elapsed = time.time() - start_time
            response_times.append(elapsed)
            successful += 1
            print(f"  Request {i+1}: {elapsed*1000:.2f}ms - {response.get('signalState')}")
        except Exception as e:
            failed += 1
            print(f"  Request {i+1}: FAILED - {e}")
    
    # Statistics
    print(f"\n{'='*60}")
    print(f"Load Test Results:")
    print(f"  Successful: {successful}/{num_requests}")
    print(f"  Failed: {failed}/{num_requests}")
    
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        print(f"  Avg Response Time: {avg_time*1000:.2f}ms")
        print(f"  Min Response Time: {min_time*1000:.2f}ms")
        print(f"  Max Response Time: {max_time*1000:.2f}ms")


def test_model_info(client: TrafficAPIClient) -> None:
    """Test getting model information."""
    print("\n\n" + "=" * 60)
    print("TEST 4: Model Information")
    print("=" * 60)
    
    try:
        info = client.get_model_info()
        if info:
            print_response(info)
        else:
            print("Could not retrieve model information")
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Main test function."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "AI Traffic Control API - Test Client" + " " * 7 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # Initialize client
    api_url = "http://localhost:8080"
    print(f"\nConnecting to API at {api_url}...")
    client = TrafficAPIClient(api_url)
    
    # Check if API is available
    if not client.check_health():
        print(f"\n✗ Cannot connect to API at {api_url}")
        print("Make sure the services are running with: docker-compose up")
        sys.exit(1)
    
    print("✓ Connected successfully!")
    
    # Run tests
    test_basic_functionality(client)
    test_custom_observations(client)
    test_load_testing(client, num_requests=5)
    test_model_info(client)
    
    print("\n\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
