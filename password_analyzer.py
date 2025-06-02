#!/usr/bin/env python3
"""
Password Strength Analyzer
Advanced password security analysis and strength testing tool.
"""

import re
import math
import hashlib
import requests
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

class PasswordAnalyzer:
    """Password strength analysis functionality."""
    
    def __init__(self):
        self.common_passwords = self._load_common_passwords()
    
    def _load_common_passwords(self):
        """Load common passwords list."""
        # Common passwords for demonstration
        return [
            'password', '123456', '123456789', 'qwerty', 'abc123',
            'password123', 'admin', 'letmein', 'welcome', 'monkey',
            'dragon', 'master', 'shadow', 'superman', 'michael',
            'football', 'baseball', 'liverpool', 'jordan', 'princess'
        ]
    
    def analyze_password(self, password):
        """Comprehensive password analysis."""
        analysis = {
            'password': password,
            'length': len(password),
            'strength_score': 0,
            'strength_level': 'Very Weak',
            'character_analysis': self._analyze_characters(password),
            'pattern_analysis': self._analyze_patterns(password),
            'security_checks': self._security_checks(password),
            'entropy': self._calculate_entropy(password),
            'crack_time': self._estimate_crack_time(password),
            'recommendations': []
        }
        
        # Calculate overall strength score
        analysis['strength_score'] = self._calculate_strength_score(analysis)
        analysis['strength_level'] = self._get_strength_level(analysis['strength_score'])
        analysis['recommendations'] = self._get_recommendations(analysis)
        
        return analysis
    
    def _analyze_characters(self, password):
        """Analyze character composition."""
        return {
            'lowercase': len(re.findall(r'[a-z]', password)),
            'uppercase': len(re.findall(r'[A-Z]', password)),
            'digits': len(re.findall(r'\d', password)),
            'special': len(re.findall(r'[^a-zA-Z0-9]', password)),
            'has_lowercase': bool(re.search(r'[a-z]', password)),
            'has_uppercase': bool(re.search(r'[A-Z]', password)),
            'has_digits': bool(re.search(r'\d', password)),
            'has_special': bool(re.search(r'[^a-zA-Z0-9]', password)),
            'unique_chars': len(set(password))
        }
    
    def _analyze_patterns(self, password):
        """Analyze password patterns."""
        patterns = {
            'repeated_chars': self._find_repeated_chars(password),
            'sequential': self._find_sequential_patterns(password),
            'keyboard_patterns': self._find_keyboard_patterns(password),
            'common_substitutions': self._find_common_substitutions(password),
            'dictionary_words': self._find_dictionary_words(password)
        }
        
        return patterns
    
    def _security_checks(self, password):
        """Perform security-related checks."""
        return {
            'is_common': password.lower() in self.common_passwords,
            'contains_personal_info': self._contains_personal_info(password),
            'pwned_check': self._check_pwned_passwords(password),
            'meets_basic_requirements': self._meets_basic_requirements(password)
        }
    
    def _calculate_entropy(self, password):
        """Calculate password entropy."""
        charset_size = 0
        
        if re.search(r'[a-z]', password):
            charset_size += 26
        if re.search(r'[A-Z]', password):
            charset_size += 26
        if re.search(r'\d', password):
            charset_size += 10
        if re.search(r'[^a-zA-Z0-9]', password):
            charset_size += 32  # Approximate special characters
        
        if charset_size == 0:
            return 0
        
        entropy = len(password) * math.log2(charset_size)
        return round(entropy, 2)
    
    def _estimate_crack_time(self, password):
        """Estimate time to crack password."""
        entropy = self._calculate_entropy(password)
        
        # Assumptions: 1 billion guesses per second
        guesses_per_second = 1e9
        total_combinations = 2 ** entropy
        
        # Average time is half of total combinations
        seconds = total_combinations / (2 * guesses_per_second)
        
        return self._format_time(seconds)
    
    def _format_time(self, seconds):
        """Format time duration."""
        if seconds < 1:
            return "Instant"
        elif seconds < 60:
            return f"{seconds:.1f} seconds"
        elif seconds < 3600:
            return f"{seconds/60:.1f} minutes"
        elif seconds < 86400:
            return f"{seconds/3600:.1f} hours"
        elif seconds < 31536000:
            return f"{seconds/86400:.1f} days"
        else:
            return f"{seconds/31536000:.1f} years"
    
    def _find_repeated_chars(self, password):
        """Find repeated character patterns."""
        repeated = []
        for i in range(len(password) - 1):
            if password[i] == password[i + 1]:
                repeated.append(password[i])
        return list(set(repeated))
    
    def _find_sequential_patterns(self, password):
        """Find sequential patterns."""
        sequences = []
        
        # Check for ascending sequences
        for i in range(len(password) - 2):
            if (ord(password[i+1]) == ord(password[i]) + 1 and 
                ord(password[i+2]) == ord(password[i]) + 2):
                sequences.append(password[i:i+3])
        
        return sequences
    
    def _find_keyboard_patterns(self, password):
        """Find keyboard patterns."""
        keyboard_rows = [
            'qwertyuiop',
            'asdfghjkl',
            'zxcvbnm',
            '1234567890'
        ]
        
        patterns = []
        for row in keyboard_rows:
            for i in range(len(row) - 2):
                pattern = row[i:i+3]
                if pattern.lower() in password.lower():
                    patterns.append(pattern)
        
        return patterns
    
    def _find_common_substitutions(self, password):
        """Find common character substitutions."""
        substitutions = {
            '@': 'a', '3': 'e', '1': 'i', '0': 'o', '5': 's',
            '7': 't', '4': 'a', '8': 'b', '!': 'i'
        }
        
        found = []
        for char, replacement in substitutions.items():
            if char in password:
                found.append(f"{char} → {replacement}")
        
        return found
    
    def _find_dictionary_words(self, password):
        """Find dictionary words in password."""
        common_words = [
            'password', 'admin', 'user', 'login', 'welcome',
            'hello', 'world', 'test', 'demo', 'sample'
        ]
        
        found_words = []
        for word in common_words:
            if word.lower() in password.lower():
                found_words.append(word)
        
        return found_words
    
    def _contains_personal_info(self, password):
        """Check if password contains personal information."""
        # This would typically check against user data
        # For demo, check for common personal patterns
        personal_patterns = [
            r'\d{4}',  # Years
            r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)',  # Months
            r'(monday|tuesday|wednesday|thursday|friday|saturday|sunday)'  # Days
        ]
        
        for pattern in personal_patterns:
            if re.search(pattern, password.lower()):
                return True
        
        return False
    
    def _check_pwned_passwords(self, password):
        """Check against Have I Been Pwned database (simulated)."""
        # In real implementation, this would check against HIBP API
        # For demo, simulate based on common passwords
        return password.lower() in self.common_passwords
    
    def _meets_basic_requirements(self, password):
        """Check if password meets basic requirements."""
        requirements = {
            'min_length': len(password) >= 8,
            'has_uppercase': bool(re.search(r'[A-Z]', password)),
            'has_lowercase': bool(re.search(r'[a-z]', password)),
            'has_digit': bool(re.search(r'\d', password)),
            'has_special': bool(re.search(r'[^a-zA-Z0-9]', password))
        }
        
        requirements['all_met'] = all(requirements.values())
        return requirements
    
    def _calculate_strength_score(self, analysis):
        """Calculate overall strength score (0-100)."""
        score = 0
        
        # Length score (0-25 points)
        length = analysis['length']
        if length >= 12:
            score += 25
        elif length >= 8:
            score += 15
        elif length >= 6:
            score += 10
        elif length >= 4:
            score += 5
        
        # Character diversity (0-25 points)
        char_types = sum([
            analysis['character_analysis']['has_lowercase'],
            analysis['character_analysis']['has_uppercase'],
            analysis['character_analysis']['has_digits'],
            analysis['character_analysis']['has_special']
        ])
        score += char_types * 6.25
        
        # Entropy bonus (0-20 points)
        entropy = analysis['entropy']
        if entropy >= 60:
            score += 20
        elif entropy >= 40:
            score += 15
        elif entropy >= 25:
            score += 10
        elif entropy >= 15:
            score += 5
        
        # Security checks (0-30 points)
        if not analysis['security_checks']['is_common']:
            score += 10
        if not analysis['security_checks']['pwned_check']:
            score += 10
        if analysis['security_checks']['meets_basic_requirements']['all_met']:
            score += 10
        
        # Penalties
        if analysis['pattern_analysis']['repeated_chars']:
            score -= 5
        if analysis['pattern_analysis']['sequential']:
            score -= 10
        if analysis['pattern_analysis']['keyboard_patterns']:
            score -= 10
        if analysis['pattern_analysis']['dictionary_words']:
            score -= 15
        
        return max(0, min(100, round(score)))
    
    def _get_strength_level(self, score):
        """Get strength level based on score."""
        if score >= 80:
            return 'Very Strong'
        elif score >= 60:
            return 'Strong'
        elif score >= 40:
            return 'Moderate'
        elif score >= 20:
            return 'Weak'
        else:
            return 'Very Weak'
    
    def _get_recommendations(self, analysis):
        """Get improvement recommendations."""
        recommendations = []
        
        if analysis['length'] < 8:
            recommendations.append('Use at least 8 characters')
        elif analysis['length'] < 12:
            recommendations.append('Consider using 12+ characters for better security')
        
        char_analysis = analysis['character_analysis']
        if not char_analysis['has_uppercase']:
            recommendations.append('Add uppercase letters')
        if not char_analysis['has_lowercase']:
            recommendations.append('Add lowercase letters')
        if not char_analysis['has_digits']:
            recommendations.append('Add numbers')
        if not char_analysis['has_special']:
            recommendations.append('Add special characters (!@#$%^&*)')
        
        if analysis['security_checks']['is_common']:
            recommendations.append('Avoid common passwords')
        
        if analysis['pattern_analysis']['repeated_chars']:
            recommendations.append('Avoid repeated characters')
        
        if analysis['pattern_analysis']['sequential']:
            recommendations.append('Avoid sequential patterns (abc, 123)')
        
        if analysis['pattern_analysis']['keyboard_patterns']:
            recommendations.append('Avoid keyboard patterns (qwerty, asdf)')
        
        if analysis['pattern_analysis']['dictionary_words']:
            recommendations.append('Avoid dictionary words')
        
        if not recommendations:
            recommendations.append('Excellent password! Consider changing it regularly.')
        
        return recommendations

analyzer = PasswordAnalyzer()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Strength Analyzer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .analyzer-form {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .password-input {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 18px;
            margin-bottom: 20px;
        }
        
        .strength-meter {
            height: 10px;
            background: #e0e0e0;
            border-radius: 5px;
            margin-bottom: 10px;
            overflow: hidden;
        }
        
        .strength-fill {
            height: 100%;
            transition: width 0.3s ease, background-color 0.3s ease;
            border-radius: 5px;
        }
        
        .strength-very-weak { background: #e74c3c; }
        .strength-weak { background: #f39c12; }
        .strength-moderate { background: #f1c40f; }
        .strength-strong { background: #2ecc71; }
        .strength-very-strong { background: #27ae60; }
        
        .results {
            display: none;
        }
        
        .results-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-top: 20px;
        }
        
        .analysis-section {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .metric {
            display: flex;
            justify-content: between;
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .metric:last-child {
            border-bottom: none;
        }
        
        .metric-label {
            font-weight: 600;
        }
        
        .metric-value {
            color: #666;
        }
        
        .recommendations {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
        }
        
        .recommendation-item {
            margin: 8px 0;
            padding-left: 20px;
            position: relative;
        }
        
        .recommendation-item:before {
            content: '•';
            position: absolute;
            left: 0;
            color: #f39c12;
            font-weight: bold;
        }
        
        .pattern-warning {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 8px;
            padding: 10px;
            margin: 5px 0;
            color: #721c24;
        }
        
        .security-check {
            display: flex;
            justify-content: between;
            align-items: center;
            padding: 8px 0;
        }
        
        .check-pass { color: #27ae60; }
        .check-fail { color: #e74c3c; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐 Password Strength Analyzer</h1>
            <p>Advanced password security analysis and strength testing</p>
        </div>
        
        <div class="analyzer-form">
            <input type="password" id="passwordInput" class="password-input" placeholder="Enter password to analyze..." oninput="analyzePassword()">
            
            <div class="strength-meter">
                <div id="strengthFill" class="strength-fill" style="width: 0%;"></div>
            </div>
            
            <div id="strengthLabel" style="text-align: center; font-weight: 600; margin-bottom: 20px;">
                Enter a password to see analysis
            </div>
            
            <button onclick="generatePassword()" style="background: #667eea; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">
                🎲 Generate Secure Password
            </button>
        </div>
        
        <div id="results" class="results">
            <div class="results-grid">
                <div class="analysis-section">
                    <h3>📊 Password Analysis</h3>
                    <div id="basicMetrics"></div>
                    
                    <h4 style="margin-top: 20px;">🔍 Character Composition</h4>
                    <div id="characterAnalysis"></div>
                </div>
                
                <div class="analysis-section">
                    <h3>🛡️ Security Checks</h3>
                    <div id="securityChecks"></div>
                    
                    <h4 style="margin-top: 20px;">⚠️ Pattern Analysis</h4>
                    <div id="patternAnalysis"></div>
                </div>
            </div>
            
            <div class="recommendations" id="recommendations">
                <h3>💡 Recommendations</h3>
                <div id="recommendationsList"></div>
            </div>
        </div>
    </div>

    <script>
        let analysisTimeout;
        
        function analyzePassword() {
            const password = document.getElementById('passwordInput').value;
            
            // Clear previous timeout
            clearTimeout(analysisTimeout);
            
            if (!password) {
                hideResults();
                return;
            }
            
            // Debounce analysis
            analysisTimeout = setTimeout(() => {
                performAnalysis(password);
            }, 300);
        }
        
        async function performAnalysis(password) {
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ password: password })
                });
                
                const analysis = await response.json();
                displayResults(analysis);
                
            } catch (error) {
                console.error('Error:', error);
            }
        }
        
        function displayResults(analysis) {
            updateStrengthMeter(analysis.strength_score, analysis.strength_level);
            
            // Basic metrics
            document.getElementById('basicMetrics').innerHTML = `
                <div class="metric">
                    <span class="metric-label">Length:</span>
                    <span class="metric-value">${analysis.length} characters</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Entropy:</span>
                    <span class="metric-value">${analysis.entropy} bits</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Crack Time:</span>
                    <span class="metric-value">${analysis.crack_time}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Unique Characters:</span>
                    <span class="metric-value">${analysis.character_analysis.unique_chars}</span>
                </div>
            `;
            
            // Character analysis
            const charAnalysis = analysis.character_analysis;
            document.getElementById('characterAnalysis').innerHTML = `
                <div class="metric">
                    <span class="metric-label">Lowercase:</span>
                    <span class="metric-value ${charAnalysis.has_lowercase ? 'check-pass' : 'check-fail'}">
                        ${charAnalysis.lowercase} ${charAnalysis.has_lowercase ? '✓' : '✗'}
                    </span>
                </div>
                <div class="metric">
                    <span class="metric-label">Uppercase:</span>
                    <span class="metric-value ${charAnalysis.has_uppercase ? 'check-pass' : 'check-fail'}">
                        ${charAnalysis.uppercase} ${charAnalysis.has_uppercase ? '✓' : '✗'}
                    </span>
                </div>
                <div class="metric">
                    <span class="metric-label">Digits:</span>
                    <span class="metric-value ${charAnalysis.has_digits ? 'check-pass' : 'check-fail'}">
                        ${charAnalysis.digits} ${charAnalysis.has_digits ? '✓' : '✗'}
                    </span>
                </div>
                <div class="metric">
                    <span class="metric-label">Special Characters:</span>
                    <span class="metric-value ${charAnalysis.has_special ? 'check-pass' : 'check-fail'}">
                        ${charAnalysis.special} ${charAnalysis.has_special ? '✓' : '✗'}
                    </span>
                </div>
            `;
            
            // Security checks
            const securityChecks = analysis.security_checks;
            document.getElementById('securityChecks').innerHTML = `
                <div class="security-check">
                    <span>Common Password:</span>
                    <span class="${securityChecks.is_common ? 'check-fail' : 'check-pass'}">
                        ${securityChecks.is_common ? '✗ Yes' : '✓ No'}
                    </span>
                </div>
                <div class="security-check">
                    <span>Previously Breached:</span>
                    <span class="${securityChecks.pwned_check ? 'check-fail' : 'check-pass'}">
                        ${securityChecks.pwned_check ? '✗ Yes' : '✓ No'}
                    </span>
                </div>
                <div class="security-check">
                    <span>Basic Requirements:</span>
                    <span class="${securityChecks.meets_basic_requirements.all_met ? 'check-pass' : 'check-fail'}">
                        ${securityChecks.meets_basic_requirements.all_met ? '✓ Met' : '✗ Not Met'}
                    </span>
                </div>
            `;
            
            // Pattern analysis
            const patterns = analysis.pattern_analysis;
            let patternHtml = '';
            
            if (patterns.repeated_chars.length > 0) {
                patternHtml += `<div class="pattern-warning">Repeated characters: ${patterns.repeated_chars.join(', ')}</div>`;
            }
            if (patterns.sequential.length > 0) {
                patternHtml += `<div class="pattern-warning">Sequential patterns: ${patterns.sequential.join(', ')}</div>`;
            }
            if (patterns.keyboard_patterns.length > 0) {
                patternHtml += `<div class="pattern-warning">Keyboard patterns: ${patterns.keyboard_patterns.join(', ')}</div>`;
            }
            if (patterns.dictionary_words.length > 0) {
                patternHtml += `<div class="pattern-warning">Dictionary words: ${patterns.dictionary_words.join(', ')}</div>`;
            }
            
            if (!patternHtml) {
                patternHtml = '<div style="color: #27ae60;">✓ No problematic patterns detected</div>';
            }
            
            document.getElementById('patternAnalysis').innerHTML = patternHtml;
            
            // Recommendations
            document.getElementById('recommendationsList').innerHTML = 
                analysis.recommendations.map(rec => `<div class="recommendation-item">${rec}</div>`).join('');
            
            document.getElementById('results').style.display = 'block';
        }
        
        function updateStrengthMeter(score, level) {
            const fill = document.getElementById('strengthFill');
            const label = document.getElementById('strengthLabel');
            
            fill.style.width = score + '%';
            fill.className = 'strength-fill strength-' + level.toLowerCase().replace(' ', '-');
            label.textContent = `${level} (${score}/100)`;
        }
        
        function hideResults() {
            document.getElementById('results').style.display = 'none';
            document.getElementById('strengthFill').style.width = '0%';
            document.getElementById('strengthLabel').textContent = 'Enter a password to see analysis';
        }
        
        function generatePassword() {
            const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';
            let password = '';
            
            // Ensure at least one of each type
            password += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[Math.floor(Math.random() * 26)];
            password += 'abcdefghijklmnopqrstuvwxyz'[Math.floor(Math.random() * 26)];
            password += '0123456789'[Math.floor(Math.random() * 10)];
            password += '!@#$%^&*'[Math.floor(Math.random() * 8)];
            
            // Fill remaining length
            for (let i = 4; i < 16; i++) {
                password += chars[Math.floor(Math.random() * chars.length)];
            }
            
            // Shuffle password
            password = password.split('').sort(() => Math.random() - 0.5).join('');
            
            document.getElementById('passwordInput').value = password;
            analyzePassword();
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main analyzer page."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze_password():
    """Analyze password strength."""
    data = request.get_json()
    password = data.get('password', '')
    
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    
    analysis = analyzer.analyze_password(password)
    
    # Remove the actual password from response for security
    analysis['password'] = '*' * len(password)
    
    return jsonify(analysis)

def main():
    """Main execution function."""
    print("Password Strength Analyzer")
    print("=" * 30)
    
    print("Starting web server...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()

