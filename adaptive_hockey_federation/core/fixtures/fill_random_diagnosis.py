import json
import random


# TODO: (Скрипт который заполняет диагнозы игроков,
# но его можно убрать, как будут реальные данные
# по диагнозам игроков.) (! future update)


with open("main_player.json", "r", encoding="utf-8") as f:
    players = json.load(f)

with open("main_diagnosis.json", "r", encoding="utf-8") as f:
    diagnoses = json.load(f)

diagnosis_ids = [diagnosis["id"] for diagnosis in diagnoses]

for player in players:
    player["diagnosis_id"] = random.choice(diagnosis_ids)

with open("main_player.json", "w", encoding="utf-8") as f:
    json.dump(players, f, ensure_ascii=False, indent=4)

print("Диагнозы успешно назначены и сохранены в main_player_updated.json")
