import re
from datetime import datetime
from typing import Dict, List, Tuple

class GitAnalyzer:
    def __init__(self):
        self.risk_patterns = {
            'high': [
                r'password\s*=\s*[\'"].*[\'"]',
                r'api_key\s*=\s*[\'"].*[\'"]',
                r'DROP\s+TABLE',
                r'rm\s+-rf',
            ],
            'medium': [
                r'TODO',
                r'FIXME',
                r'hack',
                r'workaround',
            ],
            'low': [
                r'print\(',
                r'console\.log',
                r'DEBUG',
            ]
        }
        self.commit_metrics = {}

    def analyze_commit(self, commit_hash: str, commit_data: Dict) -> Dict:
        """Analyzes a single commit for various risk factors and patterns."""
        risk_score = 0
        findings = []

        # Analyze commit message
        message = commit_data.get('message', '')
        files_changed = commit_data.get('files_changed', [])
        lines_changed = commit_data.get('lines_changed', 0)
        author = commit_data.get('author', '')
        timestamp = commit_data.get('timestamp', '')

        # Pattern detection in changed code
        for file_diff in files_changed:
            for severity, patterns in self.risk_patterns.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, file_diff, re.IGNORECASE)
                    for match in matches:
                        risk_factor = {
                            'high': 10,
                            'medium': 5,
                            'low': 2
                        }[severity]
                        risk_score += risk_factor
                        findings.append({
                            'severity': severity,
                            'pattern': pattern,
                            'match': match.group(),
                            'file': file_diff[:50] + '...'
                        })

        # Time-based risk factors
        commit_time = datetime.fromisoformat(timestamp)
        if commit_time.hour < 5 or commit_time.hour > 22:  # Late night commits
            risk_score += 3
            findings.append({
                'severity': 'medium',
                'type': 'time_based',
                'detail': f'Commit made at unusual hour: {commit_time.hour}:00'
            })

        # Size-based risk factors
        if lines_changed > 500:
            risk_score += 5
            findings.append({
                'severity': 'medium',
                'type': 'size_based',
                'detail': f'Large commit: {lines_changed} lines changed'
            })

        # Store metrics for trend analysis
        self.commit_metrics[commit_hash] = {
            'risk_score': risk_score,
            'findings': findings,
            'timestamp': timestamp,
            'author': author,
            'lines_changed': lines_changed
        }

        return {
            'commit_hash': commit_hash,
            'risk_score': risk_score,
            'findings': findings,
            'analysis_summary': self._generate_summary(risk_score, findings)
        }

    def analyze_trends(self) -> Dict:
        """Analyzes patterns and trends across multiple commits."""
        if not self.commit_metrics:
            return {'error': 'No commit data available for trend analysis'}

        author_risks = {}
        total_risk = 0
        high_risk_commits = []

        for commit_hash, metrics in self.commit_metrics.items():
            author = metrics['author']
            risk_score = metrics['risk_score']
            
            # Track per-author metrics
            if author not in author_risks:
                author_risks[author] = {'total_score': 0, 'commit_count': 0}
            author_risks[author]['total_score'] += risk_score
            author_risks[author]['commit_count'] += 1

            total_risk += risk_score
            if risk_score > 20:
                high_risk_commits.append(commit_hash)

        # Calculate average risks and identify concerning patterns
        avg_risk = total_risk / len(self.commit_metrics) if self.commit_metrics else 0
        author_avg_risks = {
            author: data['total_score'] / data['commit_count']
            for author, data in author_risks.items()
        }

        return {
            'average_risk_score': avg_risk,
            'high_risk_commits': high_risk_commits,
            'author_risk_profiles': author_avg_risks,
            'total_commits_analyzed': len(self.commit_metrics)
        }

    def _generate_summary(self, risk_score: int, findings: List[Dict]) -> str:
        """Generates a human-readable summary of the analysis."""
        severity_counts = {'high': 0, 'medium': 0, 'low': 0}
        for finding in findings:
            if 'severity' in finding:
                severity_counts[finding['severity']] += 1

        summary = f'Risk Score: {risk_score}\n'
        summary += f'Findings: {len(findings)} total\n'
        summary += f'High: {severity_counts["high"]} '
        summary += f'Medium: {severity_counts["medium"]} '
        summary += f'Low: {severity_counts["low"]}\n'

        if risk_score > 20:
            summary += 'WARNING: High risk commit detected!\n'
        elif risk_score > 10:
            summary += 'NOTICE: Moderate risk level detected.\n'

        return summary