"""
Analyseur IA pour les alertes Wazuh.
Utilise Ollama (IA locale) pour analyser les alertes de sécurité.
"""

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("⚠️ Ollama n'est pas installé. Installez-le avec: pip install ollama")


class AlertAnalyzer:
    """Analyse les alertes Wazuh avec l'IA."""

    def __init__(self, model="llama3.2"):
        """
        Initialise l'analyseur IA.

        Args:
            model: Nom du modèle Ollama à utiliser
        """
        if not OLLAMA_AVAILABLE:
            raise RuntimeError("La bibliothèque ollama n'est pas installée")

        self.model = model

    def analyze_alert(self, alert_data):
        """
        Analyse une alerte avec l'IA.

        Args:
            alert_data: Dictionnaire contenant les données de l'alerte

        Returns:
            dict: Analyse structurée avec gravité, explications et recommandations
        """
        # Extraire les informations clés de l'alerte
        rule_description = alert_data.get('rule', {}).get('description', 'N/A')
        rule_level = alert_data.get('rule', {}).get('level', 0)
        agent_name = alert_data.get('agent', {}).get('name', 'N/A')

        # Construire le prompt pour l'IA
        prompt = f"""Tu es un expert en cybersécurité. Analyse cette alerte Wazuh:

Alerte: {rule_description}
Niveau: {rule_level}/15
Agent: {agent_name}

Reponds UNIQUEMENT avec un objet JSON valide, sans texte avant ou apres. Structure exacte:
{{
  "severity": "low",
  "explanation": "explication courte en 1 phrase",
  "recommendations": ["action 1", "action 2"],
  "is_false_positive": false
}}"""

        try:
            # Appel à l'IA Ollama
            response = ollama.chat(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Extraire la réponse
            ai_response = response['message']['content']

            # Nettoyer la réponse (enlever markdown potentiel)
            ai_response = ai_response.strip()
            if ai_response.startswith('```json'):
                ai_response = ai_response[7:]  # Enlever ```json
            if ai_response.startswith('```'):
                ai_response = ai_response[3:]  # Enlever ```
            if ai_response.endswith('```'):
                ai_response = ai_response[:-3]  # Enlever ```
            ai_response = ai_response.strip()

            # Parser le JSON (l'IA devrait renvoyer du JSON)
            import json
            analysis = json.loads(ai_response)

            return analysis

        except Exception as e:
            # En cas d'erreur, renvoyer une analyse basique
            return {
                "severity": self._map_level_to_severity(rule_level),
                "explanation": f"Erreur d'analyse IA: {str(e)}",
                "recommendations": ["Vérifier manuellement cette alerte"],
                "is_false_positive": False
            }

    def _map_level_to_severity(self, level):
        """Convertit le niveau Wazuh en gravité."""
        if level >= 12:
            return "critical"
        elif level >= 8:
            return "high"
        elif level >= 4:
            return "medium"
        else:
            return "low"


# Test de l'analyseur
if __name__ == "__main__":
    if not OLLAMA_AVAILABLE:
        print("❌ Ollama non disponible. Installez-le avec:")
        print("   pip install ollama")
        print("\nPuis téléchargez un modèle:")
        print("   ollama pull llama3.2")
    else:
        # Exemple d'alerte fictive
        fake_alert = {
            "rule": {
                "description": "Multiple failed login attempts",
                "level": 5
            },
            "agent": {
                "name": "Windows-PC"
            }
        }

        analyzer = AlertAnalyzer()
        print("[IA] Test de l'analyseur IA...")
        result = analyzer.analyze_alert(fake_alert)

        print("\n[RESULTAT]")
        print(f"  Gravite: {result['severity']}")
        print(f"  Explication: {result['explanation']}")
        print(f"  Recommandations:")
        for rec in result['recommendations']:
            print(f"    - {rec}")
        print(f"  Faux positif: {result['is_false_positive']}")
