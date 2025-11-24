#!/usr/bin/env python3
"""
OWASP ZAP Hook Script for CI/CD Pipeline
This script processes ZAP scan results and fails the build based on alert severity thresholds.
"""

import sys
import json
import defusedxml.ElementTree as ET


def parse_zap_xml(xml_file):
    """Parse ZAP XML report and return alert counts by severity"""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        alerts = {"High": 0, "Medium": 0, "Low": 0, "Informational": 0}

        # Parse alerts from XML
        for site in root.findall(".//site"):
            for alert in site.findall(".//alertitem"):
                risk = alert.find("riskdesc")
                if risk is not None:
                    risk_level = risk.text.split()[0]  # Get 'High', 'Medium', etc.
                    if risk_level in alerts:
                        alerts[risk_level] += 1

        return alerts
    except Exception as e:
        print(f"Error parsing ZAP XML report: {e}")
        return None


def main():
    xml_report = "zap-report.xml"

    print("\n" + "=" * 60)
    print("OWASP ZAP Scan Results")
    print("=" * 60)

    alerts = parse_zap_xml(xml_report)

    if alerts is None:
        print("❌ Failed to parse ZAP report")
        sys.exit(1)

    # Print summary
    print(f"\n📊 Alert Summary:")
    print(f"   High:          {alerts['High']}")
    print(f"   Medium:        {alerts['Medium']}")
    print(f"   Low:           {alerts['Low']}")
    print(f"   Informational: {alerts['Informational']}")
    print("\n" + "=" * 60)

    # Determine if build should fail
    # Threshold: Fail only on High severity alerts (Medium alerts will be warnings)
    if alerts["High"] > 0:
        print(f"\n❌ DAST SCAN FAILED!")
        print(f"   Found {alerts['High']} High severity alerts")
        print(f"   Security threshold exceeded - failing build")
        sys.exit(1)
    elif alerts["Medium"] > 0:
        print(f"\n⚠️  DAST SCAN PASSED WITH WARNINGS!")
        print(f"   Found {alerts['Medium']} Medium severity alerts")
        print(f"   These should be reviewed and fixed in future iterations")
        print(f"   Build will continue (only HIGH alerts block deployment)")
        sys.exit(0)
    else:
        print(f"\n✅ DAST SCAN PASSED!")
        print(f"   No High or Medium severity alerts found")
        sys.exit(0)


if __name__ == "__main__":
    main()
