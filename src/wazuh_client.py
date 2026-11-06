
"""
Client pour interagir avec l'API Wazuh.
"""
import requests
import urllib3

# Désactiver les avertissements SSL (certificat auto-signé)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class WazuhClient:
    """Client pour l'API Wazuh."""

    def __init__(self, api_url: str, username: str, password: str):
        self.api_url = api_url.rstrip('/')
        self.username = username
        self.password = password
        self.token = None

    def authenticate(self):
        """S'authentifie et récupère un token JWT."""
        response = requests.post(
            f"{self.api_url}/security/user/authenticate",
            auth=(self.username, self.password),
            verify=False,
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        self.token = data['data']['token']
        return True

    def get_agents(self):
        """Récupère la liste des agents."""
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(
            f"{self.api_url}/agents",
            headers=headers,
            verify=False,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    def get_alerts(self, limit=100, offset=0, level_min=None):
        """Récupère les alertes récentes via l'indexer."""
        # Note: L'API Wazuh n'expose pas directement /alerts
        # Il faut passer par l'indexer Elasticsearch sur le port 9200
        # Pour l'instant, on renvoie un placeholder
        # TODO: Implémenter l'accès à l'indexer
        return {
            'data': {
                'affected_items': [],
                'total_affected_items': 0
            }
        }

    def get_vulnerabilities(self, agent_id, limit=500):
        """Récupère les vulnérabilités d'un agent."""
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"limit": limit, "sort": "-cvss.score"}

        response = requests.get(
            f"{self.api_url}/vulnerability/{agent_id}",
            headers=headers,
            params=params,
            verify=False,
            timeout=10
        )
        response.raise_for_status()
        return response.json()


# Test du client
if __name__ == "__main__":
    client = WazuhClient(
        "https://localhost:55000",
        "wazuh-wui",
        "MyS3cr37P450r.*-"
    )

    client.authenticate()
    agents = client.get_agents()

    print(f"\n📊 Agents connectés:")
    for agent in agents['data']['affected_items']:
        print(f"  - {agent['name']} (ID: {agent['id']}) - Status: {agent['status']}")