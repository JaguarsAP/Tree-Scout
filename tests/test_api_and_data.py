"""
Test suite for Tree-Scout project
Tests API connectivity and data format validation
"""

import pytest
import pandas as pd
import numpy as np
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDataFormat:
    """Tests to validate data files are in correct format"""
    
    def test_county_boundingboxes_exists(self):
        """Test that US_County_Boundingboxes.csv exists and has required columns"""
        filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                'US_County_Boundingboxes.csv')
        assert os.path.exists(filepath), "US_County_Boundingboxes.csv not found"
        
        df = pd.read_csv(filepath)
        required_cols = ['COUNTY_NAME', 'STATEFP', 'COUNTYFP', 'GEOID', 
                         'xmin', 'xmax', 'ymin', 'ymax']
        for col in required_cols:
            assert col in df.columns, f"Missing required column: {col}"
    
    def test_county_boundingboxes_valid_coordinates(self):
        """Test that bounding box coordinates are valid"""
        filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                'US_County_Boundingboxes.csv')
        df = pd.read_csv(filepath)
        
        # Check coordinate ranges for continental US
        assert df['xmin'].min() >= -180, "xmin out of valid longitude range"
        assert df['xmax'].max() <= 0, "xmax should be negative for US"
        assert df['ymin'].min() >= 0, "ymin should be positive for US"
        assert df['ymax'].max() <= 90, "ymax out of valid latitude range"
        
        # xmin should always be less than xmax
        assert (df['xmin'] < df['xmax']).all(), "xmin should be less than xmax"
        # ymin should always be less than ymax
        assert (df['ymin'] < df['ymax']).all(), "ymin should be less than ymax"
    
    def test_county_boundingboxes_fips_format(self):
        """Test that FIPS codes are in correct format"""
        filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                'US_County_Boundingboxes.csv')
        df = pd.read_csv(filepath)
        
        # GEOID should be 5 digits (can have leading zeros)
        df['GEOID_str'] = df['GEOID'].astype(str).str.zfill(5)
        assert df['GEOID_str'].str.len().max() == 5, "GEOID should be 5 digits"
        
        # State FIPS should be 1-2 digits (1-56)
        assert df['STATEFP'].min() >= 1, "State FIPS should be >= 1"
        assert df['STATEFP'].max() <= 78, "State FIPS should be <= 78"


class TestForestDataFormat:
    """Tests for the forest loss data output format"""
    
    @pytest.fixture
    def forest_data_path(self):
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                            'county_forest_loss_data.csv')
    
    def test_forest_data_columns(self, forest_data_path):
        """Test that forest data has required columns"""
        if not os.path.exists(forest_data_path):
            pytest.skip("county_forest_loss_data.csv not generated yet")
        
        df = pd.read_csv(forest_data_path)
        required_cols = ['County_Name', 'State_FIPS', 'County_FIPS', 'Year', 
                         'Tree_Loss_Hectares', 'Carbon_Emissions_Mg_CO2e', 
                         'Tree_Cover_Extent_Ha']
        for col in required_cols:
            assert col in df.columns, f"Missing required column: {col}"
    
    def test_forest_data_year_range(self, forest_data_path):
        """Test that years are within expected range"""
        if not os.path.exists(forest_data_path):
            pytest.skip("county_forest_loss_data.csv not generated yet")
        
        df = pd.read_csv(forest_data_path)
        assert df['Year'].min() >= 2000, "Year should be >= 2000"
        assert df['Year'].max() <= 2025, "Year should be <= 2025"
    
    def test_forest_data_no_negative_loss(self, forest_data_path):
        """Test that tree loss values are non-negative"""
        if not os.path.exists(forest_data_path):
            pytest.skip("county_forest_loss_data.csv not generated yet")
        
        df = pd.read_csv(forest_data_path)
        assert (df['Tree_Loss_Hectares'] >= 0).all(), "Tree loss should be non-negative"


class TestEnhancedDataFormat:
    """Tests for the enhanced dataset with external features"""
    
    @pytest.fixture
    def enhanced_data_path(self):
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                            'county_forest_data_enhanced.csv')
    
    def test_enhanced_data_has_climate_features(self, enhanced_data_path):
        """Test that enhanced data includes climate features"""
        if not os.path.exists(enhanced_data_path):
            pytest.skip("county_forest_data_enhanced.csv not generated yet")
        
        df = pd.read_csv(enhanced_data_path)
        climate_cols = ['Atmospheric_CO2_ppm', 'Total_CO2_Mt', 'CO2_Per_Capita_t']
        found_cols = [col for col in climate_cols if col in df.columns]
        assert len(found_cols) > 0, "No climate features found in enhanced data"
    
    def test_enhanced_data_has_stock_features(self, enhanced_data_path):
        """Test that enhanced data includes stock price features"""
        if not os.path.exists(enhanced_data_path):
            pytest.skip("county_forest_data_enhanced.csv not generated yet")
        
        df = pd.read_csv(enhanced_data_path)
        stock_cols = [col for col in df.columns if 'Price' in col or 'Logging' in col]
        assert len(stock_cols) > 0, "No stock price features found in enhanced data"


class TestAPIConnectivity:
    """Tests to verify API endpoints are accessible"""
    
    def test_noaa_co2_endpoint(self):
        """Test that NOAA CO2 data endpoint is accessible"""
        import requests
        url = "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_mlo.txt"
        try:
            response = requests.get(url, timeout=10)
            assert response.status_code == 200, "NOAA CO2 endpoint not accessible"
            # Check that we got actual data
            assert len(response.text) > 100, "NOAA response too short"
        except requests.exceptions.RequestException as e:
            pytest.skip(f"Network unavailable: {e}")
    
    def test_owid_emissions_endpoint(self):
        """Test that Our World in Data emissions endpoint is accessible"""
        import requests
        url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
        try:
            response = requests.get(url, timeout=15)
            assert response.status_code == 200, "OWID emissions endpoint not accessible"
            # Check that we got CSV data
            assert 'country' in response.text.lower(), "OWID response doesn't look like expected CSV"
        except requests.exceptions.RequestException as e:
            pytest.skip(f"Network unavailable: {e}")
    
    def test_gfw_api_endpoint_reachable(self):
        """Test that GFW API base URL is reachable"""
        import requests
        url = "https://data-api.globalforestwatch.org"
        try:
            response = requests.get(url, timeout=10)
            # API may return various status codes, but should be reachable
            assert response.status_code < 500, "GFW API server error"
        except requests.exceptions.RequestException as e:
            pytest.skip(f"Network unavailable: {e}")


class TestTrainTestSplit:
    """Tests for train/test data split files"""
    
    def test_train_test_files_exist(self):
        """Test that train and test CSV files exist after running notebook"""
        base_path = os.path.dirname(os.path.dirname(__file__))
        train_path = os.path.join(base_path, 'county_forest_data_train.csv')
        test_path = os.path.join(base_path, 'county_forest_data_test.csv')
        
        if not os.path.exists(train_path) or not os.path.exists(test_path):
            pytest.skip("Train/test files not generated yet")
        
        df_train = pd.read_csv(train_path)
        df_test = pd.read_csv(test_path)
        
        assert len(df_train) > 0, "Training data is empty"
        assert len(df_test) > 0, "Test data is empty"
    
    def test_no_data_leakage(self):
        """Test that test years don't appear in training data (no leakage)"""
        base_path = os.path.dirname(os.path.dirname(__file__))
        train_path = os.path.join(base_path, 'county_forest_data_train.csv')
        test_path = os.path.join(base_path, 'county_forest_data_test.csv')
        
        if not os.path.exists(train_path) or not os.path.exists(test_path):
            pytest.skip("Train/test files not generated yet")
        
        df_train = pd.read_csv(train_path)
        df_test = pd.read_csv(test_path)
        
        train_years = set(df_train['Year'].unique())
        test_years = set(df_test['Year'].unique())
        
        overlap = train_years.intersection(test_years)
        assert len(overlap) == 0, f"Data leakage detected! Overlapping years: {overlap}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
