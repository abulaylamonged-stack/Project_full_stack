# analyzer/chart_generator.py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from collections import Counter

def generate_analysis_chart(results):
    """Génère des graphiques d'analyse incluant les métriques ML"""
    try:
        # Créer une figure avec plusieurs sous-graphiques
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle(f'Analyse Réseau - {results["filename"]}', fontsize=14, fontweight='bold')
        
        # 1. Distribution des protocoles (pie chart)
        ax1 = axes[0, 0]
        protocols = results['protocols']
        labels = list(protocols.keys())
        sizes = list(protocols.values())
        colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#6b7280']
        ax1.pie(sizes, labels=labels, colors=colors[:len(labels)], autopct='%1.1f%%', startangle=90)
        ax1.set_title('Distribution des protocoles', fontweight='bold')
        
        # 2. Top ports (bar chart)
        ax2 = axes[0, 1]
        top_ports = dict(list(results['top_ports'].items())[:10])
        ports = [str(p) for p in top_ports.keys()]
        counts = list(top_ports.values())
        colors_bar = ['#ef4444' if p in ['445', '3389', '21', '23'] else '#3b82f6' for p in top_ports.keys()]
        ax2.barh(ports, counts, color=colors_bar)
        ax2.set_xlabel('Nombre de paquets')
        ax2.set_title('Top 10 ports actifs', fontweight='bold')
        ax2.invert_yaxis()
        
        # 3. Score de sécurité avec jauge ML
        ax3 = axes[1, 0]
        security_score = results['security_score']
        colors_gauge = ['#ef4444', '#f59e0b', '#22c55e']
        ax3.pie([security_score, 100-security_score], 
                colors=[colors_gauge[2 if security_score >= 70 else 1 if security_score >= 40 else 0], '#e5e7eb'],
                startangle=90, counterclock=False)
        centre_circle = plt.Circle((0,0), 0.70, fc='white')
        ax3.add_artist(centre_circle)
        ax3.text(0, 0, f'{security_score}', ha='center', va='center', fontsize=28, fontweight='bold')
        ax3.text(0, -0.2, 'Score sécurité', ha='center', va='center', fontsize=10)
        ax3.set_title('Score de sécurité global', fontweight='bold')
        
        # 4. Confiance du modèle ML (bar chart)
        ax4 = axes[1, 1]
        if 'ml_confidence' in results:
            ml_confidence = results['ml_confidence']
            vulnerabilities = results.get('vulnerabilities', [])
            if vulnerabilities:
                ml_scores = [v.get('ml_score', 0) for v in vulnerabilities[:5]]
                vuln_names = [v['type'][:20] + '...' if len(v['type']) > 20 else v['type'] 
                             for v in vulnerabilities[:5]]
                
                y_pos = range(len(vuln_names))
                ax4.barh(y_pos, ml_scores, color='#8b5cf6')
                ax4.set_yticks(y_pos)
                ax4.set_yticklabels(vuln_names, fontsize=8)
                ax4.set_xlabel('Score de confiance ML (%)')
                ax4.set_title('Top vulnérabilités (analyse IA)', fontweight='bold')
                ax4.set_xlim(0, 100)
            else:
                ax4.text(0.5, 0.5, 'Aucune vulnérabilité\ndétectée par l\'IA', 
                        ha='center', va='center', transform=ax4.transAxes, fontsize=12)
                ax4.set_title('Résultats analyse IA', fontweight='bold')
        
        plt.tight_layout()
        
        # Convertir en base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
        
    except Exception as e:
        print(f"Erreur génération graphique: {e}")
        return None