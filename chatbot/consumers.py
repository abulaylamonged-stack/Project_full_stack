# chatbot/consumers.py // c'est ici qu'on travaille l'intelligence du chatbot 
import json
import re
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        if self.channel_layer is not None:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        
        await self.accept()
        
        # Message de bienvenue personnalisé
        await self.send(text_data=json.dumps({
            'message': '👋 Bonjour ! Je suis votre assistant spécialisé en sécurité réseau et analyse de fichiers .cap. Posez-moi vos questions !'
        }))
    
    async def disconnect(self, close_code):
        if self.channel_layer is not None:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '').lower()
        
        # Appeler la fonction de réponse intelligente
        response = await self.get_intelligent_response(message)
        
        if self.channel_layer is not None:
            await self.channel_layer.group_send(
                self.room_group_name,
                {'type': 'chat_message', 'message': response}
            )
        else:
            await self.send(text_data=json.dumps({'message': response}))
    
    async def get_intelligent_response(self, message):
        """Génère une réponse intelligente basée sur le message"""
        
        # ========== SALUTATIONS ==========
        if re.search(r'\b(bonjour|salut|coucou|hello|hi|hey)\b', message):
            return "👋 Bonjour ! Comment puis-je vous aider avec l'analyse de fichiers .cap ou la sécurité réseau aujourd'hui ?"
        
        # ========== AUDIT DE SÉCURITÉ ==========
        if re.search(r'audit de s[ée]curit[ée]', message):
            return """🔒 **Audit de sécurité réseau** : 
Un audit de sécurité consiste à évaluer la vulnérabilité d'un système ou d'un réseau informatique. Cela comprend :
- L'analyse des flux réseau (fichiers .cap)
- La détection d'intrusions
- L'identification des failles de sécurité
- L'évaluation des politiques de sécurité

Avec vos fichiers .cap, je peux vous aider à analyser le trafic et détecter des anomalies !"""
        
        # ========== FICHIERS .CAP ==========
        if re.search(r'\.cap|fichier .cap|capture', message):
            return """📁 **Fichiers .cap** : 
Ce sont des fichiers de capture réseau (Wireshark/tcpdump). Ils contiennent les paquets réseau échangés.
Je peux analyser ces fichiers pour :
- Identifier les protocoles utilisés (TCP, UDP, HTTP, etc.)
- Détecter des attaques (ARP spoofing, DoS, etc.)
- Analyser les conversations réseau
- Extraire des statistiques de trafic

Uploader un fichier .cap et posez-moi des questions dessus !"""
        
        # ========== WIRESHARK ==========
        if re.search(r'wireshark', message):
            return """🦈 **Wireshark** : 
Wireshark est l'outil standard pour l'analyse de paquets réseau. Avec Wireshark, vous pouvez :
- Capturer du trafic en temps réel
- Analyser des fichiers .cap
- Filtrer les paquets (ex: `tcp.port == 80`)
- Suivre des flux TCP
- Détecter des anomalies réseau

Vous pouvez exporter vos captures en .cap et me les envoyer pour analyse !"""
        
        # ========== ATTAQUES RÉSEAU ==========
        if re.search(r'(attaque|ddos|dos|arp spoof|syn flood)', message):
            return """⚠️ **Attaques réseau courantes** :
- **DDoS/DoS** : Surcharge du serveur par des requêtes multiples
- **ARP Spoofing** : Usurpation d'adresse MAC
- **SYN Flood** : Saturation des connexions TCP
- **Man-in-the-Middle** : Interception des communications
- **Scan de ports** : Détection des services ouverts

Avec un fichier .cap, je peux vous aider à détecter ces attaques !"""
        
        # ========== PROTOCOLES ==========
        if re.search(r'(tcp|udp|http|https|dns|dhcp|arp)', message):
            return """🌐 **Protocoles réseau** :
- **TCP** : Connexion fiable (HTTP, HTTPS, SSH, FTP)
- **UDP** : Connexion rapide (DNS, DHCP, streaming)
- **HTTP/HTTPS** : Navigation web
- **DNS** : Résolution de noms de domaine
- **ARP** : Association IP ↔ MAC
- **DHCP** : Attribution automatique d'IP

Je peux analyser ces protocoles dans vos fichiers .cap !"""
        
        # ========== ANALYSE DE FICHIER ==========
        if re.search(r'analyse|analyser|examiner|vérifier', message):
            return "🔍 Pour analyser un fichier .cap, uploadez-le via le bouton '📁 Upload .cap' dans le chat. Je pourrai alors extraire des informations comme : les adresses IP, les ports, les protocoles, et détecter d'éventuelles anomalies."
        
        # ========== AIDE ==========
        if re.search(r'aide|help|que peux-tu faire|commande', message):
            return """💡 **Ce que je peux faire pour vous** :
1. Répondre à vos questions sur la sécurité réseau
2. Analyser des fichiers .cap (upload)
3. Détecter des attaques réseau
4. Expliquer les protocoles (TCP, UDP, HTTP, etc.)
5. Vous aider à comprendre Wireshark

Posez-moi vos questions ou uploadez un fichier .cap !"""
        
        # ========== REMERCIEMENTS ==========
        if re.search(r'merci|thanks|super|génial', message):
            return "Avec plaisir ! N'hésitez pas si vous avez d'autres questions sur vos fichiers .cap ou la sécurité réseau. 😊"
        
        # ========== RÉPONSE PAR DÉFAUT ==========
        return f"🤔 Je n'ai pas bien compris votre question sur : '{message}'. Voici ce que je peux faire :\n- Répondre sur l'audit de sécurité\n- Analyser vos fichiers .cap\n- Expliquer les protocoles réseau\n- Détecter des attaques\n\nPouvez-vous reformuler votre question ?"
    
    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))