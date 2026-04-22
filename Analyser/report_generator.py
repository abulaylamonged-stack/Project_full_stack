# analyzer/report_generator.py
import json
import pdfkit
from datetime import datetime
from jinja2 import Template
import markdown

class ReportGenerator:
    """Génère des rapports professionnels au format HTML, PDF et JSON"""
    
    def __init__(self, analysis_results):
        self.results = analysis_results
        self.vulnerabilities = analysis_results.get('vulnerabilities', [])
    
    def generate_html_report(self):
        """Génère un rapport HTML détaillé"""
        template = Template('''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport d'Analyse Sécurité - {{ results.filename }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f0f2f5;
            padding: 40px;
            color: #1a1a2e;
        }
        
        .report-container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header .subtitle {
            opacity: 0.9;
            margin-top: 10px;
        }
        
        .content {
            padding: 40px;
        }
        
        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            transition: transform 0.3s;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card .number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .security-score {
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            margin-bottom: 30px;
            color: white;
        }
        
        .score-value {
            font-size: 4em;
            font-weight: bold;
        }
        
        .vulnerability-item {
            border-left: 4px solid;
            padding: 15px;
            margin: 15px 0;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .severity-Critical { border-color: #dc3545; background: #fff5f5; }
        .severity-High { border-color: #fd7e14; background: #fff8f0; }
        .severity-Medium { border-color: #ffc107; background: #fffcf0; }
        .severity-Low { border-color: #28a745; background: #f0fff4; }
        
        .vuln-title {
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 10px;
        }
        
        .vuln-description {
            margin: 10px 0;
            color: #555;
        }
        
        .vuln-recommendation {
            background: #e7f3ff;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
            font-size: 0.9em;
        }
        
        .cvss-badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
            margin-left: 10px;
        }
        
        .cvss-critical { background: #dc3545; color: white; }
        .cvss-high { background: #fd7e14; color: white; }
        .cvss-medium { background: #ffc107; color: #333; }
        
        .chart-container {
            margin: 30px 0;
            text-align: center;
        }
        
        .chart-container img {
            max-width: 100%;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }
        
        @media print {
            body {
                padding: 0;
                background: white;
            }
            .no-print {
                display: none;
            }
        }
        
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px;
        }
        
        button:hover {
            background: #764ba2;
        }
    </style>
</head>
<body>
    <div class="report-container">
        <div class="header">
            <h1>🔒 Rapport d'Analyse de Sécurité Réseau</h1>
            <div class="subtitle">
                Généré le {{ generation_date }}<br>
                Fichier analysé: {{ results.filename }}
            </div>
        </div>
        
        <div class="content">
            <div class="summary-cards">
                <div class="card">
                    <div class="number">{{ results.total_packets }}</div>
                    <div>Paquets analysés</div>
                </div>
                <div class="card">
                    <div class="number">{{ "%.2f"|format(results.total_bytes / 1024 / 1024) }} MB</div>
                    <div>Volume total</div>
                </div>
                <div class="card">
                    <div class="number">{{ results.duration }}s</div>
                    <div>Durée capture</div>
                </div>
                <div class="card">
                    <div class="number">{{ vulnerabilities|length }}</div>
                    <div>Vulnérabilités</div>
                </div>
            </div>
            
            <div class="security-score">
                <div class="score-value">{{ results.security_score }}/100</div>
                <div style="font-size: 1.2em; margin-top: 10px;">
                    Niveau: {{ results.security_level }}
                </div>
                <div class="subtitle" style="margin-top: 10px;">
                    Score de sécurité global
                </div>
            </div>
            
            {% if results.chart_image %}
            <div class="chart-container">
                <h3>📊 Visualisation des données</h3>
                <img src="{{ results.chart_image }}" alt="Graphique d'analyse">
            </div>
            {% endif %}
            
            <h2>🛡️ Vulnérabilités Détectées</h2>
            
            {% if vulnerabilities %}
                {% for vuln in vulnerabilities %}
                <div class="vulnerability-item severity-{{ vuln.severity }}">
                    <div class="vuln-title">
                        {{ vuln.type }}
                        <span class="cvss-badge cvss-{{ vuln.severity|lower }}">
                            CVSS: {{ vuln.get('cvss_score', 'N/A') }}
                        </span>
                        <span style="float: right;">{{ vuln.severity }}</span>
                    </div>
                    <div class="vuln-description">
                        {{ vuln.description }}
                    </div>
                    <div class="vuln-recommendation">
                        <strong>🔧 Recommandation:</strong> {{ vuln.recommendation }}
                    </div>
                </div>
                {% endfor %}
            {% else %}
                <div style="text-align: center; padding: 40px; background: #d4edda; border-radius: 10px;">
                    <span style="font-size: 3em;">✅</span>
                    <h3>Aucune vulnérabilité détectée</h3>
                    <p>Votre réseau semble sécurisé !</p>
                </div>
            {% endif %}
            
            <h2 style="margin-top: 30px;">📈 Statistiques détaillées</h2>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
                <div>
                    <h3>Top Protocoles</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        {% for proto, percent in results.protocols.items() %}
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{{ proto }}</td>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right;">{{ percent }}%</td>
                        </tr>
                        {% endfor %}
                    </table>
                </div>
                <div>
                    <h3>Top Ports Destination</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        {% for port, count in results.top_ports.items() %}
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;">Port {{ port }}</td>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right;">{{ count }} connexions</td>
                        </tr>
                        {% endfor %}
                    </table>
                </div>
            </div>
            
            <h2 style="margin-top: 30px;">🌐 Top IPs Sources</h2>
            <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                {% for ip, count in results.top_ips.items() %}
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #ddd;">{{ ip }}</td>
                    <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right;">{{ count }} paquets</td>
                </tr>
                {% endfor %}
            </table>
        </div>
        
        <div class="footer">
            <p>Rapport généré automatiquement par SecuAnalyzer - Outil d'analyse de cybersécurité</p>
            <p>Ce rapport est confidentiel - À usage professionnel uniquement</p>
            <div class="no-print">
                <button onclick="window.print()">🖨️ Imprimer le rapport</button>
                <button onclick="downloadJSON()">📥 Télécharger (JSON)</button>
            </div>
        </div>
    </div>
    
    <script>
        function downloadJSON() {
            const data = {{ results_json|safe }};
            const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'security_report_{{ results.filename }}.json';
            a.click();
            URL.revokeObjectURL(url);
        }
    </script>
</body>
</html>
        ''')
        
        return template.render(
            results=self.results,
            vulnerabilities=self.vulnerabilities,
            generation_date=datetime.now().strftime('%d/%m/%Y à %H:%M:%S'),
            results_json=json.dumps(self.results, ensure_ascii=False)
        )
    
    def generate_json_report(self):
        """Génère un rapport JSON"""
        return json.dumps({
            'metadata': {
                'report_date': datetime.now().isoformat(),
                'tool': 'SecuAnalyzer',
                'version': '1.0.0'
            },
            'analysis': self.results,
            'summary': {
                'total_vulnerabilities': len(self.vulnerabilities),
                'critical_count': sum(1 for v in self.vulnerabilities if v['severity'] == 'Critical'),
                'high_count': sum(1 for v in self.vulnerabilities if v['severity'] == 'High'),
                'medium_count': sum(1 for v in self.vulnerabilities if v['severity'] == 'Medium'),
                'low_count': sum(1 for v in self.vulnerabilities if v['severity'] == 'Low'),
                'security_score': self.results.get('security_score', 0)
            }
        }, ensure_ascii=False, indent=2)
    
    def generate_markdown_report(self):
        """Génère un rapport Markdown"""
        md_content = f"""# Rapport d'Analyse de Sécurité Réseau

## Informations Générales
- **Fichier analysé:** {self.results['filename']}
- **Date d'analyse:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
- **Paquets analysés:** {self.results['total_packets']}
- **Volume total:** {self.results['total_bytes'] / 1024 / 1024:.2f} MB
- **Score de sécurité:** {self.results['security_score']}/100 ({self.results['security_level']})

## Vulnérabilités Détectées ({len(self.vulnerabilities)})

"""
        for vuln in self.vulnerabilities:
            md_content += f"""
### {vuln['type']} - **{vuln['severity']}**

**Description:** {vuln['description']}

**Recommandation:** {vuln['recommendation']}

---
"""
        
        return md_content
    
    def save_report(self, filename, format='html'):
        """Sauvegarde le rapport dans un fichier"""
        if format == 'html':
            content = self.generate_html_report()
            extension = '.html'
        elif format == 'json':
            content = self.generate_json_report()
            extension = '.json'
        elif format == 'md':
            content = self.generate_markdown_report()
            extension = '.md'
        else:
            raise ValueError(f"Format {format} non supporté")
        
        with open(filename + extension, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filename + extension