"""
SentinelAI - Analyseur d'alertes Wazuh avec IA
"""
from src.wazuh_client import WazuhClient
from src.alert_analyzer import AlertAnalyzer
from src.test_alerts import get_test_alerts


def main():
    print("=" * 60)
    print("SENTINEL AI - Analyse d'alertes Wazuh avec IA")
    print("=" * 60)

    # Configuration (a remplacer par .env plus tard)
    WAZUH_API_URL = "https://localhost:55000"
    WAZUH_USER = "wazuh-wui"
    WAZUH_PASSWORD = "MyS3cr37P450r.*-"

    # 1. Connexion a Wazuh
    print("\n[1/4] Connexion a Wazuh...")
    client = WazuhClient(WAZUH_API_URL, WAZUH_USER, WAZUH_PASSWORD)

    try:
        client.authenticate()
        print("  [OK] Authentification reussie")
    except Exception as e:
        print(f"  [ERREUR] {e}")
        return

    # 2. Recuperation des alertes recentes
    print("\n[2/4] Recuperation des alertes de test...")
    try:
        # Utilisation d'alertes de test pour le moment
        alerts = get_test_alerts()
        print(f"  [OK] {len(alerts)} alertes recuperees")
    except Exception as e:
        print(f"  [ERREUR] {e}")
        return

    if not alerts:
        print("\n  Aucune alerte trouvee. Tout va bien !")
        return

    # 3. Initialisation de l'analyseur IA
    print("\n[3/4] Initialisation de l'IA...")
    try:
        analyzer = AlertAnalyzer(model="llama3.2")
        print("  [OK] Modele llama3.2 pret")
    except Exception as e:
        print(f"  [ERREUR] {e}")
        return

    # 4. Analyse de chaque alerte
    print("\n[4/4] Analyse des alertes avec l'IA...")
    print("-" * 60)

    for i, alert in enumerate(alerts, 1):
        rule = alert.get('rule', {})
        agent = alert.get('agent', {})

        print(f"\n[ALERTE {i}/{len(alerts)}]")
        print(f"  Description: {rule.get('description', 'N/A')}")
        print(f"  Niveau: {rule.get('level', 0)}/15")
        print(f"  Agent: {agent.get('name', 'N/A')}")

        # Analyse IA
        print("  Analyse en cours...")
        analysis = analyzer.analyze_alert(alert)

        print(f"\n  [ANALYSE IA]")
        print(f"    Gravite: {analysis['severity'].upper()}")
        print(f"    Explication: {analysis['explanation']}")
        print(f"    Recommandations:")
        for rec in analysis['recommendations']:
            print(f"      - {rec}")
        print(f"    Faux positif probable: {'Oui' if analysis['is_false_positive'] else 'Non'}")
        print("-" * 60)

    print("\n[TERMINE] Analyse complete !")


if __name__ == "__main__":
    main()
