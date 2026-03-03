from pymongo import MongoClient
import os

# Connect to MongoDB
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
client = MongoClient(MONGO_URL)
db = client['healthsecure']

def seed_database():
    """Seed the database with initial data"""
    
    # Clear existing data
    db.assets.delete_many({})
    db.vulnerabilities.delete_many({})
    db.phi_risks.delete_many({})
    db.compliance_controls.delete_many({})
    db.anomalies.delete_many({})
    
    # Seed Assets
    assets = [
        {"id": 1, "name": "Patient Records Database", "type": "Database", "status": "Active", "risk_score": 75},
        {"id": 2, "name": "MRI Scanner Workstation", "type": "Medical Device", "status": "Active", "risk_score": 45},
        {"id": 3, "name": "Email Server", "type": "Server", "status": "Active", "risk_score": 60},
        {"id": 4, "name": "HR Management System", "type": "Application", "status": "Active", "risk_score": 55},
        {"id": 5, "name": "Billing System", "type": "Application", "status": "Active", "risk_score": 40},
    ]
    db.assets.insert_many(assets)
    
    # Seed Vulnerabilities
    vulnerabilities = [
        {"id": 1, "title": "SQL Injection", "severity": "High", "status": "Open", "cvss": 8.5},
        {"id": 2, "title": "Outdated SSL/TLS", "severity": "Medium", "status": "Open", "cvss": 5.3},
        {"id": 3, "title": "Weak Password Policy", "severity": "High", "status": "Open", "cvss": 7.2},
        {"id": 4, "title": "Missing Security Patches", "severity": "Critical", "status": "Open", "cvss": 9.1},
        {"id": 5, "title": "Insecure File Permissions", "severity": "Medium", "status": "Closed", "cvss": 5.8},
    ]
    db.vulnerabilities.insert_many(vulnerabilities)
    
    # Seed PHI Risks
    phi_risks = [
        {"id": 1, "description": "Unauthorized access to patient records", "severity": "High", "status": "Open", "affected_patients": 150},
        {"id": 2, "description": "Unencrypted PHI in transit", "severity": "Critical", "status": "Open", "affected_patients": 500},
        {"id": 3, "description": "Improper disposal of medical records", "severity": "Medium", "status": "Closed", "affected_patients": 25},
        {"id": 4, "description": "PHI sharing without consent", "severity": "High", "status": "Open", "affected_patients": 80},
    ]
    db.phi_risks.insert_many(phi_risks)
    
    # Seed Compliance
    compliance = [
        {"id": 1, "control": "Access Control", "requirement": "HIPAA 164.312(a)", "status": "Compliant", "last_audit": "2024-01-15"},
        {"id": 2, "control": "Audit Controls", "requirement": "HIPAA 164.312(b)", "status": "Non-Compliant", "last_audit": "2024-01-20"},
        {"id": 3, "control": "Transmission Security", "requirement": "HIPAA 164.312(e)", "status": "Compliant", "last_audit": "2024-01-10"},
        {"id": 4, "control": "Device Controls", "requirement": "HIPAA 164.310(d)", "status": "Partially Compliant", "last_audit": "2024-01-25"},
    ]
    db.compliance_controls.insert_many(compliance)
    
    # Seed Anomalies
    anomalies = [
        {"id": 1, "type": "Unusual Access Pattern", "description": "Multiple failed login attempts from external IP", "severity": "High", "timestamp": "2024-01-26T10:30:00"},
        {"id": 2, "type": "Data Exfiltration", "description": "Large data transfer to unknown destination", "severity": "Critical", "timestamp": "2024-01-26T11:45:00"},
        {"id": 3, "type": "Privilege Escalation", "description": "Normal user accessing admin resources", "severity": "Medium", "timestamp": "2024-01-26T09:15:00"},
    ]
    db.anomalies.insert_many(anomalies)
    
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()
