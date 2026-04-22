# test_ml_analyzer.py - À placer à la racine du projet Django
import sys
import os

# Ajouter le chemin du projet pour les imports
sys.path.insert(0, os.path.dirname(__file__))

# Importer l'analyseur ML
from Analyser.ml_vulnerability_analyzer import MLVulnerabilityAnalyzer

def test_ml_analyzer():
    """Test simple de l'analyseur ML"""
    print("=" * 60)
    print("🧪 TEST DE L'ANALYSEUR ML")
    print("=" * 60)
    
    # 1. Créer l'instance du modèle
    print("\n1️⃣ Initialisation du modèle...")
    analyzer = MLVulnerabilityAnalyzer()
    print("   ✅ Modèle chargé")
    
    # 2. Simuler des données réseau
    print("\n2️⃣ Simulation de données réseau...")
    test_data = {
        'total_packets': 1250,
        'packet_rate': 80.6,
        'top_ports': {443: 520, 80: 380, 445: 35, 3389: 45, 21: 20, 23: 5},
        'top_ips': {'192.168.1.100': 450, '192.168.1.1': 320, '10.0.0.5': 200},
        'protocols': {'TCP': 65, 'UDP': 22, 'ICMP': 8, 'DNS': 3, 'ARP': 2}
    }
    print("   ✅ Données simulées")
    
    # 3. Extraire les features
    print("\n3️⃣ Extraction des caractéristiques...")
    features = analyzer.extract_features(test_data)
    print("   📊 Features extraites:")
    for key, value in list(features.items())[:5]:  # Afficher les 5 premières
        print(f"      - {key}: {value}")
    
    # 4. Prédire les vulnérabilités
    print("\n4️⃣ Analyse par le modèle ML...")
    vulns, confidence = analyzer.predict_vulnerabilities(features, test_data)
    
    print(f"\n📈 RÉSULTATS DE L'ANALYSE:")
    print(f"   - Vulnérabilités détectées: {len(vulns)}")
    print(f"   - Confiance du modèle: {confidence*100:.1f}%")
    
    # 5. Afficher les détails
    if vulns:
        print("\n⚠️ VULNÉRABILITÉS DÉTECTÉES:")
        for i, vuln in enumerate(vulns, 1):
            print(f"\n   {i}. {vuln['type']}")
            print(f"      Sévérité: {vuln['severity']}")
            print(f"      Confiance ML: {vuln['confidence']}%")
            print(f"      Description: {vuln['description'][:80]}...")
    else:
        print("\n   ✅ Aucune vulnérabilité détectée")
    
    print("\n" + "=" * 60)
    print("✅ TEST TERMINÉ")
    print("=" * 60)

if __name__ == "__main__":
    test_ml_analyzer()