"""
Alertes de test pour SentinelAI.
Basees sur de vraies alertes Wazuh pour tester l'analyseur IA.
"""


def get_test_alerts():
    """Renvoie des alertes de test realistes."""
    return [
        # Alerte 1: Connexion echouee (Event ID 4625)
        {
            "rule": {
                "id": "60105",
                "level": 5,
                "description": "Windows Logon Failure. Multiple failed login attempts."
            },
            "agent": {
                "id": "001",
                "name": "Windows-PC"
            },
            "data": {
                "win": {
                    "eventdata": {
                        "ipAddress": "192.168.1.50",
                        "logonType": "2",
                        "failureReason": "Bad password"
                    }
                }
            },
            "timestamp": "2026-11-06T16:00:00.000Z"
        },

        # Alerte 2: Vulnerabilite critique detectee
        {
            "rule": {
                "id": "23505",
                "level": 10,
                "description": "CVE-2019-15315 affects setuptools. Critical vulnerability detected."
            },
            "agent": {
                "id": "001",
                "name": "Windows-PC"
            },
            "data": {
                "vulnerability": {
                    "cve": "CVE-2019-15315",
                    "cvss": {
                        "score": 8.8
                    },
                    "package": {
                        "name": "setuptools",
                        "version": "40.8.0"
                    }
                }
            },
            "timestamp": "2026-11-06T15:30:00.000Z"
        },

        # Alerte 3: Processus suspect demarre
        {
            "rule": {
                "id": "61603",
                "level": 7,
                "description": "Suspicious process started. Possible malware execution."
            },
            "agent": {
                "id": "001",
                "name": "Windows-PC"
            },
            "data": {
                "win": {
                    "eventdata": {
                        "image": "C:\\Users\\Public\\temp123.exe",
                        "commandLine": "temp123.exe --download malicious.dll"
                    }
                }
            },
            "timestamp": "2026-11-06T16:15:00.000Z"
        },

        # Alerte 4: Modification de fichier systeme
        {
            "rule": {
                "id": "550",
                "level": 12,
                "description": "Integrity checksum changed. Critical system file modified."
            },
            "agent": {
                "id": "001",
                "name": "Windows-PC"
            },
            "data": {
                "syscheck": {
                    "path": "C:\\Windows\\System32\\cmd.exe",
                    "event": "modified",
                    "changed_attributes": ["size", "md5", "sha1"]
                }
            },
            "timestamp": "2026-11-06T14:00:00.000Z"
        },

        # Alerte 5: Scan de port detecte
        {
            "rule": {
                "id": "5712",
                "level": 8,
                "description": "Multiple connection attempts from same source. Possible port scan."
            },
            "agent": {
                "id": "001",
                "name": "Windows-PC"
            },
            "data": {
                "srcip": "203.0.113.45",
                "dstport": "Multiple (22, 80, 443, 3389, 8080)"
            },
            "timestamp": "2026-11-06T13:45:00.000Z"
        }
    ]
