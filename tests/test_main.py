"""
Tests for Password Strength Analyzer.
"""

import pytest
import os
import sys
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from password_analyzer import PasswordAnalyzer, app


@pytest.fixture
def analyzer():
    """Create a PasswordAnalyzer instance."""
    return PasswordAnalyzer()


@pytest.fixture
def client():
    """Create a Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


class TestAnalyzePassword:
    """Tests for analyze_password method."""

    def test_returns_dict_with_expected_keys(self, analyzer):
        """analyze_password should return a dict with all expected keys."""
        result = analyzer.analyze_password("test")
        expected_keys = {
            'password', 'length', 'strength_score', 'strength_level',
            'character_analysis', 'pattern_analysis', 'security_checks',
            'entropy', 'crack_time', 'recommendations',
        }
        assert expected_keys.issubset(result.keys())

    def test_weak_password_gets_low_score(self, analyzer):
        """A common weak password should score low."""
        result = analyzer.analyze_password("123456")
        assert result['strength_score'] <= 20

    def test_strong_password_gets_high_score(self, analyzer):
        """A complex password should score high."""
        result = analyzer.analyze_password("MyS3cur3P@ssw0rd!2024")
        assert result['strength_score'] >= 60


class TestCalculateEntropy:
    """Tests for _calculate_entropy method."""

    def test_returns_positive_float(self, analyzer):
        """Entropy of a non-empty password should be a positive float."""
        entropy = analyzer._calculate_entropy("abc123")
        assert isinstance(entropy, float)
        assert entropy > 0

    def test_empty_password_zero_entropy(self, analyzer):
        """An empty password should have zero entropy."""
        assert analyzer._calculate_entropy("") == 0


class TestFlaskAnalyzeRoute:
    """Tests for the /analyze API endpoint."""

    def test_returns_json_with_correct_structure(self, client):
        """/analyze should return JSON with expected top-level keys."""
        response = client.post(
            '/analyze',
            data=json.dumps({'password': 'Hello123!'}),
            content_type='application/json',
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'strength_score' in data
        assert 'strength_level' in data
        assert 'entropy' in data
        assert 'recommendations' in data

    def test_missing_password_returns_400(self, client):
        """/analyze with empty password should return 400."""
        response = client.post(
            '/analyze',
            data=json.dumps({'password': ''}),
            content_type='application/json',
        )
        assert response.status_code == 400


class TestFlaskGenerateRoute:
    """Tests for the /generate API endpoint."""

    def test_returns_password_of_requested_length(self, client):
        """/generate should return a password matching the requested length."""
        response = client.get('/generate?length=20')
        assert response.status_code == 200
        data = response.get_json()
        assert 'password' in data
        assert len(data['password']) == 20

    def test_default_length(self, client):
        """/generate without length param should default to 16."""
        response = client.get('/generate')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['password']) == 16


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
