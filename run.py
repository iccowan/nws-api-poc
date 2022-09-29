import requests
from time import sleep

EVENTS = ['Flood Warning']
AREA = 'FL'
API_URL = 'https://api.weather.gov/alerts/active'
CURRENT_ALERTS = {}

def main():
    global EVENTS
    EVENTS = list(map(lambda e: e.replace(' ', '%20'), EVENTS))

    while True:
        nws_alerts = getNwsAlerts()
        new_alerts = diffAlerts(nws_alerts)

        printAlerts(new_alerts)
        sleep(10)

def getNwsAlerts():
    nws_alerts = {}
    for e in EVENTS:
        res = requests.get(API_URL + '?area=' + AREA + '&event=' + e)
        all_alerts = res.json()['features']

        for alert in all_alerts:
            alert = alert['properties']
            this_alert = {'certainty': alert['certainty'], 'event': alert['event'], 'headline': alert['headline'], 'expires': alert['expires']}
            nws_alerts[alert['id']] = this_alert

    return nws_alerts

def diffAlerts(nws_alerts):
    global CURRENT_ALERTS

    new_alerts = []
    for (alert_id, alert) in nws_alerts.items():
        if alert_id not in CURRENT_ALERTS:
            CURRENT_ALERTS[alert_id] = alert
            new_alerts.append(alert)

    for (alert_id, alert) in CURRENT_ALERTS.items():
        if alert_id not in nws_alerts:
            del CURRENT_ALERTS[alert_id]
            
    return new_alerts

def printAlerts(alerts):
    for alert in alerts:
        print('NEW ' + alert['certainty'] + ' ' + alert['event'] + ' expiring at: ' + alert['expires'] + ' - ' + alert['headline'])

    if len(alerts) == 0:
        print('No new alerts')

main()
