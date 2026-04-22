# analyzer/views.py - Version avec debug amélioré
import os
import tempfile
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .pcap_analyzer import analyze_pcap_file
from .chart_generator import generate_analysis_chart

def index(request):
    """Page d'accueil"""
    return render(request, 'Analyser/index.html')

@csrf_exempt
@require_http_methods(["POST"])
def upload_and_analyze(request):
    """Upload et analyse - Version avec debug"""
    try:
        print("=" * 50)
        print("📥 REQUÊTE REÇUE")
        print("=" * 50)
        
        # Vérifier si le fichier est présent
        if 'file' not in request.FILES:
            print("❌ Aucun fichier dans la requête")
            return JsonResponse({'error': 'Aucun fichier sélectionné'}, status=400)
        
        uploaded_file = request.FILES['file']
        print(f"📁 Fichier: {uploaded_file.name}")
        print(f"📏 Taille: {uploaded_file.size} bytes")
        print(f"🔤 Type: {uploaded_file.content_type}")
        
        # Sauvegarder le fichier temporairement
        print("💾 Sauvegarde du fichier temporaire...")
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pcap') as tmp_file:
            for chunk in uploaded_file.chunks():
                tmp_file.write(chunk)
            tmp_path = tmp_file.name
        
        print(f"✅ Fichier sauvegardé: {tmp_path}")
        
        # Analyser avec le modèle ML
        print("🤖 Lancement de l'analyse ML...")
        results = analyze_pcap_file(tmp_path, uploaded_file.name)
        
        print(f"✅ Analyse terminée!")
        print(f"   - Paquets: {results.get('total_packets', 0)}")
        print(f"   - Vulnérabilités: {len(results.get('vulnerabilities', []))}")
        print(f"   - Score sécurité: {results.get('security_score', 0)}")
        
        # Générer le graphique
        print("📊 Génération du graphique...")
        chart_image = generate_analysis_chart(results)
        if chart_image:
            results['chart_image'] = chart_image
            print("✅ Graphique généré")
        else:
            print("⚠️ Pas de graphique généré")
        
        # Nettoyer le fichier temporaire
        os.unlink(tmp_path)
        print("🗑️ Fichier temporaire supprimé")
        
        # Retourner la réponse
        response_data = {
            'success': True, 
            'results': results
        }
        
        print("📤 Envoi de la réponse JSON")
        print("=" * 50)
        
        return JsonResponse(response_data)
        
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)